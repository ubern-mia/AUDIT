from collections import Counter

import numpy as np
from scipy.spatial.distance import euclidean

from src.utils.operations.misc_operations import add_prefix_dict


class TumorFeatures:
    """
    A class to compute tumor features from given medical segmentation.

    Attributes:
    ----------
    segmentation : np.ndarray
        A numpy array representing the segmentation of the medical image.
    spacing : tuple, optional
        A tuple representing the voxel spacing of the image.
    mapping_names : dict, optional
        A dictionary to map segmentation values to names.

    Methods:
    -------
    count_tumor_pixels():
        Counts the number of pixels for each unique value in the segmentation.

    calculate_lesion_size():
        Calculates the lesion size in the segmentation.

    calculate_tumor_center_mass(label=None):
        Calculates the center of mass for the tumor in the image.

    get_tumor_slices():
        Gets the slices that contain tumor regions in axial, coronal, and sagittal planes.
    """

    def __init__(self, segmentation, spacing=(1, 1, 1), mapping_names=None, planes=None):
        """
        Constructs all the necessary attributes for the TumorAnalysis object.

        Parameters:
        ----------
        segmentation : np.ndarray
            A numpy array representing the segmentation of the medical image.
        image : np.ndarray, optional
            A numpy array representing the medical image.
        spacing : tuple, optional
            A tuple representing the voxel spacing of the image (default is (1, 1, 1)).
        mapping_names : dict, optional
            A dictionary to map segmentation values to names.
        """
        self.center_mass_dict = None
        self.lesion_size = None
        self.tumor_location = None
        self.number_pixels = None
        self.tumor_slices = None
        self.segmentation = segmentation
        self.spacing = spacing
        self.mapping_names = mapping_names
        self.planes = planes if planes is not None else ["axial", "coronal", "sagittal"]

    def count_tumor_pixels(self):
        """
        Counts the number of pixels for each unique value in the segmentation.

        Returns:
        -------
        dict
            A dictionary with the counts of each unique value in the segmentation.
        """
        unique, counts = np.unique(self.segmentation, return_counts=True)
        pixels_dict = dict(zip(unique, counts))

        if self.mapping_names:
            pixels_dict = {self.mapping_names.get(k, k).lower(): v for k, v in pixels_dict.items()}

        return pixels_dict

    def calculate_lesion_size(self):
        """
        Calculates the lesion size in the segmentation.

        Returns:
        -------
        dict
            A dictionary containing the lesion size.
        """
        lesion_size = (self.segmentation > 0).sum() * np.prod(self.spacing)
        return {'lesion_size': lesion_size}

    def calculate_tumor_center_mass(self, label=None):
        """
        Calculates the center of mass for the tumor in the image.

        Parameters:
        ----------
        label : int, optional
            The label value of the tumor (default is None).

        Returns:
        -------
        np.ndarray
            The center of mass coordinates adjusted by the voxel spacing.
        """
        if self.segmentation is None:
            raise ValueError("Image data is required to calculate the center of mass.")

        if label is not None and not np.any(self.segmentation == label):
            return np.array([np.nan] * len(self.segmentation.shape))

        coordinates = np.argwhere(self.segmentation != 0) if label is None else np.argwhere(self.segmentation == label)
        center_of_mass_mean = np.mean(coordinates, axis=0)
        return center_of_mass_mean * self.spacing

    def get_tumor_slices(self):
        axial_dim, coronal_dim, sagittal_dim = self.segmentation.shape
        axial_tumor_slices, coronal_tumor_slices, sagittal_tumor_slices = [], [], []

        # axial plane
        for n, s in enumerate(range(axial_dim)):
            slc = self.segmentation[s, :, :]
            if Counter(slc.flatten()).get(0) != (coronal_dim * sagittal_dim):
                axial_tumor_slices.append(n)

        # coronal plane
        for n, s in enumerate(range(coronal_dim)):
            slc = self.segmentation[:, s, :]
            if Counter(slc.flatten()).get(0) != (axial_dim * sagittal_dim):
                coronal_tumor_slices.append(n)

        # sagittal plane
        for n, s in enumerate(range(sagittal_dim)):
            slc = self.segmentation[:, :, s]
            if Counter(slc.flatten()).get(0) != (axial_dim * coronal_dim):
                sagittal_tumor_slices.append(n)

        return axial_tumor_slices, coronal_tumor_slices, sagittal_tumor_slices

    @staticmethod
    def calculate_tumor_distance(brain_centre_mass, tumor_centre_mass_per_label):
        tumor_location = {}
        for k, v in tumor_centre_mass_per_label.items():
            if not np.isnan(v).any():
                tumor_location[f'{k}_tumor_location'] = euclidean(brain_centre_mass, v)
            else:
                tumor_location[f'{k}_tumor_location'] = np.nan
        return tumor_location

    def extract_features(self, brain_centre_mass) -> dict:
        """
        Extracts all tumor-related features.

        Returns:
        -------
        dict
            A dictionary containing all tumor features.
        """

        # calculate the center of mass of the whole tumor and each label
        tumor_centre_mass_per_label = {}
        for idx, name in self.mapping_names.items():
            if name == 'BKG':
                name = "WHOLE"
            tumor_centre_mass_per_label[name.lower()] = self.calculate_tumor_center_mass(label=idx)

        # Flatten the dictionary to get the center of mass in each plane
        self.center_mass_dict = {
            f"{plane}_{label}_center_mass": coord
            for label, coords in tumor_centre_mass_per_label.items()
            for plane, coord in zip(["axial", "coronal", "sagittal"], coords)
        }

        # calculate tumor location for each label
        self.tumor_location = TumorFeatures.calculate_tumor_distance(list(brain_centre_mass), tumor_centre_mass_per_label)

        # calculate the number of tumor slices
        self.tumor_slices = {f"{k}_tumoral_slice": len(v) for k, v in
                             dict(zip(self.planes, self.get_tumor_slices())).items()}

        # calculate number of tumor pixels
        number_pixels = self.count_tumor_pixels()
        number_pixels.pop("bkg", None)
        number_pixels = {key: int(value * self.spacing.prod()) for key, value in number_pixels.items()}
        self.number_pixels = add_prefix_dict(number_pixels, prefix='lesion_size_')

        # calculate lesion size
        self.lesion_size = self.calculate_lesion_size()

        # Combine all features into a single dictionary
        return {**self.center_mass_dict, **self.tumor_location, **self.number_pixels, **self.lesion_size,
                **self.tumor_slices}
