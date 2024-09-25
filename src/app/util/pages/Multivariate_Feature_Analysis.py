import streamlit as st
from streamlit_plotly_events import plotly_events

from src.app.util.commons.data_preprocessing import processing_data
from src.app.util.commons.checks import health_checks
from src.app.util.constants_test.descriptions import MultivariatePage
from src.app.util.constants_test.features import Features
from src.utils.operations.file_operations import load_config_file
from src.utils.operations.file_operations import read_datasets_from_dict
from src.utils.operations.itk_operations import run_itk_snap
from src.visualization.scatter_plots import multivariate_features_highlighter

# Load constants
const = MultivariatePage()
const_features = Features()

# Load configuration
config = load_config_file("./src/configs/app.yml")
datasets_root_path = config.get("datasets_path")
features_information = config.get("features")


# Sidebar setup for selecting datasets and variables
def setup_sidebar(data, data_paths):
    with st.sidebar:
        st.header("Configuration")

        # Select datasets
        with st.sidebar.expander("Datasets", expanded=True):
            selected_sets = st.multiselect(
                label="Select datasets to visualize:", options=data_paths.keys(), default=data_paths.keys()
            )

        # Select features for X-axis, Y-axis, and color
        with st.sidebar.expander("Features (X axis)", expanded=True):
            # x axis
            select_x_category = st.selectbox(label="Feature category:", options=const_features.categories, index=0)
            available_features = [k for k, v in const_features.get_features(select_x_category).items() if v in data.columns]
            select_x_axis = st.selectbox(label="Feature name:", options=available_features, index=0)
            select_x_axis = const_features.get_features(select_x_category).get(select_x_axis, None)
        with st.sidebar.expander("Features (Y axis)", expanded=True):
            # y axis
            select_y_category = st.selectbox(label="Feature category (Y axis):", options=const_features.categories, index=0)
            available_features = [k for k, v in const_features.get_features(select_y_category).items() if v in data.columns]
            select_y_axis = st.selectbox(label="Feature name (X axis):", options=available_features, index=1)
            select_y_axis = const_features.get_features(select_y_category).get(select_y_axis, None)
        with st.sidebar.expander("Features color:", expanded=True):
            # color axis
            select_color_category = st.selectbox(label="Feature category (color):", options=["Dataset"] + const_features.categories, index=0)
            if select_color_category == "Dataset":
                select_color_axis = 'Dataset'
            else:
                available_features = [k for k, v in const_features.get_features(select_color_category).items() if v in data.columns]
                select_color_axis = st.selectbox(label="Color-axis variable:", options=available_features, index=0)
                select_color_axis = const_features.get_features(select_color_category).get(select_color_axis, None)

        return selected_sets, select_x_axis, select_y_axis, select_color_axis


# Main function for visualization and ITK-SNAP interaction
def main(data, x_axis, y_axis, color_axis):
    """
    Main function to load datasets, filter data, create scatter plots, and handle ITK-SNAP interaction.

    Args:
        data (pd.DataFrame): Dataset
        x_axis (str): Selected X-axis variable.
        y_axis (str): Selected Y-axis variable.
        color_axis (str): Selected color-axis variable.
    """
    # Scatter plot visualization
    st.markdown("**Click on a point to visualize it in ITK-SNAP app.**")
    data.reset_index(drop=True, inplace=True)

    with st.sidebar.expander(label="Highlight subject"):
        highlight_subject = st.selectbox(
            label="Enter patient ID to highlight", options=[None] + list(data.ID.unique()), index=0
        )

    fig = multivariate_features_highlighter(
        data=data,
        x_axis=x_axis,
        y_axis=y_axis,
        color=color_axis,
        highlight_point=highlight_subject,
    )
    selected_points = plotly_events(fig, click_event=True, override_height=None)

    # retrieving selected ID
    selected_case, st.session_state.selected_case = None, None
    if selected_points:
        try:
            point = selected_points[0]
            filtered_set_data = data[data.set == data.set.unique()[point["curveNumber"]]]
            selected_case = filtered_set_data.iloc[point["pointIndex"]]["ID"]
        except IndexError:
            selected_case = highlight_subject

    # Visualize case in ITK-SNAP
    if selected_case != st.session_state.selected_case:
        st.session_state.selected_case = selected_case
        dataset = data[data.ID == selected_case]["set"].unique()[0].lower()
        verification_check = run_itk_snap(datasets_root_path, dataset, selected_case, config.get("labels"))
        if not verification_check:
            st.error("Ups, something went wrong when opening the file in ITK-SNAP", icon="🚨")


def multivariate():
    # Define page layout
    st.header(const.header)
    st.markdown(const.sub_header)

    # Load datasets
    df = read_datasets_from_dict(features_information)

    # Sidebar setup
    selected_sets, select_x_feature_name, select_y_feature_name, select_color_feature_name = setup_sidebar(df, features_information)

    proceed = health_checks(selected_sets, [select_x_feature_name, select_y_feature_name, select_color_feature_name])
    if proceed[0]:

        df = processing_data(df, sets=selected_sets)

        main(df, select_x_feature_name, select_y_feature_name, select_color_feature_name)

        st.markdown(const.description)
    else:
        st.error(proceed[-1], icon='🚨')


