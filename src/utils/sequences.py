import os
from loguru import logger

import numpy as np
import SimpleITK
from SimpleITK import GetArrayFromImage
from SimpleITK import GetImageFromArray
from SimpleITK import ReadImage
from SimpleITK import WriteImage


def load_nii(path_folder: str, as_array: bool = False) -> SimpleITK.Image:
    """  This function loads a NIfTI."""
    try:
        if as_array:
            return GetArrayFromImage(ReadImage(str(path_folder)))
        else:
            return ReadImage(str(path_folder))
    except RuntimeError:
        return None


def load_nii_by_id(root: str, patient_id: str, seq: str = "_seg", as_array: bool = False):
    """  This function loads a specific sequence from a NIfTI file by subject ID."""

    nii_path = f"{root}/{patient_id}/{patient_id}{seq}.nii.gz"
    if not os.path.exists(nii_path):
        logger.warning(f" Sequence '{seq}' not found.")
        return None

    try:
        if as_array:
            return GetArrayFromImage(ReadImage(nii_path))
        else:
            return ReadImage(f"{root}/{patient_id}/{patient_id}{seq}.nii.gz")
    except RuntimeError:
        return None


def read_sequences_dict(root, patient_id, sequences=["_t1", "_t1ce", "_t2", "_flair"]):
    out = {}

    for seq in sequences:
        nii_path = f"{root}/{patient_id}/{patient_id}{seq}.nii.gz"

        # load the sequence if it exists
        if os.path.exists(nii_path):
            out[seq.replace("_", "")] = load_nii(nii_path, as_array=True)
        else:
            out[seq.replace("_", "")] = None
            logger.warning(f" Sequence '{seq}' not found.")

    return out


def get_spacing(img):
    if img is not None:
        return np.array(img.GetSpacing())
    else:
        logger.warning(f" Sequence empty. Assuming isotropic spacing (1, 1, 1).")
        return np.array([1, 1, 1])


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


def iterative_labels_replacement(
        root_dir: str,
        original_labels: list,
        new_labels: list,
        ext="_seg",
        verbose: bool = False
):
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
            seg = load_nii(file_path, as_array=True)

            # Perform label replacement
            post_seg = label_replacement(seg, original_labels, new_labels)

            # Save the modified segmentation array back to file
            WriteImage(build_nifty_image(post_seg), file_path)

            if verbose:
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


def fit_brain_boundaries(sequence: np.ndarray):
    sequence = sequence.copy()

    # Getting all non-xero indexes
    z_indexes, y_indexes, x_indexes = np.nonzero(sequence != 0)

    # Calculating lower and upper boundaries by each dimension. Add a extra pixel in each dimension
    zmin, ymin, xmin = [max(0, int(np.min(idx))) for idx in (z_indexes, y_indexes, x_indexes)]
    zmax, ymax, xmax = [int(np.max(arr)) for arr in (z_indexes, y_indexes, x_indexes)]

    # Fitting sequences and segmentation to brain boundaries
    sequence = sequence[zmin:zmax, ymin:ymax, xmin:xmax]

    return sequence
