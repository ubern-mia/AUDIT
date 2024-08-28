from pathlib import Path
import pandas as pd

from src.commons.commons import ls_dirs, load_config_file
from src.commons.sequences import get_spacing
from src.commons.sequences import load_subject_nii
from src.commons.sequences import read_segmentation
from src.commons.sequences import read_sequences_dict
from src.features.spatial import SpatialFeatures
from src.features.statistical import StatisticalFeatures
from src.features.tumor import TumorFeatures
from src.features.texture import compute_texture_values, extract_radiomics_features
from src.commons.commons import fancy_tqdm, fancy_print

from colorama import Fore, Style


def extract_features(path_images: str) -> pd.DataFrame:
    patients_list = ls_dirs(path_images)

    # loop over all the elements in the root folder
    data = pd.DataFrame()

    with fancy_tqdm(total=len(patients_list), desc=f"{Fore.CYAN}Progress", leave=True) as pbar:
        for n, ID in enumerate(patients_list):
            # updating progress bar
            pbar.set_postfix_str(f"{Fore.CYAN}Current patient: {Fore.LIGHTBLUE_EX}{ID}{Fore.CYAN}")
            pbar.update(1)
            if n % 10 == 0 and n > 0:  # Every 10 patients
                fancy_print(f"Processed {n} patients", Fore.CYAN, '🔹')

            # read sequences and segmentation
            sequences = read_sequences_dict(root=root_imgs, patient_id=ID)
            seg = read_segmentation(root=root_imgs, patient_id=ID)

            # calculating spacing
            sequences_spacing = get_spacing(img=load_subject_nii(root_imgs, ID, "t1ce"))
            seg_spacing = get_spacing(img=load_subject_nii(root_imgs, ID, "seg"))

            # calculate spatial features (dimensions and brain center mass)
            sf = SpatialFeatures(sequence=sequences.get('t1c'), spacing=sequences_spacing)
            spatial_features = sf.extract_features()

            # calculate tumor features
            tf = TumorFeatures(segmentation=seg, spacing=seg_spacing, mapping_names=dict(zip(numeric_label, label_names)))
            tumor_features = tf.extract_features(sf.center_mass.values())

            # extract first order (statistical) information from sequences
            stats_features = {key: StatisticalFeatures(seq[seq > 0]).extract_features() for key, seq in sequences.items() if seq is not None}

            # TODO: revise this functionality, as some values were equals to 1 for all subjects
            # extract second order (texture) information from sequences
            #stats_features = {key: StatisticalFeatures(seq[seq > 0]).extract_features() for key, seq in sequences.items() if seq is not None}

            # extract radiomics features
            # radiomics = extract_radiomics_features(f"{root_imgs}/{ID}/{ID}_t1.nii.gz")
            # print(radiomics)

            patient_info_df = store_subject_information(ID, spatial_features, tumor_features, stats_features)

            # Add info to the main df
            data = pd.concat([data, patient_info_df], ignore_index=True)

        return data


def store_subject_information(ID, spatial_features, tumor_features, stats_features):
    # storing information about patient
    patient_info = {
        'ID': ID
    }

    # including spatial information
    patient_info.update(spatial_features)

    # including tumor information
    patient_info.update(tumor_features)

    # including stats information
    for seq, dict_stats in stats_features.items():
        prefixed_stats = {f'{seq}_{k}': v for k, v in dict_stats.items()}
        patient_info.update(prefixed_stats)

    # including texture information
    # patient_info.update(textures_values)

    # from dict to dataframe
    patient_info_df = pd.DataFrame(patient_info, index=[0])

    return patient_info_df


if __name__ == '__main__':

    # config variables
    config = load_config_file("./feature_extractor_config.yml")
    feature_extractor_paths = config['feature_extractor_paths']
    label_names, numeric_label = list(config["labels"].keys()), list(config["labels"].values())
    output_path = config['output_path']
    Path(output_path).mkdir(parents=True, exist_ok=True)

    # iterate over all paths
    for name, root_imgs in feature_extractor_paths.items():
        fancy_print(f"Starting feature extraction for {name}", Fore.LIGHTMAGENTA_EX, '\n✨')
        extracted_information = extract_features(path_images=root_imgs)

        longitudinal = config["longitudinal"].get(name, None)
        if longitudinal:
            pattern = longitudinal.get("pattern")
            patient_name = longitudinal.get("patient_name")
            timepoint = longitudinal.get("timepoint")
            extracted_information[['patient_name', 'timepoint']] = extracted_information['ID'].str.split(pattern,
                                                                                                         expand=True).iloc[
                                                                   :, [patient_name, timepoint]]
            extracted_information["timepoint"] = extracted_information["timepoint"].astype(int)
        else:
            extracted_information['patient_name'] = ""
            extracted_information['timepoint'] = 0

        # TODO: Should it have nan values or they must be 0? When NAN value, they do not appear in plots.
        extracted_information.to_csv(f"{output_path}/extracted_information_{name}.csv", index=False)


