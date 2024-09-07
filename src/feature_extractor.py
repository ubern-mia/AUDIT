from pathlib import Path
from datetime import datetime
from loguru import logger
from pprint import pformat

import pandas as pd
from colorama import Fore

from src.features.spatial import SpatialFeatures
from src.features.statistical import StatisticalFeatures
from src.features.tumor import TumorFeatures
from src.utils.operations.file_operations import load_config_file
from src.utils.operations.file_operations import ls_dirs
from src.utils.operations.misc_operations import fancy_print
from src.utils.operations.misc_operations import fancy_tqdm
from src.utils.sequences import get_spacing
from src.utils.sequences import load_nii_by_id
from src.utils.sequences import read_sequences_dict, read_sequences_dict_v2
from src.utils.operations.misc_operations import configure_logging


@logger.catch
def extract_features(path_images: str, config_file: dict) -> pd.DataFrame:
    """
    Extracts features from all the MRIs located in the specified directory and compiles them into a DataFrame.

    Args:
        path_images (str): The path to the directory containing patient image data.

    Returns:
        pd.DataFrame: A DataFrame containing extracted features for each patient, including spatial, tumor, and
                      statistical features.
    """

    patients_list = ls_dirs(path_images)

    # loop over all the elements in the root folder
    data = pd.DataFrame()

    with fancy_tqdm(total=len(patients_list), desc=f"{Fore.CYAN}Progress", leave=True) as pbar:
        for n, subject_id in enumerate(patients_list):
            logger.info(f"Processing subject: {subject_id}")

            # updating progress bar
            pbar.set_postfix_str(f"{Fore.CYAN}Current patient: {Fore.LIGHTBLUE_EX}{subject_id}{Fore.CYAN}")
            pbar.update(1)
            if n % 10 == 0 and n > 0:  # Every 10 patients
                fancy_print(f"Processed {n} patients", Fore.CYAN, "🔹")

            # read sequences and segmentation
            sequences = read_sequences_dict_v2(root=path_images, patient_id=subject_id)
            seg = load_nii_by_id(root=path_images, patient_id=subject_id, as_array=True)

            # calculating spacing
            sequences_spacing = get_spacing(img=load_nii_by_id(path_images, subject_id, "_t1ce"))
            seg_spacing = get_spacing(img=load_nii_by_id(path_images, subject_id, "_seg"))

            # calculate spatial features (dimensions and brain center mass)
            sf = SpatialFeatures(sequence=sequences.get("t1ce"), spacing=sequences_spacing)
            spatial_features = sf.extract_features()

            # calculate tumor features
            tf = TumorFeatures(
                segmentation=seg, spacing=seg_spacing, mapping_names=dict(zip(numeric_label, label_names))
            )
            tumor_features = tf.extract_features(sf.center_mass.values())

            # extract first order (statistical) information from sequences
            stats_features = {
                key: StatisticalFeatures(seq[seq > 0]).extract_features()
                for key, seq in sequences.items()
                if seq is not None
            }

            # TODO: revise this functionality, as some values were equals to 1 for all subjects
            # extract second order (texture) information from sequences
            # stats_features = {
            #     key: StatisticalFeatures(seq[seq > 0]).extract_features()
            #     for key, seq in sequences.items()
            #     if seq is not None
            # }

            patient_info_df = store_subject_information(subject_id, spatial_features, tumor_features, stats_features)

            # Add info to the main df
            data = pd.concat([data, patient_info_df], ignore_index=True)

        data = extract_longitudinal_info(config_file, data)

        return data


def store_subject_information(
    subject_id: str, spatial_features: dict, tumor_features: dict, stats_features: dict
) -> pd.DataFrame:
    """
    Stores the extracted features for a single patient in a DataFrame.

    Args:
        subject_id (str): The ID of the patient.
        spatial_features (dict): A dictionary containing spatial features extracted from the patient's images.
        tumor_features (dict): A dictionary containing tumor features extracted from the patient's segmentation.
        stats_features (dict): A dictionary containing statistical features extracted from the patient's sequences.

    Returns:
        pd.DataFrame: A DataFrame with the patient's ID and all extracted features, structured as a single row.
    """

    # storing information about patient
    patient_info = {"ID": subject_id}

    # including spatial information
    patient_info.update(spatial_features)

    # including tumor information
    patient_info.update(tumor_features)

    # including stats information
    for seq, dict_stats in stats_features.items():
        prefixed_stats = {f"{seq}_{k}": v for k, v in dict_stats.items()}
        patient_info.update(prefixed_stats)

    # including texture information
    # patient_info.update(textures_values)

    # from dict to dataframe
    patient_info_df = pd.DataFrame(patient_info, index=[0])

    return patient_info_df


def extract_longitudinal_info(config, df):
    longitudinal = config.get("longitudinal", {}).get(dataset_name, None)
    if longitudinal:
        pattern = longitudinal.get("pattern")
        longitudinal_id = longitudinal.get("longitudinal_id")
        time_point = longitudinal.get("time_point")
        df[["longitudinal_id", "time_point"]] = (
            df["ID"].str.split(pattern, expand=True).iloc[:, [longitudinal_id, time_point]]
        )
        df["time_point"] = df["time_point"].astype(int)
    else:
        df["longitudinal_id"] = ""
        df["time_point"] = 0

    return df


if __name__ == "__main__":
    logger.remove()
    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    configure_logging(log_filename=f"./logs/feature_extraction/{current_time}.log")
    logger.info("Starting feature extraction process")

    # config variables
    config = load_config_file("./src/configs/feature_extractor.yml")
    data_paths = config["data_paths"]
    label_names, numeric_label = list(config["labels"].keys()), list(config["labels"].values())
    output_path = config["output_path"]
    Path(output_path).mkdir(parents=True, exist_ok=True)
    logger.info(f"Config file: \n{pformat(config)}")

    # iterate over all paths
    for dataset_name, src_path in data_paths.items():
        fancy_print(f"Starting feature extraction for {dataset_name}", Fore.LIGHTMAGENTA_EX, "\n✨")
        logger.info(f"Starting feature extraction for {dataset_name}")

        # features extraction
        extracted_feats = extract_features(path_images=src_path, config_file=config)
        logger.info(f"Finishing feature extraction for {dataset_name}")

        # TODO: Should it have nan values or they must be 0? When NAN value, they do not appear in plots.
        extracted_feats.to_csv(f"{output_path}/extracted_information_{dataset_name}.csv", index=False)
        logger.info(f"Results exported to CSV for {dataset_name}")
