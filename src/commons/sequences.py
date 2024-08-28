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

# TODO: Optimize this function to be able to use it.
def replace_labels(root_dir, input_labels=1, output_labels=2):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            file_path = str(os.path.join(subdir, file))

            # load image
            img = load_nii(file_path)

            # replace labels
            if input_labels is not None and output_labels is not None:
                img[img == input_labels] = -1
                img[img == output_labels] = input_labels
                img[img == -1] = output_labels

            # save image
            WriteImage(build_nifty_image(img), file_path)


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
