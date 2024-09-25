import pandas as pd
import streamlit as st

from src.app.util.constants_test.descriptions import MultiModelPerformanceComparisonsPage
from src.utils.operations.file_operations import load_config_file
from src.utils.operations.file_operations import read_datasets_from_dict
from src.utils.operations.misc_operations import capitalizer
from src.utils.operations.misc_operations import pretty_string
from src.utils.operations.misc_operations import snake_case
from src.visualization.boxplot import models_performance_boxplot

const = MultiModelPerformanceComparisonsPage()
mapping_buttons_metrics = const.mapping_buttons_metrics
mapping_buttons_columns = const.mapping_buttons_columns

# load config files
config = load_config_file("./src/configs/app.yml")
metrics_data_paths = config.get("metrics")
features_data_paths = config.get("features")
metrics_available = const.mapping_buttons_metrics.keys()


def setup_sidebar(data):
    # left sidebar
    with st.sidebar:
        st.header("Configuration")

        # select dataset
        with st.sidebar.expander("Datasets", expanded=True):
            sets_available = list(data.set.unique())
            selected_set = st.selectbox(label="Select dataset to analyze:", options=sets_available, index=0)

        # select model
        with st.sidebar.expander("Models", expanded=True):
            models_available = [capitalizer(pretty_string(m)) for m in list(data.model.unique())]
            selected_models = st.multiselect(
                label="Select the models to compare:", options=models_available, default=models_available
            )
        # select region
        with st.sidebar.expander("Regions", expanded=True):
            regions_available = list(data.region.unique())
            selected_regions = st.multiselect(
                label="Select the region to visualize:", options=regions_available, default=regions_available
            )
        # select metrics
        with st.sidebar.expander("Metrics", expanded=True):
            # metrics_available = list(data_melted.metric.unique())
            selected_metrics = st.multiselect(
                label="Select the metrics to compare:", options=metrics_available, default="Dice"
            )
            selected_metrics = [mapping_buttons_metrics[m] for m in selected_metrics]
        # contact
        st.write(const.contact)

    return selected_set, selected_models, selected_regions, selected_metrics


def main(data, selected_set, selected_models, selected_regions, selected_metrics):
    # filters
    data = data[data["set"] == selected_set]
    data = data[data["model"].isin([snake_case(m) for m in selected_models])]
    data["model"] = data["model"].apply(pretty_string).apply(capitalizer)
    data = data[data["region"].isin(selected_regions)]

    # reshape the dataset
    data_melted = pd.melt(
        data,
        id_vars=["model", "region"],
        var_name="metric",
        value_name="score",
        value_vars=[mapping_buttons_metrics[m] for m in metrics_available],
    )
    data_melted = data_melted[data_melted["metric"].isin(selected_metrics)]

    # whether aggregating the results or not
    selected_aggregated = st.checkbox("Aggregated.", value=True, help="It aggregates all the regions, if enabled.")

    # general results
    if not selected_aggregated:
        aggregated = data.drop(columns=["ID", "set"]).groupby(["region", "model"]).agg(["mean", "std"])
    else:
        aggregated = data.drop(columns=["ID", "set", "region"]).groupby(["model"]).agg(["mean", "std"])
    formatted = pd.DataFrame(index=aggregated.index)

    # st.table(aggregated.groupby("model").mean().reset_index())
    for metric in selected_metrics:
        formatted[metric] = aggregated[metric].apply(lambda x: f"{x['mean']:.3f} ± {x['std']:.3f}", axis=1)
    st.dataframe(formatted, use_container_width=True)

    # Show the plot
    st.markdown(const.description)
    fig = models_performance_boxplot(data_melted, aggregated=selected_aggregated)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def multi_model():

    # Defining page
    st.subheader(const.header)
    st.markdown(const.sub_header)

    raw_metrics = read_datasets_from_dict(metrics_data_paths)

    # calling main function
    selected_set, selected_models, selected_regions, selected_metrics = setup_sidebar(raw_metrics)
    main(raw_metrics, selected_set, selected_models, selected_regions, selected_metrics)
