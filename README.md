
[//]: # (![alt text]&#40;https://github.com/caumente/AUDIT/blob/main/src/app/util/images/AUDIT_big.jpeg&#41;)
![alt text](https://github.com/caumente/AUDIT/blob/main/src/app/util/images/AUDIT_medium.jpeg)


<a href="https://github.com/caumente/AUDIT" title="Go to GitHub repo"><img src="https://img.shields.io/static/v1?label=caumente&message=AUDIT&color=e78ac3&logo=github" alt="caumente - AUDIT"></a>
<a href="https://github.com/caumente/AUDIT"><img src="https://img.shields.io/github/stars/caumente/AUDIT?style=social" alt="stars - AUDIT"></a>
<a href="https://github.com/caumente/AUDIT"><img src="https://img.shields.io/github/forks/caumente/AUDIT?style=social" alt="forks - AUDIT"></a>


<a href="https://github.com/caumente/audit/releases/"><img src="https://img.shields.io/github/release/caumente/audit?include_prereleases=&sort=semver&color=e78ac3" alt="GitHub release"></a>
<a href="#license"><img src="https://img.shields.io/badge/License-Apache_2.0-e78ac3" alt="License"></a>
<a href="https://github.com/caumente/audit/issues"><img src="https://img.shields.io/github/issues/caumente/audit" alt="issues - AUDIT"></a>


## Summary

AUDIT, Analysis & evalUation Dashboard of artIficial inTelligence, is a tool designed to analyze,
visualize, and detect biases in brain MRI data and models. It provides tools for loading and processing MRI data,
extracting relevant features, and visualizing model performance and biases in predictions. AUDIT presents the 
following features:


- **Data management**: Easily work with MRI data from various sources.
- **Feature extraction**: Extract relevant features from MRI images and their segmentations for analysis.
- **Visualization**: Visualize model performance, including false positives and negatives, using interactive plots.
- **Model robustness**: Assess the robustness of the model by evaluating its performance across different datasets and conditions.
- **Bias detection**: Identify potential biases in model predictions and performance.
- **Longitudinal analysis**: Track your model performance over different time points.

Details of our work are provided in [*our paper*](https://aacrjournals.org/cancerres/article/doi/10.1158/0008-5472.CAN-22-0804/696349/Delineating-The-RAS-Conformational-LandscapeThe), **Delineating The RAS Conformational Landscape**. We hope that researchers will use *Rascore* to gain novel insights into RAS biology and drug discovery. 


## Usage
- **Home Page**: The main landing page of the tool.
- **Univariate Analysis**: Analysis of individual variables to understand their distributions and characteristics.
- **Multivariate Analysis**: Examination of multiple variables simultaneously to explore relationships and patterns.
- **Segmentation Error Matrix**: A table displaying the errors associated with different segmentation tasks.
- **Model Performance Analysis**: Evaluation of the effectiveness and accuracy of a single model.
- **Pairwise Model Performance Comparison**: Comparison of performance metrics between two different models.
- **Multi-model Performance Comparison**: Comparative analysis of performance metrics across multiple models.
- **Longitudinal Measurements**: Analysis of data collected over time to observe trends and changes.
- **Subjects Exploration**: Detailed examination of individual subjects within the dataset.


## Web AUDIT

Last released version of **AUDIT** is hosted at https://rascore.streamlitapp.com for an online overview of its functionalities.


## Getting Started

### 1. Installation

**(Recommended) Create an isolated Anaconda environment:**

```bash
conda create -n audit_env python=3.10
conda activate audit_env
```

#### 1.1. (Not available yet) Via PIP installer


```bash
pip install audit
```

#### 1.2. Via AUDIT repository

1. Clone the repository:
    ```bash
    git clone https://github.com/caumente/AUDIT.git
    cd AUDIT
    ```
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
   
3. Export path
    ```bash
    export PYTHONPATH=$PYTHONPATH:/home/user/AUDIT/src
    ```

### 2. Configuration

Edit the config files in `./src/configs/` directory to set up the paths for data loading and other configurations:

#### 2.1. Feature extractor config

```yaml
feature_extractor_paths:
  DATASET_1: '/home/user/AUDIT/datasets/d1/d1_images'
  DATASET_2: '/home/user/AUDIT/datasets/d2/d2_images'
  DATASET_N: '/home/user/AUDIT/datasets/dN/dN_images'
labels:
  BKG: 0
  EDE: 2
  ENH: 4
  NEC: 1
longitudinal:
  DATASET_1:
    pattern: "-"
    longitudinal_id: 1
    time_point: 2
output_path: '/home/user/AUDIT/outputs/features'

```

#### 2.2. Metric extractor config

```yaml
data_path: '/home/user/AUDIT/datasets/dN/dN_images'
model_predictions_paths:
  MODEL_1: '/home/user/AUDIT/datasets/dN/dN_seg/dN_model_1'
  MODEL_2: '/home/user/AUDIT/datasets/dN/dN_seg/dN_model_2'
  MODEL_M: '/home/user/AUDIT/datasets/dN/dN_seg/dN_model_N'
labels:
  BKG: 0
  EDE: 2
  ENH: 4
  NEC: 1
output_path: '/home/user/AUDIT/outputs/metrics'
filename: 'dataset_N'
```

#### 2.3. APP config

```yaml
labels:
  BKG: 0
  EDE: 4
  ENH: 1
  NEC: 2
datasets_root_path: '/home/user/AUDIT/datasets'
csv_features_path: '/home/user/AUDIT/outputs'
features_analysis:
  data_paths:
    DATASET_1: '/home/user/AUDIT/outputs/features/extracted_information_D1.csv'
    DATASET_2: '/home/user/AUDIT/outputs/features/extracted_information_D2.csv'
    DATASET_N: '/home/user/AUDIT/outputs/features/extracted_information_DN.csv'

distributions_analysis:
  data_paths:
    DATASET_1: '/home/user/AUDIT/outputs/features/extracted_information_D1.csv'
    DATASET_2: '/home/user/AUDIT/outputs/features/extracted_information_D2.csv'
    DATASET_N: '/home/user/AUDIT/outputs/features/extracted_information_DN.csv'

segmentation_error_analysis:
  DATASET_1:
    ground_truth: '/home/user/AUDIT/datasets/d1/d1_images'
    MODEL_1: '/home/user/AUDIT/datasets/d1/d1_seg/d1_model_1'
    MODEL_2: '/home/user/AUDIT/datasets/d1/d1_seg/d1_model_2'
    MODEL_M: '/home/user/AUDIT/datasets/d1/d1_seg/d1_model_M'
  DATASET_2:
    ground_truth: '/home/user/AUDIT/datasets/d2/d2_images'
    MODEL_1: '/home/user/AUDIT/datasets/d2/d2_seg/d2_model_1'
    MODEL_2: '/home/user/AUDIT/datasets/d2/d2_seg/d2_model_2'
    MODEL_M: '/home/user/AUDIT/datasets/d2/d2_seg/d2_model_M'
  DATASET_N:
    ground_truth: '/home/user/AUDIT/datasets/dN/dN_images'
    MODEL_1: '/home/user/AUDIT/datasets/dN/dN_seg/dN_model_1'
    MODEL_2: '/home/user/AUDIT/datasets/dN/dN_seg/dN_model_2'
    MODEL_M: '/home/user/AUDIT/datasets/dN/dN_seg/dN_model_M'

model_performance_analysis:
  features:
    DATASET_1: '/home/user/AUDIT/outputs/features/extracted_information_D1.csv'
    DATASET_2: '/home/user/AUDIT/outputs/features/extracted_information_D2.csv'
    DATASET_N: '/home/user/AUDIT/outputs/features/extracted_information_DN.csv'
  metrics:
    DATASET_1: '/home/user/AUDIT/outputs/metrics/extracted_information_D1.csv'
    DATASET_2: '/home/user/AUDIT/outputs/metrics/extracted_information_D2.csv'
    DATASET_N: '/home/user/AUDIT/outputs/metrics/extracted_information_DN.csv'
    
model_performance_comparison:
  metrics:
    DATASET_1: '/home/user/AUDIT/outputs/metrics/extracted_information_D1.csv'
    DATASET_2: '/home/user/AUDIT/outputs/metrics/extracted_information_D2.csv'
    DATASET_N: '/home/user/AUDIT/outputs/metrics/extracted_information_DN.csv'
  features:
    DATASET_1: '/home/user/AUDIT/outputs/features/extracted_information_D1.csv'
    DATASET_2: '/home/user/AUDIT/outputs/features/extracted_information_D2.csv'
    DATASET_N: '/home/user/AUDIT/outputs/features/extracted_information_DN.csv'

longitudinal_measurements:
  features:
    DATASET_1: '/home/user/AUDIT/outputs/features/extracted_information_D1.csv'
  metrics:
    DATASET_1: '/home/user/AUDIT/outputs/metrics/extracted_information_D1.csv'

```

### 3. Run the *Feature extractor* and *Metric extractor* scripts:

```bash
python src/feature_extractor.py
```

```bash
python src/metric_extractor.py
```

### 4. Run the APP

```bash
streamlit run src/app/GUI.py
```


## Authors

Please feel free to contact us with any issues, comments, or questions.

#### Carlos Aumente 

- Email: <mip34@drexel.edu> or <mitchell.parker@fccc.edu>
- GitHub: https://github.com/caumente

#### ..... 

- Email: <roland.dunbrack@fccc.edu>
- GitHub: https://github.com/DunbrackLab


## License
Apache License 2.0





