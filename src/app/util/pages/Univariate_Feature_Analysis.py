import streamlit as st
from streamlit_plotly_events import plotly_events

from src.app.util.constants import UnivariatePage
from src.commons.commons import load_config_file, read_datasets_from_dict, run_itk_snap
from src.visualization.boxplot import boxplot
from src.visualization.histograms import custom_histogram, custom_distplot

const = UnivariatePage()

# Load configuration and data
config = load_config_file("./src/app/util/config.yml")
datasets_root_path = config.get("datasets_root_path")
data_paths = config.get("distributions_analysis").get('data_paths')
allowed_features = UnivariatePage().mapping_buttons_columns


def filter_datasets(df, filtering_method, selected_sets, select_x_axis, remove_low, remove_up, clip_low, clip_up, num_std_devs):
    df = df[df.set.isin(selected_sets)]
    mean, std_dev = df[allowed_features.get(select_x_axis)].mean(), df[allowed_features.get(select_x_axis)].std()

    # Apply filtering
    if filtering_method == "Removing outliers":
        df = df[df[allowed_features.get(select_x_axis)].between(remove_low, remove_up)]
    elif filtering_method == "Clipping outliers":
        df[allowed_features.get(select_x_axis)] = df[allowed_features.get(select_x_axis)].clip(clip_low, clip_up)
    elif filtering_method == "Standard deviations":
        upper_bound = mean + int(num_std_devs) * std_dev
        lower_bound = mean - int(num_std_devs) * std_dev
        df = df[df[allowed_features.get(select_x_axis)].between(lower_bound, upper_bound)]

    return df


def setup_datasets_sidebar(data_paths):
    """
    Set up the sidebar for dataset selection and configuration.

    Args:
        data_paths (dict): Dictionary with paths to datasets.

    Returns:
        tuple: Selected datasets, x-axis feature, histogram parameters, and filtering options.
    """
    with st.sidebar:
        st.header("Configuration")
        with st.sidebar.expander("Datasets", expanded=True):
            selected_sets = st.multiselect(
                label="Select datasets to visualize:",
                options=data_paths.keys(),
                default=data_paths.keys()
            )
            select_x_axis = st.selectbox(
                label="X-axis variable:",
                options=allowed_features.keys(),
                index=0
            )

    return selected_sets, select_x_axis


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
                n_bins = st.number_input("Select the number of bins",
                                         min_value=1,
                                         max_value=200,
                                         value=100,
                                         step=1,
                                         placeholder="Type a number...")
            elif option == "Bins size":
                bins_size = st.number_input("Select bins size",
                                            min_value=1,
                                            max_value=None,
                                            value=1,
                                            step=1,
                                            placeholder="Type a number...")

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
            options=["None", "Removing outliers", "Clipping outliers", "Standard deviations"],
            captions=["",
                      "It remove values outside a specified range",
                      "It restricts the range of data by capping values below and above a threshold to the lower "
                      "and upper bound selected.",
                      "Filtering data based on standard deviations"])

        remove_low, remove_up = None, None
        clip_low, clip_up = None, None
        num_std_devs = None

        if filtering_method == "Removing outliers":
            remove_low, remove_up = st.slider("Remove outliers within a range of values",
                                              min_value=df[allowed_features.get(feature)].min(),
                                              max_value=df[allowed_features.get(feature)].max(),
                                              value=(df[allowed_features.get(feature)].min(),
                                                     df[allowed_features.get(feature)].max())
                                              )
        elif filtering_method == "Clipping outliers":
            clip_low, clip_up = st.slider("Clip outliers within a range of values",
                                          min_value=df[allowed_features.get(feature)].min(),
                                          max_value=df[allowed_features.get(feature)].max(),
                                          value=(df[allowed_features.get(feature)].min(),
                                                 df[allowed_features.get(feature)].max())
                                          )
        elif filtering_method == "Standard deviations":
            mean, std_dev = df[allowed_features.get(feature)].mean(), df[allowed_features.get(feature)].std()
            num_std_devs = st.number_input(label="Number of standard deviations",
                                           min_value=1,
                                           step=1,
                                           value=3
                                           )

    return filtering_method, remove_low, remove_up, clip_low, clip_up, num_std_devs


def main_plotting_logic(data, plot_type, select_x_axis, n_bins, bins_size):
    """
    Main function to handle plotting logic based on user selections.

    Args:
        data (DataFrame): DataFrame containing the data to visualize.
        plot_type (str): Type of plot ("Histogram" or "Probability").
        select_x_axis (str): Selected X-axis variable.
        n_bins (int): Number of bins for histogram.
        bins_size (int): Bin size for histogram.
        filtering_method (str): Method of filtering data.
        remove_low (float): Lower bound for removing outliers.
        remove_up (float): Upper bound for removing outliers.
        clip_low (float): Lower bound for clipping outliers.
        clip_up (float): Upper bound for clipping outliers.
        num_std_devs (int): Number of standard deviations for filtering.
    """

    # Plot visualization
    if plot_type == "Probability":
        fig = custom_distplot(data, x_axis=allowed_features.get(select_x_axis), color_var="set", histnorm='probability')
    else:
        if n_bins:
            fig = custom_histogram(data, x_axis=allowed_features[select_x_axis], color_var="set", n_bins=n_bins)
        elif bins_size:
            fig = custom_histogram(data, x_axis=allowed_features.get(select_x_axis), color_var="set",
                                   n_bins=None, bins_size=bins_size)
        else:
            st.write(":red[Please, select the number of bins or bins size]")

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.markdown(const.description)


def main_interactive_boxplot(datasets_root_path, data, select_x_axis, labels):
    """
    Function to handle interactive boxplot and ITK-SNAP integration.

    Args:
        data (DataFrame): DataFrame containing the data to visualize.
        select_x_axis (str): Selected X-axis variable.
    """
    st.markdown("**Click on a point to visualize it in ITK-SNAP app.**")
    data.reset_index(drop=True, inplace=True)
    boxplot_fig = boxplot(data, x_axis=allowed_features.get(select_x_axis), color_var="set")
    selected_points = plotly_events(boxplot_fig, click_event=True, override_height=None)

    # Handle selected point
    info_placeholder = st.empty()
    selected_case, st.session_state.selected_case = None, None
    if selected_points:
        point = selected_points[0]
        filtered_set_data = data[data.set == point['y']]
        selected_case = filtered_set_data.iloc[point['pointIndex']]["ID"]
        info_placeholder.write(f'Open ITK-SNAP for visualizing the case: {selected_case}')

    # Visualize case in ITK-SNAP
    if selected_case != st.session_state.selected_case:
        st.session_state.selected_case = selected_case
        if selected_case and selected_case != "Select a case":
            dataset = data[data.ID == selected_case]['set'].unique()[0].lower()

            verification_check = run_itk_snap(path=datasets_root_path, dataset=dataset, case=selected_case,
                                              labels=labels)
            if not verification_check:
                st.error('Ups, something wrong happened when opening the file in ITK-SNAP', icon="🚨")


def univariate():
    # Load configuration and data
    st.header(const.header)
    st.markdown(const.sub_header)

    # Select type of plot
    plot_type = st.selectbox(label="Type of plot to visualize", options=["Histogram", "Probability"], index=1)

    # Load datasets
    df = read_datasets_from_dict(data_paths)

    # Set up sidebar options
    selected_sets, select_x_axis = setup_datasets_sidebar(data_paths)
    n_bins, bins_size = setup_histogram_options(plot_type)
    filtering_method, remove_low, remove_up, clip_low, clip_up, num_std_devs = setup_filtering_options(df, select_x_axis)

    # filtering data
    df = filter_datasets(df, filtering_method, selected_sets, select_x_axis, remove_low, remove_up, clip_low, clip_up, num_std_devs)

    # Run main plotting logic
    main_plotting_logic(df, plot_type, select_x_axis, n_bins, bins_size)

    # Run interactive boxplot logic
    main_interactive_boxplot(datasets_root_path, df, select_x_axis, config.get("labels"))

