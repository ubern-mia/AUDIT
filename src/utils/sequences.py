import SimpleITK
import numpy as np
import os
from SimpleITK import GetArrayFromImage, GetImageFromArray, ReadImage, WriteImage

# TODO: check whether the following two functions can be unified
def load_subject_nii(root, patient_id, seq):
    return ReadImage(str(f"{root}/{patient_id}/{patient_id}_{seq}.nii.gz"))


def load_nii(path_folder: str) -> SimpleITK.Image:
    """  This function loads a NIfTI."""

    return ReadImage(str(path_folder))


def load_nii_as_array(path_folder: str) -> np.ndarray:
    """  This function loads a NIfTI image as a NumPy array."""

    return GetArrayFromImage(ReadImage(str(path_folder)))


def read_sequences(root, patient_id):
    t1_path = f"{root}/{patient_id}/{patient_id}_t1.nii.gz"
    t1c_path = f"{root}/{patient_id}/{patient_id}_t1ce.nii.gz"
    t2_path = f"{root}/{patient_id}/{patient_id}_t2.nii.gz"
    flair_path = f"{root}/{patient_id}/{patient_id}_flair.nii.gz"

    t1 = load_nii_as_array(t1_path) if os.path.exists(t1_path) else None
    t1c = load_nii_as_array(t1c_path) if os.path.exists(t1c_path) else None
    t2 = load_nii_as_array(t2_path) if os.path.exists(t2_path) else None
    flair = load_nii_as_array(flair_path) if os.path.exists(flair_path) else None

    return t1, t1c, t2, flair


def read_sequences_dict(root, patient_id):
    sequences = {}

    # TODO: check what if any of the sequences are not within the dataset
    t1_path = f"{root}/{patient_id}/{patient_id}_t1.nii.gz"
    t1c_path = f"{root}/{patient_id}/{patient_id}_t1c.nii.gz"
    t1ce_path = f"{root}/{patient_id}/{patient_id}_t1ce.nii.gz"
    t2_path = f"{root}/{patient_id}/{patient_id}_t2.nii.gz"
    flair_path = f"{root}/{patient_id}/{patient_id}_flair.nii.gz"

    if os.path.exists(t1_path):
        sequences['t1'] = load_nii_as_array(t1_path)
    if os.path.exists(t1c_path):
        sequences['t1c'] = load_nii_as_array(t1c_path)
    if os.path.exists(t1ce_path):
        sequences['t1c'] = load_nii_as_array(t1ce_path)
    if os.path.exists(t2_path):
        sequences['t2'] = load_nii_as_array(t2_path)
    if os.path.exists(flair_path):
        sequences['flair'] = load_nii_as_array(flair_path)

    return sequences


def read_segmentation(root, patient_id):

    seg = load_nii_as_array(f"{root}/{patient_id}/{patient_id}_seg.nii.gz")

    return seg


def read_prediction(root, patient_id):
    # TODO: Remove the if-else condition when the naming convention is standardized
    if os.path.exists(f"{root}/{patient_id}_pred.nii.gz"):
        path_prediction = f"{root}/{patient_id}_pred.nii.gz"
    else:
        path_prediction = f"{root}/{patient_id}/{patient_id}_pred.nii.gz"

    pred = load_nii_as_array(path_prediction)

    return pred


def get_spacing(img):
    return np.array(img.GetSpacing())


def build_nifty_image(segmentation):
    img = GetImageFromArray(segmentation)
    return img


def label_replacement(segmentation: np.array, original_labels: list, new_labels: list) -> np.array:
    """
    Maps the values in a segmentation array from original labels to desired new labels.

    Args:
        segmentation: The segmentation array containing the original label values.
        original_labels: A list of original labels present in the segmentation array.
        new_labels: A list of new labels that will replace the original labels.

    Returns:
        post_seg: A new segmentation array where the original labels have been mapped to the new labels.

    """

    # Create a mapping dictionary from original labels to new labels
    mapping = {orig: new for orig, new in zip(original_labels, new_labels)}

    # Vectorized approach: Create a copy of the segmentation array
    post_seg = np.copy(segmentation)

    # Apply the mapping to the entire 3D array
    for orig, new in mapping.items():
        post_seg[segmentation == orig] = new

    return post_seg


def iterative_labels_replacement(root_dir: str, original_labels: list, new_labels: list, ext="_seg"):
    """
    Iteratively replaces labels in segmentation files within a directory and its subdirectories.

    This function walks through all files in a specified root directory and its subdirectories,
    identifies files containing a specified extension (e.g., "_seg" or "_pred"), loads each file as a 3D image array,
    replaces the labels based on provided mappings, and saves the modified image back to its original location.

    Args:
        root_dir: The root directory containing the segmentation files.
        original_labels: A list of original labels present in the segmentation arrays.
        new_labels: A list of new labels that will replace the original labels.
        ext: The file extension pattern to identify segmentation files. Defaults to "_seg".
    """

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            # Skip files that do not match the extension criteria
            if ext not in file:
                continue

            file_path = str(os.path.join(subdir, file))

            # Load the segmentation file as a 3D array
            seg = load_nii_as_array(file_path)

            # Perform label replacement
            post_seg = label_replacement(seg, original_labels, new_labels)

            # Save the modified segmentation array back to file
            WriteImage(build_nifty_image(post_seg), file_path)

            print(f"Processed file {file}")


def turn_planes(image, orientation=None):
    """
    Reorients the image planes based on the provided orientation.

    Parameters:
    ----------
    orientation : list, optional
        A list representing the desired plane orientations in order (default is ["axial", "coronal", "sagittal"]).

    Returns:
    -------
    np.ndarray
        The reoriented image array.
    """

    if not orientation:
        orientation = ["axial", "coronal", "sagittal"]

    # Get index position for each plane
    axial = orientation.index("axial")
    coronal = orientation.index("coronal")
    sagittal = orientation.index("sagittal")

    return np.transpose(image, (axial, coronal, sagittal))


def count_labels(segmentation, mapping_names=None):
    """
    Counts the number of pixels for each unique value in the segmentation.

    Returns:
    -------
    dict
        A dictionary with the counts of each unique value in the segmentation.
    """
    unique, counts = np.unique(segmentation, return_counts=True)
    pixels_dict = dict(zip(unique, counts))

    if mapping_names:
        pixels_dict = {mapping_names.get(k, k).lower(): v for k, v in pixels_dict.items()}

    return pixels_dict
