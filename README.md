![alt text](https://github.com/caumente/AUDIT/blob/main/src/app/util/images/AUDIT.png)

<a href="https://github.com/caumente/AUDIT" title="Go to GitHub repo"><img src="https://img.shields.io/static/v1?label=caumente&message=rascore&color=e78ac3&logo=github" alt="caumente - rascore"></a>
<a href="https://github.com/caumente/AUDIT"><img src="https://img.shields.io/github/stars/caumente/AUDIT?style=social" alt="stars - rascore"></a>
<a href="https://github.com/caumente/AUDIT"><img src="https://img.shields.io/github/forks/caumente/AUDIT?style=social" alt="forks - rascore"></a>

</div>

<a href="https://github.com/caumente/audit/releases/"><img src="https://img.shields.io/github/release/caumente/audit?include_prereleases=&sort=semver&color=e78ac3" alt="GitHub release"></a>
<a href="#license"><img src="https://img.shields.io/badge/License-Apache_2.0-e78ac3" alt="License"></a>
<a href="https://github.com/caumente/audit/issues"><img src="https://img.shields.io/github/issues/caumente/audit" alt="issues - rascore"></a>

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
- **Longitudinal analysis**: Track your model performance over different timepoints.

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
### 1. Prerequisites
- Python 3.7+
- [Streamlit](https://streamlit.io/) for creating interactive web apps
- [Plotly](https://plotly.com/python/) for data visualization
- [Pandas](https://pandas.pydata.org/) for data manipulation


### 2. Installation

#### 2.1. Via PIP installer

**Quickstart commands for environment setup with [Anaconda](https://www.anaconda.com/products/individual):**

```bash
conda create -n audit_env python=3.8
conda activate audit_env
pip install audit
```

#### 2.2. Via AUDIT repository

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/brain-mri-analysis.git
    cd brain-mri-analysis
    ```
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration
Edit the `config.yml` file in `./src/app/` directory to set up the paths for data loading and other configurations:
```yaml
model_performance_analysis:
  data_paths:
    example_model: "path/to/your/data.csv"
  metrics_paths:
    example_model: "path/to/your/metrics.csv"
```

### 4. Run the APP
```bash
cd /Users/usr/audit
export PYTHONPATH=$PYTHONPATH:/Users/usr/audir/src
streamlit run src/app/GUI.py
```


### 5. Directory Structure

```bash
.src/
├ app/
  ├─ images/   
  ├─ pages/                                         # Directory for individual pages
    ├── Multivariate_features_analysis.py           # Multivariate features analysis page 
    ├── ...                                         # Other page files
    ├── Multimodel_performance_comparison.py        # Multi-model performance comparison page 
  ├─ Home_Page.py                                   # Main application file
  ├─ constants.py                                   # APP constants
  ├─ config.yaml                                    # APP config file
├ commons/
├ features/
├ metrics/
├ visualization/
├ README.md                                         # This readme file
├ feature_extractor.py                              # Feature extractor
├ feature_extractor_connfig.yaml                    # Feature extractor config file
├ metric_extractor.py                               # Metric extractor
├ metric_extractor_config.yaml                      # Metric extractor config file
```



## Authors

Please feel free to contact us with any issues, comments, or questions.

#### Mitchell Parker [![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/bukotsunikki.svg?style=social&label=Follow%20%40Mitch_P)](https://twitter.com/Mitch_P)

- Email: <mip34@drexel.edu> or <mitchell.parker@fccc.edu>
- GitHub: https://github.com/mitch-parker

#### Roland Dunbrack [![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/bukotsunikki.svg?style=social&label=Follow%20%40RolandDunbrack)](https://twitter.com/RolandDunbrack)

- Email: <roland.dunbrack@fccc.edu>
- GitHub: https://github.com/DunbrackLab

## Funding

- NIH NIGMS F30 GM142263 (to M.P.)
- NIH NIGMS R35 GM122517 (to R.D.)

## License
Apache License 2.0


Copyright (c) 2022 Mitchell Isaac Parker









### Future steps:
```bash
Combine the APP with PyMIA
Statistical features from raw MRIs
Code refactoring
```
