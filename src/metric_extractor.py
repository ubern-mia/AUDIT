import pandas as pd
from pathlib import Path
from src.commons.sequences import get_spacing
from src.commons.commons import ls_dirs, load_config_file, fancy_print, fancy_tqdm
from src.commons.sequences import read_segmentation, read_prediction
from src.metrics.custom_metrics import calculate_metrics, one_hot_encoding
from src.commons.sequences import load_subject_nii
from colorama import Fore

# TODO: check if removing this two lines
# custom params for pycharm
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)


def process_metric(data, models):
    metrics_cols = data.drop(columns=["ID", "region", "model"]).columns
    post_processed_metrics = []

    for metric in metrics_cols:
        df_ = data[['ID', 'region', 'model', metric]]
        pivot_df = df_.pivot_table(index=['ID', 'region'], columns='model', values=metric).reset_index()

        # difference of all models with respect to the baseline model
        for model in models:
            if model != 'baseline':
                pivot_df[f'{model}'] = 100 * (pivot_df[f'{model}'] - pivot_df[f'baseline']) / pivot_df[f'baseline']

        pivot_df.drop(columns='baseline', inplace=True)
        pivot_df['metric'] = metric
        post_processed_metrics.append(pivot_df)

    out = pd.concat(post_processed_metrics)
    out = pd.melt(out, id_vars=['ID', 'region', 'metric'], value_vars=['model_1', 'model_2'])

    return out


if __name__ == '__main__':

    # config variables
    config = load_config_file("metric_extractor_config.yml")
    label_names, numeric_label = list(config["labels"].keys()), list(config["labels"].values())
    output_path = config['output_path']
    Path(output_path).mkdir(parents=True, exist_ok=True)

    # load paths to test data
    path_test_dataset = config['ground_truth_data_path']
    patients_list = ls_dirs(path_test_dataset)

    """
    Raw metric calculation
    """
    # initializing output metrics
    raw_metrics = pd.DataFrame()

    # load paths to predictions
    models = config["model_predictions_paths"]
    for model_name, path_predictions in models.items():
        fancy_print(f"\nStarting metric extraction for model {model_name}", Fore.LIGHTMAGENTA_EX, '✨')

        # loop over all the elements in the root folder
        with fancy_tqdm(total=len(patients_list), desc=f"{Fore.CYAN}Progress", leave=True) as pbar:
            for n, ID in enumerate(patients_list):
                pbar.set_postfix_str(f"{Fore.CYAN}Current patient: {Fore.LIGHTBLUE_EX}{ID}{Fore.CYAN}")
                pbar.update(1)
                if n % 10 == 0 and n > 0:
                    fancy_print(f"Processed {n} patients", Fore.CYAN, '🔹')

                # if n > 5:
                #     break

                # read ground truth segmentation and prediction
                gt = read_segmentation(root=path_test_dataset, patient_id=ID)
                pred = read_prediction(root=path_predictions, patient_id=ID)
                spacing = get_spacing(load_subject_nii(path_predictions, ID, "pred"))

                # making the segmentations binary (one hot encoding for each region)
                gt = one_hot_encoding(gt, numeric_label)
                pred = one_hot_encoding(pred, numeric_label)

                # compute metrics
                metrics = calculate_metrics(ground_truth=gt, segmentation=pred, patient=ID, regions=label_names, spacing=spacing)

                # from list of dict to dataframe
                patient_info_df = pd.DataFrame(metrics)

                # add model info
                patient_info_df["model"] = model_name

                # Add info to the main df
                raw_metrics = pd.concat([raw_metrics, patient_info_df], ignore_index=True)

    # saving raw results
    raw_metrics.to_csv(f"{output_path}/{config['filename']}.csv", index=False)
