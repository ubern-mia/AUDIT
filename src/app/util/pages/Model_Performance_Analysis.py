import sys

import pandas as pd
import streamlit as st
from streamlit_plotly_events import plotly_events

from src.app.util.constants import ModelPerformanceAnalysisPage
from src.utils.operations.file_operations import load_config_file
from src.utils.operations.file_operations import read_datasets_from_dict
from src.utils.operations.misc_operations import capitalizer
from src.utils.operations.misc_operations import pretty_string
from src.utils.operations.misc_operations import snake_case
from src.visualization.scatter_plots import multivariate_metric_feature

const = ModelPerformanceAnalysisPage()


def setup_sidebar(data, aggregated):
    """
    Set up the sidebar for user interaction.

    Parameters:
    - data: DataFrame containing the dataset.
    - aggregated: Boolean indicating if the data is aggregated.

    Returns:
    - selected_set: List of selected datasets.
    - selected_model: Selected model.
    - select_x_axis: Selected feature for x-axis.
    - select_y_axis: Selected metric for y-axis.
    - selected_regions: List of selected regions.
    """
    with st.sidebar:
        st.header("Configuration")

        # Select dataset
        with st.sidebar.expander("Datasets", expanded=True):
            sets_available = list(data.set.unique())
            selected_set = st.multiselect(
                label="Select dataset to analyze:", options=sets_available, default=sets_available
            )

        # Select model
        with st.sidebar.expander("Models", expanded=True):
            selected_model = st.selectbox(
                label="Select model to visualize:",
                options=[capitalizer(pretty_string(m)) for m in data[data.set.isin(selected_set)].model.unique()],
            )

        # Select features
        with st.sidebar.expander("Features", expanded=True):
            select_y_axis = st.selectbox(label="Metric:", options=const.mapping_buttons_metrics.keys(),)

            select_x_axis = st.selectbox(label="Feature:", options=list(const.mapping_buttons_columns.keys()),)

        # Select regions if not aggregated
        selected_regions = None
        if not aggregated:
            with st.sidebar.expander("Regions", expanded=True):
                available_regions = list(data.region.unique())
                selected_regions = st.multiselect(
                    label="Select the regions to visualize:", options=available_regions, default=available_regions
                )

    return selected_set, selected_model, select_x_axis, select_y_axis, selected_regions


def merge_features_and_metrics(features: dict, metrics: dict, aggregate=True) -> pd.DataFrame:
    """
    Merge feature and metric datasets.

    Parameters:
    - features: Dictionary containing paths to feature datasets.
    - metrics: Dictionary containing paths to metric datasets.
    - aggregate: Boolean indicating if the data should be aggregated.

    Returns:
    - merged: DataFrame containing the merged data.
    """
    # Reading data
    features_df = read_datasets_from_dict(features)
    metrics_df = read_datasets_from_dict(metrics)

    # Aggregating metrics
    if aggregate:
        metrics_df = (
            metrics_df.drop(columns=["region"]).groupby(["ID", "model", "set"]).agg(lambda x: x.mean(skipna=True))
        )
    else:
        metrics_df = metrics_df.groupby(["ID", "model", "set", "region"]).agg(lambda x: x.mean(skipna=True))
    metrics_df.reset_index(inplace=True)

    # Merging data
    merged = metrics_df.merge(features_df, on=["ID", "set"])

    return merged


def visualize_data(data, set, model, regions, x_axis, y_axis, aggregated):
    """
    Filter data and visualize it using a scatter plot.

    Parameters:
    - data: DataFrame containing the data.
    - set: List of selected datasets.
    - model: Selected model.
    - regions: List of selected regions.
    - x_axis: Selected feature for x-axis.
    - y_axis: Selected metric for y-axis.
    - aggregated: Boolean indicating if the data is aggregated.
    """
    # Filter data
    filtered_data = data[data.set.isin(set)]
    filtered_data = filtered_data[filtered_data.model == snake_case(model)]
    if regions:
        filtered_data = filtered_data[filtered_data.region.isin(regions)]

    # Initialize session state for highlighted patients
    if "highlighted_patients" not in st.session_state:
        st.session_state.highlighted_patients = []
        st.session_state.dict_cases = {}

    # Visualize scatter plot
    fig = multivariate_metric_feature(
        data=filtered_data,
        x_axis=const.mapping_buttons_columns[x_axis],
        y_axis=const.mapping_buttons_metrics[y_axis],
        x_label=x_axis,
        y_label=y_axis,
        color="Dataset",
        facet_col="region" if not aggregated else None,
        highlighted_patients=st.session_state.highlighted_patients,
    )
    if not aggregated:
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    selected_points = plotly_events(fig, click_event=True, override_height=None)

    process_selected_points(selected_points, filtered_data, aggregated)

    # Button to reset highlighted cases
    reset_selected_cases = st.button(label="Reset highlighted cases")
    if reset_selected_cases:
        reset_highlighted_cases()


def process_selected_points(selected_points, data, aggregated):
    """
    Process points selected on the scatter plot.

    Parameters:
    - selected_points: Points selected on the plot.
    - data: DataFrame containing the data.
    - aggregated: Boolean indicating if the data is aggregated.
    """
    if selected_points and aggregated:
        point = selected_points[0]
        if point["curveNumber"] < len(data.set.unique()):
            point_subset = list(data.set.unique())[point["curveNumber"]]
            filtered_set_data = data[data.set == point_subset]
            selected_case = filtered_set_data.iloc[point["pointIndex"]]["ID"]

            # Add or remove the selected case
            if selected_case not in st.session_state.highlighted_patients:
                st.session_state.dict_cases[(f"{point['x']}", f"{point['y']}")] = selected_case
                st.session_state.highlighted_patients.append(selected_case)
        else:
            selected_case = st.session_state.dict_cases[(f"{point['x']}", f"{point['y']}")]
            st.session_state.highlighted_patients.remove(selected_case)
    if selected_points and not aggregated:
        st.markdown(
            ":red[Please, return to the aggregated view to highlight more cases and/or discard them or click on the "
            "'Reset highlighted cases' button below.]"
        )


def reset_highlighted_cases():
    """
    Reset the highlighted cases.
    """
    st.session_state.highlighted_patients = []
    st.session_state.dict_cases = {}
    st.rerun()


def performance():
    """
    Main function to run the Streamlit app.
    """

    # Load configuration file
    config = load_config_file("./src/configs/app_test.yml")
    if not config:
        st.error("Please set the configuration file up with a 'model_performance_analysis' key.")
        sys.exit()

    # Load metric and feature paths
    features_paths = config.get("features", {})
    metrics_paths = config.get("metrics", {})

    # Define page
    st.subheader(const.header)
    st.markdown(const.sub_header)

    # Load the data
    aggregated = st.checkbox("Aggregated", value=True, help="It aggregates all the regions, if enabled.")
    st.markdown("**Double click on a point to highlight it in red and then visualize it disaggregated.**")
    merged_data = merge_features_and_metrics(features=features_paths, metrics=metrics_paths, aggregate=aggregated)

    # Perform page logic
    selected_sets, selected_model, select_x_axis, select_y_axis, selected_regions = setup_sidebar(
        data=merged_data, aggregated=aggregated
    )
    if len(selected_sets) == 0:
        st.error("Please, select a dataset from the left sidebar", icon="🚨")
    else:
        visualize_data(
            data=merged_data,
            set=selected_sets,
            model=selected_model,
            regions=selected_regions,
            x_axis=select_x_axis,
            y_axis=select_y_axis,
            aggregated=aggregated,
        )

        st.markdown(const.description)
