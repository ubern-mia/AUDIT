# AUDIT

# Brain MRI Analysis and Visualization Framework

## Overview
This framework is designed to analyze, visualize, and detect biases in brain MRI data. It provides tools for loading and processing MRI data, extracting relevant features, and visualizing model performance and biases in predictions.

## Features
- **Data Loading**: Easily work with MRI data from various sources.
- **Feature Extraction**: Extract relevant features from MRI images and their segmentations for analysis.
- **Visualization**: Visualize model performance, including false positives and negatives, using interactive plots.
- **Model robustness**: Assess the robustness of the model by evaluating its performance across different datasets and conditions.
- **Bias Detection**: Identify potential biases in model predictions and performance.

## Directory Structure

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



## Getting Started
### Prerequisites
- Python 3.7+
- [Streamlit](https://streamlit.io/) for creating interactive web apps
- [Plotly](https://plotly.com/python/) for data visualization
- [Pandas](https://pandas.pydata.org/) for data manipulation

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/brain-mri-analysis.git
    cd brain-mri-analysis
    ```
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration
Edit the `config.yml` file in `./src/app/` directory to set up the paths for data loading and other configurations:
```yaml
model_performance_analysis:
  data_paths:
    example_model: "path/to/your/data.csv"
  metrics_paths:
    example_model: "path/to/your/metrics.csv"
```




### Run the APP
```bash
cd /Users/caumente/Projects/robustness
export PYTHONPATH=$PYTHONPATH:/Users/caumente/Projects/robustness/src
streamlit run src/app/Home_Page.py
```




### Future steps:
```bash
Combine the APP with PyMIA
Statistical features from raw MRIs
Code refactoring
```
