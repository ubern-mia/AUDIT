import numpy as np
import SimpleITK as sitk
from radiomics import featureextractor
from skimage.feature import graycomatrix
from skimage.feature import graycoprops


# TODO: create a class as the others
def compute_texture_values(image_array, texture="contrast"):
    """
    Compute the contrast values for each 2D plane in a 3D image array.

    Parameters:
    image_array (np.array): A 3D numpy array representing the MRI image.

    Returns:
    np.array: An array of contrast values for each 2D plane in the image.
    """

    # Normalize the image to values between 0 and 255
    image_array = (255 * (image_array - np.min(image_array)) / (np.max(image_array) - np.min(image_array))).astype(
        np.uint8
    )

    # Define distances and angles for GLCM calculation
    distances = [1]
    angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]

    # Initialize a list to store the contrast for each plane
    contrast_values = []

    # Iterate over each 2D plane in the Z dimension
    for z in range(image_array.shape[0]):
        plane = image_array[z, :, :]

        # Compute GLCM for the current plane
        glcm = graycomatrix(plane, distances=distances, angles=angles, levels=256, symmetric=True, normed=True)

        # Compute contrast using skimage.feature.graycoprops
        contrast = graycoprops(glcm, prop=texture).mean()

        # Store the contrast of the current plane
        contrast_values.append(contrast)

    return np.array(contrast_values)


# Function to extract radiomics features using PyRadiomics
# TODO: Check whether to remove method or keep it and don't use it
def extract_radiomics_features(image_path):
    """
    Extract radiomics features from a medical image without using a segmentation mask.

    Parameters:
    image_path (str): Path to the input medical image (e.g., MRI).

    Returns:
    dict: Dictionary containing extracted radiomics features.
    """
    # Initialize PyRadiomics feature extractor
    extractor = featureextractor.RadiomicsFeatureExtractor()

    # Load the image using SimpleITK
    image = sitk.ReadImage(image_path)

    # Create a dummy mask that covers the entire image
    mask = sitk.GetImageFromArray(np.ones(sitk.GetArrayFromImage(image).shape, dtype=np.uint8))
    mask.CopyInformation(image)

    # Ensure image has the correct spacing
    image.SetSpacing((1.0, 1.0, 1.0))
    mask.SetSpacing((1.0, 1.0, 1.0))

    # Extract features
    result = extractor.execute(image, mask)

    # Return extracted features
    return result
