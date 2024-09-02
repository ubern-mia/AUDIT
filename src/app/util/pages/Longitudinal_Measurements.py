import pandas as pd
import streamlit as st

from src.app.util.constants import LongitudinalAnalysis
from src.utils.operations.file_operations import load_config_file
from src.utils.operations.file_operations import read_datasets_from_dict
from src.utils.operations.misc_operations import capitalizer
from src.utils.operations.misc_operations import pretty_string
from src.utils.operations.misc_operations import snake_case
from src.visualization.time_series import plot_longitudinal
from src.visualization.time_series import plot_longitudinal2

const = LongitudinalAnalysis()

# Load configuration and data
config = load_config_file("./src/configs/app.yml")
datasets_root_path = config.get("datasets_root_path")
features_paths = config.get("longitudinal_measurements").get('features')
metrics_paths = config.get("longitudinal_measurements").get('metrics')
features = const.mapping_buttons_columns



def main(features: dict, metrics: dict) -> pd.DataFrame:
    """
    Merge feature and metric datasets.

    Parameters:
    - features: Dictionary containing paths to feature datasets.
    - metrics: Dictionary containing paths to metric datasets.
    - aggregate: Boolean indicating if the data should be aggregated.

    Returns:
    - merged: DataFrame containing the merged data.
    """
    # Reading feature data
    features_df = read_datasets_from_dict(features)
    features_df = features_df[["ID", "set", "patient_name", "timepoint"] + [c for c in features_df.columns if "size" in c]]

    # Reading metrics data
    metrics_df = read_datasets_from_dict(metrics)
    metrics_df = metrics_df[["ID", "model", "set", "size", "region"]]
    metrics_df = metrics_df.pivot_table(index=['ID', 'model', 'set'], columns='region', values='size').reset_index()
    metrics_df.columns = [f"lesion_size_{col.lower()}_pred" if col not in ['ID', 'model', 'set'] else col for col in
                          metrics_df.columns]

    # Merging data
    merged = metrics_df.merge(features_df, on=['ID', 'set'])

    # Calculating totals
    pred_lesion_size_columns = [col for col in merged.columns if 'lesion_size' in col and '_pred' in col]
    merged['lesion_size_pred'] = merged[pred_lesion_size_columns].sum(axis=1)

    return merged


# Sidebar setup for selecting datasets and variables
def setup_sidebar(data, data_paths):
    """
    Set up the sidebar with options to select datasets and variables.

    Args:
        data_paths (dict): Dictionary with paths to datasets.
        allowed_features (dict): Dictionary of allowed features for selection.

    Returns:
        tuple: Contains selected datasets, X-axis variable, Y-axis variable, and color-axis variable.
    """
    with st.sidebar:
        st.header("Configuration")

        # Select datasets
        with st.sidebar.expander("Dataset", expanded=True):
            selected_set = st.selectbox(
                label="Select datasets to visualize:",
                options=data_paths.keys(),
                index=0
            )
        with st.sidebar.expander("Models", expanded=True):
            models_available = [capitalizer(pretty_string(m)) for m in data.model.unique()]
            selected_model = st.selectbox(
                label="Select a model:",
                options=models_available,
                index=0)

        # Filter datasets
        # st.table(data)
        data = data[(data['set'] == selected_set) & (data['model'] == snake_case(selected_model))]

        # Filter unique patients
        patients = sorted(data.patient_name.unique())
        with st.sidebar.expander("Patient", expanded=True):
            patient_selected = st.selectbox(
                label="Select a patient to visualize:",
                options=patients,
                index=0
            )

        st.write("[Contact us - MIA group](%s)" % const.mia_url)

        return data[data.patient_name == patient_selected].reset_index(drop=True)


# Main function for visualization and ITK-SNAP interaction
def plot_visualization(merged_data):
    """
    Main function to load datasets, filter data, create scatter plots, and handle ITK-SNAP interaction.

    Args:
        sets (list): List of selected datasets.
        x_axis (str): Selected X-axis variable.
        y_axis (str): Selected Y-axis variable.
        color_axis (str): Selected color-axis variable.
    """

    # Mostrar el gráfico
    fig = plot_longitudinal(merged_data)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True, scrolling=True)

    # Description
    st.markdown(const.description)

    fig = plot_longitudinal2(merged_data)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True, scrolling=True)


def longitudinal():
    # Define page layout
    st.header(const.header)
    st.markdown(const.sub_header)

    # Sidebar setup
    merged_data = main(features=features_paths, metrics=metrics_paths)
    data = setup_sidebar(merged_data, features_paths)

    # Main functionality
    plot_visualization(data)

