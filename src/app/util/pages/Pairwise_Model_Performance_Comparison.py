import pandas as pd
import numpy as np
import streamlit as st

from src.visualization.barplots import individual_pairwise_model_performance, aggregated_pairwise_model_performance
from src.app.util.constants import PairwiseModelPerformanceComparisonPage
from src.commons.commons import load_config_file, pretty_string, read_datasets_from_dict, all_capitals, snake_case
from src.metrics.statistical_tests import wilcoxon_test, normality_test, paired_ttest
from src.metrics.commons import calculate_absolute_error
from src.metrics.commons import calculate_relative_error
from src.metrics.commons import calculate_ratio_improvement
from src.visualization.histograms import plot_histogram

const = PairwiseModelPerformanceComparisonPage()
mapping_buttons_metrics = const.mapping_buttons_metrics
mapping_buttons_columns = const.mapping_buttons_columns
mapping_order_by = const.mapping_order_by


def setup_sidebar(data, aggregated=True):
    """
    Set up the sidebar for user interaction.

    Parameters:
    - data: DataFrame containing the dataset.
    - aggregated: Boolean indicating if the data is aggregated.

    Returns:
    - selected_set: Selected dataset.
    - baseline_model: Selected baseline model.
    - new_model: Selected new model.
    - selected_metric: Selected metric.
    - num_max_patients: Number of maximum patients to visualize.
    - selected_sorted: Selected column to sort by.
    - selected_order: Order (ascending/descending) to sort by.
    """
    with st.sidebar:
        st.header("Configuration")

        # Select dataset
        with st.sidebar.expander("Datasets", expanded=True):
            sets_available = list(data.set.unique())
            selected_set = st.selectbox("Select dataset to analyze:", options=sets_available, index=0)

        # Select models
        with st.sidebar.expander("Models", expanded=True):
            models_available = [all_capitals(pretty_string(m)) for m in data[data.set == selected_set].model.unique()]
            baseline_model = st.selectbox("Select the model to take as a baseline:", options=models_available, index=0)
            new_model = st.selectbox("Select the new model:", options=models_available, index=1)
            if baseline_model == new_model:
                st.error('Models selected must be different to make a performance comparison', icon="🚨")

        # Select metric
        with st.sidebar.expander("Metrics", expanded=True):
            selected_metric = st.selectbox("Select metric to analyze:", options=mapping_buttons_metrics, index=0)

        # Customization options if not aggregated
        num_max_patients, selected_sorted, selected_order = None, None, None
        if not aggregated:
            with st.sidebar.expander("Customization", expanded=True):
                num_max_patients = st.number_input("Maximum patients to visualize", min_value=1, value=5, step=1)
                mapping_buttons_columns_perf = {**mapping_buttons_columns.copy(), **{f"Performance ({baseline_model})": f"Performance ({baseline_model})", f"Performance ({new_model})": f"Performance ({new_model})"}}
                selected_sorted = st.selectbox("Sorted by:", options=mapping_buttons_columns_perf)
                selected_order = st.radio("Order by:", options=mapping_order_by.keys())

    return selected_set, baseline_model, new_model, selected_metric, num_max_patients, selected_sorted, selected_order


def average_performance_calculation(raw_metrics, selected_metric, baseline_model, new_model):
    # Adding model performance
    mean_performance = raw_metrics.groupby(["ID", "set", "model"])[
        mapping_buttons_metrics[selected_metric]].mean().reset_index()
    mean_performance.rename(columns={mapping_buttons_metrics[selected_metric]: "performance"}, inplace=True)
    mean_performance = mean_performance[
        mean_performance.model.isin([snake_case(baseline_model), snake_case(new_model)])]

    # Pivoting the DataFrame
    mean_performance_wide = mean_performance.pivot_table(index=['ID', 'set'], columns='model',
                                                         values='performance').reset_index()
    # renaming columns
    mean_performance_wide.rename(columns={
        snake_case(baseline_model): f"Performance ({baseline_model})",
        snake_case(new_model): f"Performance ({new_model})"},
        inplace=True)

    return mean_performance_wide


def process_metrics(data, baseline_model="baseline", new_model="model_1", aggregate=False):
    """
    Process metrics to calculate relative differences.

    Parameters:
    - data: DataFrame containing the data.
    - baseline_model: Name of the baseline model.
    - new_model: Name of the new model.
    - aggregate: Boolean indicating if the data should be aggregated.

    Returns:
    - out: DataFrame containing the processed metrics with relative differences.
    """
    index_cols = ['ID', 'region', 'set']
    group_by_cols = ["ID", "region", "model", "set"]
    out_cols = ["ID", "region", "metric", "set", "relative", "absolute", "ratio"]

    if aggregate:
        data = data.drop(columns="ID").groupby(["region", "model", "set"]).mean().reset_index()
        index_cols.remove("ID")
        group_by_cols.remove("ID")

    metrics_cols = data.drop(columns=group_by_cols).columns
    post_processed_metrics = []

    for metric in metrics_cols:
        df_ = data[group_by_cols + [metric]]
        pivot_df = df_.pivot_table(index=index_cols, columns='model', values=metric).reset_index()
        pivot_df["relative"] = calculate_relative_error(pivot_df, snake_case(baseline_model), snake_case(new_model))
        pivot_df["absolute"] = calculate_absolute_error(pivot_df, snake_case(baseline_model), snake_case(new_model))
        pivot_df["ratio"] = calculate_ratio_improvement(pivot_df, snake_case(baseline_model), snake_case(new_model))

        if aggregate:
            totals = pivot_df.drop(columns="region").groupby('set').mean().reset_index()
            totals["region"] = "Average"
            pivot_df = pd.concat([pivot_df, totals])

        pivot_df['metric'] = metric
        post_processed_metrics.append(pivot_df)

    out = pd.concat(post_processed_metrics)
    if aggregate:
        out_cols.remove("ID")
    out = out[out_cols]

    return out


def run_functionality(data, selected_aggregated, selected_set, baseline_model, new_model, selected_metric, num_max_patients, selected_sorted, selected_order, improvement_type):
    # filters
    data = data[data['metric'] == mapping_buttons_metrics[selected_metric]]
    data = data[data['set'] == selected_set]
    data["gain"] = np.where(data[improvement_type] < 0, const.colorbar.get('decrease'), const.colorbar.get('increase'))

    if not selected_aggregated:
        # Order the data
        mapping_buttons_columns_perf = {**mapping_buttons_columns.copy(), **{f"Performance ({baseline_model})": f"Performance ({baseline_model})", f"Performance ({new_model})": f"Performance ({new_model})"}}
        data = data.sort_values(by=mapping_buttons_columns_perf[selected_sorted], ascending=mapping_order_by[selected_order])

        # Filter based on the number of patients
        if num_max_patients:
            data = data.head(num_max_patients * 3)

        # Clip metric
        with st.sidebar:
            metric_clip = st.checkbox("Clip the metric",
                                      help="It restricts the range of the metrics by capping values below and "
                                           "above a threshold to the lower and upper bound selected, if "
                                           "enabled.")
            if metric_clip:
                clip_low, clip_up = st.slider(label="Clip the metric",
                                              min_value=data[improvement_type].min(),
                                              max_value=data[improvement_type].max(),
                                              value=(data[improvement_type].min(), data[improvement_type].max()),
                                              label_visibility="collapsed"
                                              )
        if metric_clip:
            data[improvement_type] = data[improvement_type].clip(clip_low, clip_up)

    # plot
    if selected_aggregated:
        fig = aggregated_pairwise_model_performance(data, improvement_type)
        st.plotly_chart(fig, theme="streamlit", use_container_width=False, scrolling=True)
    else:
        st.dataframe(data)
        all_figures = individual_pairwise_model_performance(data, baseline_model, new_model, improvement_type)
        for fig in all_figures:
            st.plotly_chart(fig, theme="streamlit", use_container_width=False, scrolling=True)

    def perform_normality_test(df_for_stats_test, selected_set, selected_metric, baseline_model, new_model):
        col1, col2 = st.columns(2)
        df_wide = df_for_stats_test[df_for_stats_test.set == selected_set][
            ["ID", "model", mapping_buttons_metrics[selected_metric]]]
        df_wide = df_wide.pivot(index='ID', columns='model', values=mapping_buttons_metrics[selected_metric])

        sample_baseline_model = df_wide[snake_case(baseline_model)]
        sample_new_model = df_wide[snake_case(new_model)]

        with col1:
            # checking normality baseline model
            normality_test_baseline_model = normality_test(sample_baseline_model)
            st.table(
                pd.DataFrame(normality_test_baseline_model.items(), columns=["Metric", "Baseline model"]).set_index(
                    "Metric"))
            fig = plot_histogram(data=df_wide[[snake_case(baseline_model)]],
                                 x_axis=snake_case(baseline_model), color_var=None, n_bins=None, x_label=baseline_model)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True, scrolling=True)
        with col2:
            # checking normality new model
            normality_test_new_model = normality_test(sample_new_model)
            st.table(
                pd.DataFrame(normality_test_new_model.items(), columns=["Metric", "New model"]).set_index("Metric"))
            fig = plot_histogram(data=df_wide[[snake_case(new_model)]],
                                 x_axis=snake_case(new_model), color_var=None, n_bins=None, x_label=new_model)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True, scrolling=True)

        return normality_test_baseline_model, normality_test_new_model


def perform_normality_test(df_for_stats_test, selected_set, selected_metric, baseline_model, new_model):
    col1, col2 = st.columns(2)
    df_wide = df_for_stats_test[df_for_stats_test.set == selected_set][
        ["ID", "model", mapping_buttons_metrics[selected_metric]]]
    df_wide = df_wide.pivot(index='ID', columns='model', values=mapping_buttons_metrics[selected_metric])

    sample_baseline_model = df_wide[snake_case(baseline_model)]
    sample_new_model = df_wide[snake_case(new_model)]

    with col1:
        # checking normality baseline model
        normality_test_baseline_model = normality_test(sample_baseline_model)
        st.table(
            pd.DataFrame(normality_test_baseline_model.items(), columns=["Metric", "Baseline model"]).set_index(
                "Metric"))
        fig = plot_histogram(data=df_wide[[snake_case(baseline_model)]],
                             x_axis=snake_case(baseline_model), color_var=None, n_bins=10, x_label=baseline_model)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True, scrolling=True)
    with col2:
        # checking normality new model
        normality_test_new_model = normality_test(sample_new_model)
        st.table(
            pd.DataFrame(normality_test_new_model.items(), columns=["Metric", "New model"]).set_index("Metric"))
        fig = plot_histogram(data=df_wide[[snake_case(new_model)]],
                             x_axis=snake_case(new_model), color_var=None, n_bins=10, x_label=new_model)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True, scrolling=True)

    return sample_baseline_model, sample_new_model, normality_test_baseline_model, normality_test_new_model


def perform_statistical_test(normality_test_baseline_model, normality_test_new_model, sample_baseline_model, sample_new_model):
    """
    Perform statistical test to evaluate differences in model performance.

    Parameters:
    - df_for_stats_test: DataFrame for statistical test.
    - selected_set: Selected dataset.
    - selected_metric: Selected metric.
    - baseline_model: Baseline model.
    - new_model: New model.
    """

    if normality_test_baseline_model["Normally distributed"] and normality_test_new_model["Normally distributed"]:
        st.markdown("""Both the baseline model sample and the new model sample follow a normal distribution. 
        Therefore, the **Paired Student t-test** will be performed. This is a parametric test that compares two 
        **paired samples** normally distributed.""")

        statistical_diff = paired_ttest(sample1=sample_baseline_model, sample2=sample_new_model)
    else:
        st.markdown("""
        Either the baseline model sample or the new model sample does not follow a normal distribution. 
        Therefore, the **Wilcoxon signed-rank test** will be used. This is a non-parametric test that compares two 
        **paired samples** when normality cannot be assumed.
        """)

        statistical_diff = wilcoxon_test(sample1=sample_baseline_model, sample2=sample_new_model)

    # Convert the result to a DataFrame for better table display
    # result_df = pd.DataFrame(wt.items(), columns=["Metric", "Value"])
    # # st.table(result_df.set_index("Metric"))
    st.markdown(f":red[**Results:**] The p-value obtained from the test was {statistical_diff.get('p-value'): .4e}. "
                f"{statistical_diff.get('interpretation')}")


def pairwise_comparison():

    # Defining page
    st.subheader(const.header)
    st.markdown(const.sub_header)
    show_descriptions = st.toggle("Show formulas")
    if show_descriptions:
        st.markdown(const.description)
        st.latex(const.absolute_formula)
        st.latex(const.relative_formula)
        st.latex(const.ratio_formula)

    # Load configuration files
    config = load_config_file("./src/app/util/config.yml").get("model_performance_comparison")
    metrics_data_paths = config.get("metrics")
    features_data_paths = config.get("features")

    # Load datasets
    raw_metrics = read_datasets_from_dict(metrics_data_paths)
    raw_features = read_datasets_from_dict(features_data_paths)[['set'] + list(mapping_buttons_columns.values())]
    df_for_stats_test = raw_metrics.drop(columns='region').groupby(["ID", "model", "set"]).mean().reset_index()

    # type of improvement
    improvement_type = st.selectbox(label="Type of comparison",
                                    options=["relative", "absolute", "ratio"],
                                    format_func=pretty_string,
                                    index=0)

    # Aggregation option
    selected_aggregated = st.checkbox("Aggregated.", value=True, help="It aggregates all the patients, if enabled.")

    # Setup sidebar
    selected_set, baseline_model, new_model, selected_metric, num_max_patients, selected_sorted, selected_order = setup_sidebar(raw_metrics, selected_aggregated)

    # Process metrics if models are different
    if baseline_model != new_model:
        df = process_metrics(data=raw_metrics,
                             baseline_model=baseline_model,
                             new_model=new_model,
                             aggregate=selected_aggregated
                             )

        # Merge with features and average performance if not aggregated
        if not selected_aggregated:
            df = df.merge(raw_features, on=['ID', 'set'])

            mean_performance = average_performance_calculation(raw_metrics, selected_metric, baseline_model, new_model)
            df = df.merge(mean_performance, on=['ID', 'set'])

        # calling the main functionality
        run_functionality(df, selected_aggregated, selected_set, baseline_model, new_model, selected_metric, num_max_patients, selected_sorted, selected_order, improvement_type)

        # Perform statistical test
        if selected_aggregated:
            statistical_test = st.checkbox(label="Perform statistical test",
                                           help="It performs statistical tests to evaluate whether exist statistical "
                                                "differences between the model performance, if enabled."
                                           )
            if statistical_test:
                st.markdown("""**Performing normality test:**""")
                sample_bm, sample_nm, nt_baseline_model, nt_new_model = perform_normality_test(df_for_stats_test, selected_set, selected_metric, baseline_model, new_model)

                st.markdown("""**Performing statistical test:**""")
                perform_statistical_test(nt_baseline_model, nt_new_model, sample_bm, sample_nm)

                # download the data used for the statistical tests
                @st.cache_data
                def convert_df(df):
                    # IMPORTANT: Cache the conversion to prevent computation on every rerun
                    return df.to_csv().encode("utf-8")

                statistical_csv = convert_df(df_for_stats_test)

                st.download_button(
                    label="Download data used in the statistical tests as CSV",
                    data=statistical_csv,
                    file_name="raw_data_statistical_test.csv",
                    mime="text/csv",
                )