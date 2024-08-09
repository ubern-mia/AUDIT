import os
import streamlit as st
import numpy as np
from stqdm import stqdm

from src.commons.commons import load_config_file
from src.commons.commons import pretty_string
from src.commons.commons import snake_case
from src.commons.commons import run_comparison_segmentation_itk_snap
from src.commons.commons import all_capitals
from src.app.util.constants import SegmentationErrorMatrixPage
from src.commons.sequences import read_segmentation, read_prediction
from src.metrics.confusion_matrix import mistakes_per_class_optim
from src.metrics.confusion_matrix import normalize_matrix_per_row
from src.visualization.confusion_matrices import plt_confusion_matrix_plotly
from src.visualization.sequences import plot_seq

const = SegmentationErrorMatrixPage()

config = load_config_file("./src/app/util/config.yml").get("segmentation_error_analysis", {})
labels_dict = load_config_file("./src/app/util/config.yml").get('labels')
classes = list(labels_dict.keys())
labels = list(labels_dict.values())
datasets = list(config.keys())


def setup_sidebar(config, datasets):
    """
    Set up the sidebar configuration options.

    Args:
        config (dict): Configuration dictionary.
        datasets (list): List of available datasets.

    Returns:
        tuple: Selected dataset, model, patient ID, models, and patient paths.
    """
    with st.sidebar:
        st.header("Configuration")
        selected_dataset = st.selectbox("Select the dataset to analyze", datasets, index=0)
        models = config.get(selected_dataset)

        pretty_models = [all_capitals(pretty_string(m)) for m in models if m != "ground_truth"]
        patients_in_path = sorted([f.path.split("/")[-1] for f in os.scandir(config.get(selected_dataset)["ground_truth"]) if f.is_dir()])

        selected_model = st.selectbox("Select the model to analyze", pretty_models, index=0)
        selected_id = st.selectbox("Select the patient ID to visualize", ["All"] + patients_in_path, index=0)

        # visualize_slice = False
        # slice = None
        # if selected_id != "All":
        #     visualize_slice = st.checkbox("Visualize specific slice")
        #     if visualize_slice:
        #         slice = st.number_input("Select the slice to visualize", min_value=1, value=1)

        st.write(const.contact)
    return selected_dataset, selected_model, selected_id, models, patients_in_path


def visualize_patient_slices(t1, t2, flair, t1c, seg, pred, slice):
    """
    Visualize patient slices for different modalities and segmentation.

    Args:
        t1, t2, flair, t1c (np.array): Image sequences for different modalities.
        seg (np.array): Ground truth segmentation.
        pred (np.array): Predicted segmentation.
        slice (int): Slice number to visualize.
    """
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_seq(t1, "T1", slice), use_container_width=True)
        st.plotly_chart(plot_seq(t2, "T2", slice), use_container_width=True)
        st.plotly_chart(plot_seq(seg, "Ground Truth", slice), use_container_width=True)
    with col2:
        st.plotly_chart(plot_seq(t1c, "T1c", slice), use_container_width=True)
        st.plotly_chart(plot_seq(flair, "FLAIR", slice), use_container_width=True)
        st.plotly_chart(plot_seq(pred, "Prediction", slice), use_container_width=True)


def visualize_confusion_matrix(cm, classes, normalized):
    """
    Visualize the confusion matrix.

    Args:
        cm (np.array): Confusion matrix.
        classes (list): List of class labels.
        normalized (bool): Whether the confusion matrix is normalized.
    """
    fig = plt_confusion_matrix_plotly(cm, classes, normalized)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def compute_and_display_cm(seg, pred, labels, classes, normalized):
    """
    Compute and display the confusion matrix for a single patient.

    Args:
        seg (np.array): Ground truth segmentation.
        pred (np.array): Predicted segmentation.
        labels (list): List of label values.
        classes (list): List of class names.
        normalized (bool): Whether to normalize the confusion matrix.
    """
    cm = mistakes_per_class_optim(seg, pred, list(labels))
    if normalized:
        cm = normalize_matrix_per_row(cm)
    visualize_confusion_matrix(cm, classes, normalized)


def compute_accumulated_cm(patients_in_path, selected_dataset, models, selected_model, labels):
    """
    Compute the accumulated confusion matrix over all patients.

    Args:
        patients_in_path (list): List of patient paths.
        selected_dataset (str): Selected dataset name.
        models (dict): Dictionary of models.
        selected_model (str): Selected model name.
        labels (list): List of label values.

    Returns:
        np.array: Accumulated confusion matrix.
    """
    accumulated = None
    for p in stqdm(patients_in_path, desc=f"Calculating confusion matrix for {len(patients_in_path)} patients"):
        seg = read_segmentation(root=config.get(selected_dataset)["ground_truth"], patient_id=p)
        pred = read_prediction(root=models[snake_case(selected_model)], patient_id=p)
        cm = mistakes_per_class_optim(seg, pred, list(labels))
        if accumulated is None:
            accumulated = np.zeros_like(cm)
        accumulated += cm
    return accumulated


def main(selected_dataset, selected_model, selected_id, models, patients_in_path, labels, classes):
    """
    Main function to control the flow of the application.

    Args:
        selected_dataset (str): Selected dataset name.
        selected_model (str): Selected model name.
        selected_id (str): Selected patient ID.
        models (dict): Dictionary of models.
        patients_in_path (list): List of patient paths.
        labels (list): List of label values.
        classes (list): List of class names.
    """

    averaged = st.checkbox("Averaged per number of patients", value=True, help="It averages the errors per number of patients within the corresponding dataset, if enabled.")
    normalized = st.checkbox("Normalized per ground truth label", value=True, help="It normalizes the errors per class, if enabled.")
    if selected_id != "All":
        seg = read_segmentation(root=config.get(selected_dataset)["ground_truth"], patient_id=selected_id)
        pred = read_prediction(root=models[snake_case(selected_model)], patient_id=selected_id)
        compute_and_display_cm(seg, pred, labels, classes, normalized)
        st.session_state.selected_id = selected_id

        if "visualize_itk" not in st.session_state:
            st.session_state.visualize_itk = False
        visualize_itk = st.checkbox("Visualize it in ITK-SNAP", value=st.session_state.visualize_itk)
        if visualize_itk:
            verification_check = run_comparison_segmentation_itk_snap(config.get(selected_dataset)["ground_truth"],
                                                                      models[snake_case(selected_model)],
                                                                      selected_id, labels_dict)
            st.session_state.visualize_itk = False
            # st.experimental_rerun()
            # st.markdown(f"\nSelected slice {slice} from patient {selected_id}")
            # t1, t1c, t2, flair = read_sequences(root=config.get(selected_dataset)["ground_truth"], patient_id=selected_id)
            # visualize_patient_slices(t1, t2, flair, t1c, seg, pred, slice)
    else:
        accumulated = compute_accumulated_cm(patients_in_path, selected_dataset, models, selected_model, labels)
        if averaged:
            accumulated = (accumulated / len(patients_in_path)).astype(int)
        if normalized:
            accumulated = normalize_matrix_per_row(accumulated)
        visualize_confusion_matrix(accumulated, classes, normalized)


def matrix():
    st.subheader(const.header)
    st.markdown(const.sub_header)
    st.markdown(const.description)

    selected_dataset, selected_model, selected_id, models, patients_in_path = setup_sidebar(config, datasets)
    main(selected_dataset, selected_model, selected_id, models, patients_in_path, labels, classes)
