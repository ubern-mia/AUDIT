import os
import numpy as np

import SimpleITK as sitk
import pandas as pd
import pymia.evaluation.evaluator as eval_
import pymia.evaluation.metric as metric
import pymia.evaluation.writer as writer

from src.commons.commons import ls_dirs, load_config_file

# custom params for pycharm
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)



if __name__ == '__main__':

    # config variables
    config = load_config_file("metric_extractor_config.yml")
    labels, processed_labels = config['labels'], {}
    for key, value in labels.items():
        if isinstance(value, list):
            value = tuple(value)
        processed_labels[value] = key

    output_path = config['output_path']

    # load paths to the datasets
    path_ground_truth = config['ground_truth_data_path']
    path_predictions = list(config['model_predictions_paths'].values())
    patients = ls_dirs(path_ground_truth)

    for path in [path_ground_truth] + path_predictions:
        if not os.path.exists(path):
            raise NotADirectoryError(f'"{path}" does not exist')

    # metrics to extract
    metrics = [
        metric.HausdorffDistance(percentile=95, metric="haus"),
        metric.DiceCoefficient(metric="dice"),
        metric.Sensitivity(metric="sens"),
        metric.Specificity(metric="spec"),
        metric.Accuracy(metric="accu"),
        metric.JaccardCoefficient(metric="jacc"),
        metric.Precision(metric="prec")
    ]

    """
    Raw metric calculation
    """
    # initializing output metrics
    raw_metrics = []
    evaluator = eval_.SegmentationEvaluator(metrics, processed_labels)

    # load paths to predictions
    models = config["model_predictions_paths"]
    for model_name, path_predictions in models.items():
        print(f"\n\n********* Model: {model_name} *********")

        # loop over all the elements in the root folder
        for n, ID in enumerate(patients):
            # if n > 1:
            #     break
            print(f"\t Evaluating patient {ID}")
            gt_path = os.path.join(path_ground_truth, ID, f'{ID}_seg.nii.gz')
            pred_path = os.path.join(path_predictions, ID, f'{ID}_pred.nii.gz')

            try:
                if not os.path.exists(gt_path):
                    raise FileNotFoundError(f'Ground truth file "{gt_path}" does not exist')

                if not os.path.exists(pred_path):
                    raise FileNotFoundError(f'Prediction file "{pred_path}" does not exist')

                ground_truth = sitk.ReadImage(gt_path)
                prediction = sitk.ReadImage(pred_path)
                evaluator.evaluate(prediction, ground_truth, ID)
            except Exception as e:
                print(f'{ID} -> {e}')

        # accumulate the results for each of the models
        for result in evaluator.results:
            result_dict = {
                'ID': result.id_,
                'region': result.label,
                'metric': result.metric,
                'value': result.value,
                'model': model_name
            }
            raw_metrics.append(result_dict)

        # if config["calculate_stats"]:
        #     functions = {
        #         'MEAN': np.mean,
        #         'MEDIAN': np.median,
        #         'STD': np.std,
        #         'MIN': np.min,
        #         'MAX': np.max,
        #         'Q1': lambda x: np.percentile(x, 25),
        #         'Q3': lambda x: np.percentile(x, 75),
        #         'CI_2.5': lambda x: np.percentile(x, 2.5),
        #         'CI_5': lambda x: np.percentile(x, 5),
        #         'CI_95': lambda x: np.percentile(x, 95),
        #         'CI_97.5': lambda x: np.percentile(x, 97.5),
        #     }
        #     writer.CSVStatisticsWriter(f"{output_path}/stats/{model_name}/{config['filename']}.csv", index=False, functions=functions).write(evaluator.results)
        #     writer.ConsoleStatisticsWriter(functions=functions).write(evaluator.results)
        evaluator.clear()

    # Convert all metrics to a DataFrame
    all_metrics_df = pd.DataFrame(raw_metrics)

    # Pivot the DataFrame to have metrics as columns and save results
    all_metrics_pivot = all_metrics_df.pivot_table(index=['ID', 'region', 'model'], columns='metric', values='value')
    all_metrics_pivot.reset_index(inplace=True)
    all_metrics_pivot.sort_values(by=['model', 'ID', 'region'], inplace=True)
    all_metrics_pivot.to_csv(f"{output_path}/{config['filename']}.csv", index=False)
