import pandas as pd
import streamlit as st

from src.app.util.constants_test.descriptions import SubjectsExploration
from src.utils.operations.file_operations import load_config_file
from src.utils.operations.file_operations import read_datasets_from_dict
from src.utils.operations.misc_operations import pretty_string

const = SubjectsExploration()

# Load configuration and data
config = load_config_file("./src/configs/app.yml")
data_paths = config.get("features")


# allowed_features = SubjectsExploration().mapping_buttons_columns


def setup_sidebar(data):
    """
    Set up the sidebar for dataset selection and configuration.

    Args:
        df (dict): Dictionary with paths to datasets.

    Returns:
        tuple: Selected datasets, x-axis feature, histogram parameters, and filtering options.
    """
    with st.sidebar:
        st.header("Configuration")
        with st.sidebar.expander("Datasets", expanded=True):
            selected_set = st.selectbox(label="Select dataset:", options=data.set.unique(), index=0)
        with st.sidebar.expander("Subjects", expanded=True):
            # Select type of plot
            selected_subject = st.selectbox(
                label="Select a patient to explore", options=data[data.set == selected_set].ID.unique(), index=0
            )

    return selected_set, selected_subject


def show_subject_information(data):
    temp = data.copy().transpose().reset_index()
    temp.columns = ["feature", "value"]
    temp["feature_type"] = temp.feature.map(const.mapping_feature_types)
    temp["feature"] = temp.feature.map(pretty_string)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### Anatomical features")
        st.dataframe(
            temp[temp["feature_type"] == "anatomical"].drop(columns=["feature_type"]).set_index("feature"),
            use_container_width=True,
        )

    with col2:
        st.markdown("#### Statistical features")
        st.dataframe(
            temp[temp["feature_type"] == "statistical"].drop(columns=["feature_type"]).set_index("feature"),
            use_container_width=True,
        )

    with col3:
        st.markdown("#### Texture features")
        st.dataframe(
            temp[temp["feature_type"] == "texture"].drop(columns=["feature_type"]).set_index("feature"),
            use_container_width=True,
        )


def iqr_outliers_detector(data, subject, deviation=1.5):
    outliers_iqr = {}
    for c in data.columns:
        if c in const.mapping_feature_types.keys():
            Q1 = data[c].quantile(0.25)
            Q3 = data[c].quantile(0.75)
            IQR = Q3 - Q1
            outliers_iqr[c] = (subject[c].values[0] < (Q1 - deviation * IQR)) or (
                subject[c].values[0] > (Q3 + deviation * IQR)
            )

    median = [f"{data[c].median():.2f}" for c in outliers_iqr.keys()]
    mean_std_combined = [f"{data[c].mean():.2f} ± {data[c].std():.2f}" for c in outliers_iqr.keys()]

    outliers_df = pd.DataFrame(
        {
            "Feature": list(outliers_iqr.keys()),
            "Is Outlier": list(outliers_iqr.values()),
            # 'Mean (Dataset)': [data[c].mean() for c in outliers_iqr.keys()],
            # 'Std Dev (Dataset)': [data[c].std() for c in outliers_iqr.keys()],
            "Median (Dataset)": median,
            "Mean ± Std (Dataset)": mean_std_combined,
            "Subject": [f"{subject[c].values[0]:.2f}" for c in outliers_iqr.keys()],
        }
    )

    outliers_df["Feature"] = outliers_df.Feature.map(pretty_string)
    outliers_df = outliers_df.set_index("Feature")

    return outliers_df


def subjects():
    # Load configuration and data
    st.header(const.header)
    st.markdown(const.sub_header)

    # Load datasets
    df = read_datasets_from_dict(data_paths)
    # Set up sidebar options
    selected_set, selected_subject = setup_sidebar(df)

    # Filter subject info and remove the subject from the dataset for further analysis
    subject_data = df[(df.set == selected_set) & (df.ID == selected_subject)]
    df = df[(df.set == selected_set) & (df.ID != selected_subject)]

    # show main information for the selected patient
    st.subheader("Subject information")
    st.markdown("This section provides information of the chosen subject.")
    st.markdown("""
        - Anatomical features refer to the structural characteristics of biological entities. This category includes
        details about the physical structure, shape, size, and spatial arrangement of tumors.

        - Statistical features involve numerical attributes derived from MRI quantitative measurements. These features
         are used to describe the distribution, variability, etc.

        - Texture features describe patterns and variations within an MRI. These features capture details about the
        surface characteristics, smoothness, roughness, that are visually discernible but not necessarily related to
        intensity.
        """)

    show_subject_information(subject_data)

    # check whether the subject is an outlier or not
    st.subheader("IQR outlier detection")
    st.markdown(
        "The Interquartile Range (IQR) method for outlier detection is a statistical technique used to identify "
        "outliers in a dataset. It relies on the spread of the middle 50% of the data, providing a robust measure "
        "of variability that is not influenced by extreme values. The IQR method is a non-parametric technique "
        "suitable for a variety of data distributions, including normal, skewed, and even data with heavy "
        "tails. It does not rely on the assumption of normality, making it a versatile and robust choice for outlier "
        "detection in many scenario"
    )
    extreme = st.checkbox("Extreme outlier", value=False, help="If enabled, it looks for extreme outlier values.")
    deviation = 3 if extreme else 1.5
    outliers = iqr_outliers_detector(df, subject_data, deviation=deviation)
    if any(outliers["Is Outlier"]) > 0:
        st.write(outliers[outliers["Is Outlier"] == True].drop(columns=["Is Outlier"]))
    else:
        st.write("The subject is not an outlier for any of the features")
