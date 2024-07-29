import os

import numpy as np
import pymia.evaluation.evaluator as eval_
import pymia.evaluation.metric as metric
import pymia.evaluation.writer as writer
import SimpleITK as sitk

gt_dir = '/home/melandur/Downloads/fda_data/fda_images'  # ground truth directory
pred_dir = '/home/melandur/Downloads/fda_data/fda_preds/fda_mvp_23'  # prediction directory
dst_dir = '/home/melandur/Downloads/metrics/fda/fda_mvp_23'  # destination directory

metrics = [
    metric.DiceCoefficient("dice"),
    metric.HausdorffDistance(95),
    metric.ReferenceVolume(),
    metric.PredictionVolume()
]

labels = {1: 'ed',
          2: 'en',
          3: 'ne',
          (2, 3): 'tc',
          }


os.makedirs(dst_dir, exist_ok=True)

for path in [gt_dir, pred_dir, dst_dir]:
    if not os.path.exists(path):
        raise NotADirectoryError(f'"{path}" does not exist')

result_file = os.path.join(dst_dir, 'results.csv')
result_summary_file = os.path.join(dst_dir, 'results_summary.csv')

evaluator = eval_.SegmentationEvaluator(metrics, labels)

subjects = os.listdir(gt_dir)

for subject in subjects:
    subject_id = subject.split('.')[0]
    gt_path = os.path.join(gt_dir, subject, f'{subject}_seg.nii.gz')
    pred_path = os.path.join(pred_dir, subject, f'{subject}_pred.nii.gz')

    try:
        if not os.path.exists(gt_path):
            raise FileNotFoundError(f'Ground truth file "{gt_path}" does not exist')

        if not os.path.exists(pred_path):
            raise FileNotFoundError(f'Prediction file "{pred_path}" does not exist')

        print(f'Evaluating -> {subject_id}')

        ground_truth = sitk.ReadImage(gt_path)
        prediction = sitk.ReadImage(pred_path)
        evaluator.evaluate(prediction, ground_truth, subject_id)
    except Exception as e:
         print(f'{subject_id} -> {e}')

writer.CSVWriter(result_file).write(evaluator.results)

# print('\nSubject-wise results...')
# writer.ConsoleWriter().write(evaluator.results)
#
# functions = {
#     'MEAN': np.mean,
#     'MEDIAN': np.median,
#     'STD': np.std,
#     'MIN': np.min,
#     'MAX': np.max,
#     'Q1': lambda x: np.percentile(x, 25),
#     'Q3': lambda x: np.percentile(x, 75),
#     'CI_2.5': lambda x: np.percentile(x, 2.5),
#     'CI_5': lambda x: np.percentile(x, 5),
#     'CI_95': lambda x: np.percentile(x, 95),
#     'CI_97.5': lambda x: np.percentile(x, 97.5),
# }
# writer.CSVStatisticsWriter(result_summary_file, functions=functions).write(evaluator.results)
# print('\nAggregated statistic results...')
# writer.ConsoleStatisticsWriter(functions=functions).write(evaluator.results)
# evaluator.clear()