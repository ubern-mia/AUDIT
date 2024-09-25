import streamlit as st
from streamlit_plotly_events import plotly_events
import pandas as pd

from src.app.util.commons.data_preprocessing import processing_data
from src.app.util.commons.checks import health_checks
from src.app.util.constants_test.descriptions import UnivariatePage
from src.utils.operations.file_operations import load_config_file
from src.utils.operations.file_operations import read_datasets_from_dict
from src.utils.operations.itk_operations import run_itk_snap
from src.visualization.boxplot import boxplot_highlighter
from src.visualization.histograms import custom_distplot
from src.visualization.histograms import custom_histogram
from src.app.util.constants_test.features import Features

# Load constants
const = UnivariatePage()
const_features = Features()

# Load configuration and data
config = load_config_file("./src/configs/app.yml")
datasets_root_path = config.get("datasets_path")
data_paths = config.get("features")


def setup_datasets_sidebar(data, data_paths):
    """
    Set up the sidebar for dataset selection and configuration.

    Args:
        data (pd.DataFrame): Raw dataset
        data_paths (dict): Dictionary with paths to datasets.

    Returns:
        tuple: Selected datasets, x-axis feature, histogram parameters, and filtering options.
    """
    with st.sidebar:
        st.header("Configuration")
        with st.sidebar.expander("Datasets", expanded=True):
            selected_sets = st.multiselect(
                label="Select datasets to visualize:", options=data_paths.keys(), default=data_paths.keys()
            )
        with st.sidebar.expander("Features", expanded=True):
            select_category = st.selectbox(label="Feature category:", options=const_features.categories, index=0)

            available_features = [k for k, v in const_features.get_features(select_category).items() if v in data.columns]
            select_x_axis = st.selectbox(label="Feature name:", options=available_features, index=0)

    return selected_sets, select_category, select_x_axis


def setup_histogram_options(plot_type):
    """
    Set up histogram customization options based on plot type.

    Args:
        plot_type (str): Type of plot ("Histogram" or "Probability").

    Returns:
        tuple: Number of bins or bin size based on user selection.
    """
    n_bins, bins_size = None, None
    if plot_type == "Histogram":
        with st.sidebar.expander("Customization", expanded=True):
            option = st.selectbox("Define number of bins or bins size", ("Number of bins", "Bins size"))
            if option == "Number of bins":
                n_bins = st.number_input(
                    "Select the number of bins",
                    min_value=1,
                    max_value=200,
                    value=100,
                    step=1,
                    placeholder="Type a number...",
                    help="The actual number of bins will be the closest value to your selection based on distribution.",
                )
            elif option == "Bins size":
                bins_size = st.number_input(
                    "Select bins size", min_value=1, max_value=None, value=1, step=1, placeholder="Type a number..."
                )

    return n_bins, bins_size


def setup_filtering_options(df, feature):
    """
    Set up filtering options based on selected features.

    Args:
        df (DataFrame): DataFrame containing the data.
        feature (dict): Feature selected

    Returns:
        tuple: Filtering method and corresponding parameters.
    """
    with st.sidebar.expander("Filtering", expanded=False):
        filtering_method = st.radio(
            label="Filter data based on",
            options=["No filter", "Removing outliers", "Clipping outliers", "Standard deviations"],
            captions=[
                "",
                "It remove values outside a specified range",
                "It restricts the range of data by capping values below and above a threshold to the lower "
                "and upper bound selected.",
                "Filtering data based on standard deviations",
            ],
        )

        remove_low, remove_up = None, None
        clip_low, clip_up = None, None
        num_std_devs = None

        if filtering_method == "Removing outliers":
            remove_low, remove_up = st.slider(
                "Remove outliers within a range of values",
                min_value=df[feature].min(),
                max_value=df[feature].max(),
                value=(df[feature].min(), df[feature].max()),
            )
        elif filtering_method == "Clipping outliers":
            clip_low, clip_up = st.slider(
                "Clip outliers within a range of values",
                min_value=df[feature].min(),
                max_value=df[feature].max(),
                value=(df[feature].min(), df[feature].max()),
            )
        elif filtering_method == "Standard deviations":
            # mean, std_dev = df[feature].mean(), df[feature].std()
            num_std_devs = st.number_input(label="Number of standard deviations", min_value=1, step=1, value=3)

    return filtering_method, remove_low, remove_up, clip_low, clip_up, num_std_devs


def main_plotting_logic(data, plot_type, feature, n_bins, bins_size):
    """
    Main function to handle plotting logic based on user selections.

    Args:
        data (DataFrame): DataFrame containing the data to visualize.
        plot_type (str): Type of plot ("Histogram" or "Probability").
        select_x_axis (str): Selected X-axis variable.
        n_bins (int): Number of bins for histogram.
        bins_size (int): Bin size for histogram.
    """

    # Plot visualization
    if plot_type == "Probability":
        fig = custom_distplot(data, x_axis=feature, color_var="set", histnorm="probability")
    else:
        if n_bins:
            fig = custom_histogram(data, x_axis=feature, color_var="set", n_bins=n_bins)
        elif bins_size:
            fig = custom_histogram(
                data, x_axis=feature, color_var="set", n_bins=None, bins_size=bins_size
            )
        else:
            st.write(":red[Please, select the number of bins or bins size]",)

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.markdown(const.description)


def main_interactive_boxplot(datasets_root_path, data, feature, labels, plot_type, highlight_subject):
    """
    Function to handle interactive boxplot and ITK-SNAP integration.

    Args:
        data (DataFrame): DataFrame containing the data to visualize.
        select_x_axis (str): Selected X-axis variable.
    """
    st.markdown("**Click on a point to visualize it in ITK-SNAP app.**")

    boxplot_fig = boxplot_highlighter(
        data,
        x_axis=feature,
        color_var="set",
        plot_type=plot_type,
        highlight_point=highlight_subject,
    )
    selected_points = plotly_events(boxplot_fig, click_event=True, override_height=None)

    selected_case, st.session_state.selected_case = None, None

    # Handle selected point
    info_placeholder = st.empty()
    if (
        selected_points and len(selected_points) == 1
    ):  # last condition to avoid that clicking inside the boxplot randomly opens a patient
        point = selected_points[0]
        filtered_set_data = data[data.set == point["y"]]
        if point["curveNumber"] < len(data.set.unique()):
            selected_case = filtered_set_data.iloc[point["pointIndex"]]["ID"]
        else:  # to open the case highlighted when clicking on it
            selected_case = highlight_subject
        info_placeholder.write(f"Open ITK-SNAP for visualizing the case: {selected_case}")

    # Visualize case in ITK-SNAP
    if selected_case != st.session_state.selected_case:
        st.session_state.selected_case = selected_case
        if (
            selected_case and selected_case != "Select a case" and len(selected_points) == 1
        ):  # last condition to avoid that clicking inside the boxplot randomly opens a patient
            dataset = data[data.ID == selected_case]["set"].unique()[0]
            verification_check = run_itk_snap(
                path=datasets_root_path, dataset=dataset, case=selected_case, labels=labels
            )
            if not verification_check:
                st.error("Ups, something wrong happened when opening the file in ITK-SNAP", icon="🚨")


def main(data, select_feature_name):

    with st.sidebar.expander(label="Highlight subject"):
        highlight_subject = st.selectbox(
            label="Enter patient ID to highlight", options=[None] + list(data.ID.unique()), index=0
        )
    # Run interactive boxplot logic
    st.subheader("Boxplot")
    data.reset_index(drop=True, inplace=True)
    st.markdown(const.description_boxplot)
    plot_type = st.selectbox(label="Type of plot to visualize", options=["Box", "Violin"], index=0)
    main_interactive_boxplot(
        datasets_root_path, data, select_feature_name, config.get("labels"), plot_type, highlight_subject
    )

    # Run main plotting logic
    st.subheader("Continuous distribution")
    st.markdown(const.description_distribution)
    plot_type = st.selectbox(label="Type of plot to visualize", options=["Histogram", "Probability"], index=1)
    n_bins, bins_size = setup_histogram_options(plot_type)
    main_plotting_logic(data, plot_type, select_feature_name, n_bins, bins_size)


def univariate():
    # Load configuration and data
    st.header(const.header)
    st.markdown(const.sub_header)

    # Load datasets
    df = read_datasets_from_dict(data_paths)

    # Set up sidebar and plot options
    selected_sets, select_category, select_feature_name = setup_datasets_sidebar(df, data_paths)
    proceed = health_checks(selected_sets, [select_feature_name])
    if proceed[0]:
        select_feature_name = const_features.get_features(select_category).get(select_feature_name, None)
        filtering_method, remove_low, remove_up, clip_low, clip_up, num_std_devs = setup_filtering_options(
            df, select_feature_name
        )

        # filtering data
        df = processing_data(
            data=df,
            sets=selected_sets,
            filtering_method=filtering_method,
            filtering_feature=select_feature_name,
            remove_low=remove_low,
            remove_up=remove_up,
            clip_low=clip_low,
            clip_up=clip_up,
            num_std_devs=num_std_devs
        )

        main(df, select_feature_name)
    else:
        st.error(proceed[-1], icon='🚨')