class ConstantsAPP:

    def __init__(self):
        self.mia_url = "https://www.artorg.unibe.ch/research/mia/index_eng.html"
        self.header = ""
        self.sub_header = ""
        self.description = ""
        self.contact = "[Contact us - MIA group](%s)" % self.mia_url

        self.mapping_buttons_metrics = {
            "Dice": "dice",
            # "Hausdorff distance": "haus",
            "Jaccard": "jacc",
            "Accuracy": "accu",
            "Precision": "prec",
            "Specificity": "spec",
            "Sensitivity": "sens"
        }

        self.mapping_buttons_columns = {
            "Patient ID": "ID",
            "Lesion size (All labels)": "lesion_size",
            'Lesion size (ENH)': 'lesion_size_enh',
            'Lesion size (EDE)': 'lesion_size_ede',
            'Lesion size (NEC)': 'lesion_size_nec',
            'Tumor location (All labels)': 'whole_tumor_location',
            'Tumor location (ENH)': 'enh_tumor_location',
            'Tumor location (EDE)': 'ede_tumor_location',
            'Tumor location (NEC)': 'nec_tumor_location'
        }

        self.mapping_order_by = {
            "Ascending": True,
            "Descending": False
        }

        self.mapping_feature_types = {
            'axial_dim': 'anatomical',
            'coronal_dim': 'anatomical',
            'sagittal_dim': 'anatomical',
            'axial_brain_centre_mass': 'anatomical',
            'coronal_brain_centre_mass': 'anatomical',
            'sagittal_brain_centre_mass': 'anatomical',
            'lesion_size_ede': 'anatomical',
            'lesion_size_enh': 'anatomical',
            'lesion_size_nec': 'anatomical',
            'whole_tumor_location': 'anatomical',
            'ede_tumor_location': 'anatomical',
            'enh_tumor_location': 'anatomical',
            'nec_tumor_location': 'anatomical',
            'lesion_size': 'anatomical',
            'axial_whole_center_mass': 'anatomical',
            'coronal_whole_center_mass': 'anatomical',
            'sagittal_whole_center_mass': 'anatomical',
            'axial_ede_center_mass': 'anatomical',
            'coronal_ede_center_mass': 'anatomical',
            'sagittal_ede_center_mass': 'anatomical',
            'axial_enh_center_mass': 'anatomical',
            'coronal_enh_center_mass': 'anatomical',
            'sagittal_enh_center_mass': 'anatomical',
            'axial_nec_center_mass': 'anatomical',
            'coronal_nec_center_mass': 'anatomical',
            'sagittal_nec_center_mass': 'anatomical',
            'axial_tumor_slices': 'anatomical',
            'coronal_tumor_slices': 'anatomical',
            'sagittal_tumor_slices': 'anatomical',
            'min_axial_tumor_slice': 'statistical',
            'min_coronal_tumor_slice': 'statistical',
            'min_sagittal_tumor_slice': 'statistical',
            'max_axial_tumor_slice': 'statistical',
            'max_coronal_tumor_slice': 'statistical',
            'max_sagittal_tumor_slice': 'statistical',
            't1_max_intensity': 'statistical',
            't1_min_intensity': 'statistical',
            't1_mean_intensity': 'statistical',
            't1_std_intensity': 'statistical',
            't1_skewness': 'statistical',
            't1c_max_intensity': 'statistical',
            't1c_min_intensity': 'statistical',
            't1c_mean_intensity': 'statistical',
            't1c_std_intensity': 'statistical',
            't1c_skewness': 'statistical',
            't2_max_intensity': 'statistical',
            't2_min_intensity': 'statistical',
            't2_mean_intensity': 'statistical',
            't2_std_intensity': 'statistical',
            't2_skewness': 'statistical',
            'flair_max_intensity': 'statistical',
            'flair_min_intensity': 'statistical',
            'flair_mean_intensity': 'statistical',
            'flair_std_intensity': 'statistical',
            'flair_skewness': 'statistical',
            't1_median_intensity': 'statistical',
            't1_range_intensity': 'statistical',
            't1c_median_intensity': 'statistical',
            't1c_range_intensity': 'statistical',
            't2_median_intensity': 'statistical',
            't2_range_intensity': 'statistical',
            'flair_median_intensity': 'statistical',
            'flair_range_intensity': 'statistical',
            't1_contrast_95_perc': 'texture',
            't1_contrast_mean': 'texture',
            't1_contrast_std': 'texture',
            't1_dissimilarity_95_perc': 'texture',
            't1_dissimilarity_mean': 'texture',
            't1_dissimilarity_std': 'texture',
            't1_homogeneity_95_perc': 'texture',
            't1_homogeneity_mean': 'texture',
            't1_homogeneity_std': 'texture',
            't1_energy_95_perc': 'texture',
            't1_energy_mean': 'texture',
            't1_energy_std': 'texture',
            't1_correlation_95_perc': 'texture',
            't1_correlation_mean': 'texture',
            't1_correlation_std': 'texture',
            't1_ASM_95_perc': 'texture',
            't1_ASM_mean': 'texture',
            't1_ASM_std': 'texture',
            't1c_contrast_95_perc': 'texture',
            't1c_contrast_mean': 'texture',
            't1c_contrast_std': 'texture',
            't1c_dissimilarity_95_perc': 'texture',
            't1c_dissimilarity_mean': 'texture',
            't1c_dissimilarity_std': 'texture',
            't1c_homogeneity_95_perc': 'texture',
            't1c_homogeneity_mean': 'texture',
            't1c_homogeneity_std': 'texture',
            't1c_energy_95_perc': 'texture',
            't1c_energy_mean': 'texture',
            't1c_energy_std': 'texture',
            't1c_correlation_95_perc': 'texture',
            't1c_correlation_mean': 'texture',
            't1c_correlation_std': 'texture',
            't1c_ASM_95_perc': 'texture',
            't1c_ASM_mean': 'texture',
            't1c_ASM_std': 'texture',
            't2_contrast_95_perc': 'texture',
            't2_contrast_mean': 'texture',
            't2_contrast_std': 'texture',
            't2_dissimilarity_95_perc': 'texture',
            't2_dissimilarity_mean': 'texture',
            't2_dissimilarity_std': 'texture',
            't2_homogeneity_95_perc': 'texture',
            't2_homogeneity_mean': 'texture',
            't2_homogeneity_std': 'texture',
            't2_energy_95_perc': 'texture',
            't2_energy_mean': 'texture',
            't2_energy_std': 'texture',
            't2_correlation_95_perc': 'texture',
            't2_correlation_mean': 'texture',
            't2_correlation_std': 'texture',
            't2_ASM_95_perc': 'texture',
            't2_ASM_mean': 'texture',
            't2_ASM_std': 'texture',
            'flair_contrast_95_perc': 'texture',
            'flair_contrast_mean': 'texture',
            'flair_contrast_std': 'texture',
            'flair_dissimilarity_95_perc': 'texture',
            'flair_dissimilarity_mean': 'texture',
            'flair_dissimilarity_std': 'texture',
            'flair_homogeneity_95_perc': 'texture',
            'flair_homogeneity_mean': 'texture',
            'flair_homogeneity_std': 'texture',
            'flair_energy_95_perc': 'texture',
            'flair_energy_mean': 'texture',
            'flair_energy_std': 'texture',
            'flair_correlation_95_perc': 'texture',
            'flair_correlation_mean': 'texture',
            'flair_correlation_std': 'texture',
            'flair_ASM_95_perc': 'texture',
            'flair_ASM_mean': 'texture',
            'flair_ASM_std': 'texture'
        }


class UnivariatePage(ConstantsAPP):

    def __init__(self):
        super().__init__()

        self.header = """Univariate feature analysis"""
        self.sub_header = """
            **Description**: It provides a comprehensive and interactive visualization of 
            single-variable distributions derived from MRI sequences or ground truth segmentations. This univariate 
            analysis is essential for those users aiming to explore and understand the distribution of individual 
            features in their datasets. The dashboard is equipped with interactive controls that allow users to 
            dynamically adjust the visualization parameters.
            """

        self.description_boxplot = """
            The inclusion of a boxplot offers a robust summary of the feature's distribution, highlighting key 
            statistics such as the median, quartiles, and potential outliers. The boxplot complements the histogram and 
            probability distribution, providing additional insights into the data's spread and central tendency.
            """

        self.description_distribution = """
            - **Histogram**: This visual representation helps in understanding the frequency distribution of the data points 
                        across different value ranges.
            - **Probability distribution**: Users can also view probability distributions, offering a smooth and continuous 
                        representation of the data, which is particularly useful for identifying underlying patterns 
                        and trends.
        """

        self.mapping_buttons_columns = {
            "Lesion size (All labels)": "lesion_size",
            'Lesion size (ENH)': 'lesion_size_enh',
            'Lesion size (EDE)': 'lesion_size_ede',
            'Lesion size (NEC)': 'lesion_size_nec',
            'Tumor location (All labels)': 'whole_tumor_location',
            'Tumor location (ENH)': 'enh_tumor_location',
            'Tumor location (EDE)': 'ede_tumor_location',
            'Tumor location (NEC)': 'nec_tumor_location',
            'Max. intensity (T1)': 't1_max_intensity',
            'Min. intensity (T1)': 't1_min_intensity',
            'Mean intensity (T1)': 't1_mean_intensity',
            'Std. intensity (T1)': 't1_std_intensity',
            'Skewness intensity (T1)': 't1_skewness',
            'Max. intensity (T1c)': 't1c_max_intensity',
            'Min. intensity (T1c)': 't1c_min_intensity',
            'Mean intensity (T1c)': 't1c_mean_intensity',
            'Std intensity (T1c)': 't1c_std_intensity',
            'Skewness intensity (T1c)': 't1c_skewness',
            'Max. intensity (T2)': 't2_max_intensity',
            'Min. intensity (T2)': 't2_min_intensity',
            'Mean intensity (T2)': 't2_mean_intensity',
            'Std intensity (T2)': 't2_std_intensity',
            'Skewness intensity (T2)': 't2_skewness',
            'Max. intensity (FLAIR)': 'flair_max_intensity',
            'Min. intensity (FLAIR)': 'flair_min_intensity',
            'Mean intensity (FLAIR)': 'flair_mean_intensity',
            'Std intensity (FLAIR)': 'flair_std_intensity',
            'Skewness intensity (FLAIR)': 'flair_skewness'
        }


class MultivariatePage(ConstantsAPP):

    def __init__(self):
        super().__init__()

        self.header = """Multivariate feature analysis"""
        self.sub_header = """
            **Description**: The following figure allows for an in-depth exploration of the extracted features from 
            magnetic resonance images (MRI) alongside their corresponding ground truth segmentations. This is achieved 
            through a bidimensional scatter plot that facilitates the visualization of complex relationships between 
            different intrinsic features.
            """
        self.description = """     
            Each point in the scatter plot represents a single data instance, allowing users to observe how various 
            features derived from MRI data distribute across different classes. The scatter plot employs two dimensions 
            to plot features against each other. This two-dimensional approach aids in uncovering correlations, 
            clusters, and outliers that may not be apparent in a unidimensional analysis. Data points in the scatter 
            plot are color-coded to represent different datasets, however, it also allows to color some of the 
            features.
            
            Users can interact with the scatter plot by zooming, panning, and selecting specific data points to obtain 
            more detailed information. This interactivity enhances the analytical capabilities, allowing for a more 
            thorough investigation of the data.
        """

        self.mapping_buttons_columns = {
            "Lesion size (All labels)": "lesion_size",
            'Lesion size (ENH)': 'lesion_size_enh',
            'Lesion size (EDE)': 'lesion_size_ede',
            'Lesion size (NEC)': 'lesion_size_nec',
            'Tumor location (All labels)': 'whole_tumor_location',
            'Tumor location (ENH)': 'enh_tumor_location',
            'Tumor location (EDE)': 'ede_tumor_location',
            'Tumor location (NEC)': 'nec_tumor_location',
            'Mean intensity (T1)': 't1_mean_intensity',
            'Mean intensity (T1c)': 't1c_mean_intensity',
            'Mean intensity (T2)': 't2_mean_intensity',
            'Mean intensity (FLAIR)': 'flair_mean_intensity'
        }


class SegmentationErrorMatrixPage(ConstantsAPP):

    def __init__(self):
        super().__init__()

        self.header = """Segmentation Error Matrix"""
        self.sub_header = """**Description**: The figure below is a confusion matrix that visualizes the performance 
        of an AI segmentation model in labeling MRI image pixels. Each row represents the actual pixel class as labeled 
        by a neuro-radiologist, while each column represents the predicted pixel class by the AI model. The numbers in 
        the cells indicate the count/percentage of pixels for each actual-predicted class pair. A darker cell color 
        signifies a higher number of errors, highlighting the model's misclassifications."""

        self.description = """
        - **True Label**: Indicated along the rows, representing the actual pixel classifications.
        - **Predicted Label**: Indicated along the columns, representing the AI model's pixel classifications.
        - **Diagonal Cells**: Correct classifications where the predicted label matches the true label. (omitted for now)
        - **Off-Diagonal Cells**: Misclassifications where the predicted label differs from the true label.
        """


class ModelPerformanceAnalysisPage(ConstantsAPP):

    def __init__(self):
        super().__init__()

        self.header = """Model performance analysis"""
        self.sub_header = """**Description:** The following figure allows for the exploration of model performance based on features 
        extracted from magnetic resonance images (MRI) and their corresponding ground truth segmentations. The scatter 
        plot displayed visualizes the relationship between a feature aggregated (for all labels) or not on the x-axis 
        and a metric on the y-axis. On the left sidebar, users can configure the visualization by selecting different 
        models and features. Additionally, the aggregated checkbox allows to aggregate the metric over all regions or 
        analyze them individually"""

        self.description = """
        Each data point represents a specific patient from one of the available datasets (distinguished by color). The 
        colors help in identifying patterns or trends specific to each dataset, potentially revealing variations in
        model performance across different data sources."""

        self.mapping_buttons_columns = {
            "Lesion size (All labels)": "lesion_size",
            'Lesion size (ENH)': 'lesion_size_enh',
            'Lesion size (EDE)': 'lesion_size_ede',
            'Lesion size (NEC)': 'lesion_size_nec',
            'Tumor location (All labels)': 'whole_tumor_location',
            'Tumor location (ENH)': 'enh_tumor_location',
            'Tumor location (EDE)': 'ede_tumor_location',
            'Tumor location (NEC)': 'nec_tumor_location',
            'Max. intensity (T1)': 't1_max_intensity',
            'Min. intensity (T1)': 't1_min_intensity',
            'Mean intensity (T1)': 't1_mean_intensity',
            'Std. intensity (T1)': 't1_std_intensity',
            'Skewness intensity (T1)': 't1_skewness',
            'Max. intensity (T1c)': 't1c_max_intensity',
            'Min. intensity (T1c)': 't1c_min_intensity',
            'Mean intensity (T1c)': 't1c_mean_intensity',
            'Std intensity (T1c)': 't1c_std_intensity',
            'Skewness intensity (T1c)': 't1c_skewness',
            'Max. intensity (T2)': 't2_max_intensity',
            'Min. intensity (T2)': 't2_min_intensity',
            'Mean intensity (T2)': 't2_mean_intensity',
            'Std intensity (T2)': 't2_std_intensity',
            'Skewness intensity (T2)': 't2_skewness',
            'Max. intensity (FLAIR)': 'flair_max_intensity',
            'Min. intensity (FLAIR)': 'flair_min_intensity',
            'Mean intensity (FLAIR)': 'flair_mean_intensity',
            'Std intensity (FLAIR)': 'flair_std_intensity',
            'Skewness intensity (FLAIR)': 'flair_skewness',
            'Axial tumor center of mass': 'axial_whole_center_mass',
            'Coronal tumor center of mass': 'coronal_whole_center_mass',
            'Sagittal tumor center of mass': 'sagittal_whole_center_mass',
            'Axial brain center of mass': 'axial_brain_centre_mass',
            'Coronal brain center of mass': 'coronal_brain_centre_mass',
            'Sagittal brain center of mass': 'sagittal_brain_centre_mass',
            'Axial tumor slices': 'axial_tumor_slices',
            'Coronal tumor slices': 'coronal_tumor_slices',
            'Sagittal tumor slices': 'sagittal_tumor_slices'
        }

    # mapping_buttons_metrics = {
    #     "Dice": "dice",
    #     "Hausdorff distance": "haus",
    #     "Jaccard": "jacc",
    #     "Accuracy": "acc",
    #     "Precision": "prec",
    #     "Specificity": "spec",
    #     "Sensitivity": "sens"
    # }


class PairwiseModelPerformanceComparisonPage(ConstantsAPP):

    def __init__(self):
        super().__init__()

        self.header = """Pairwise model performance comparison"""
        self.sub_header = """
        **Description**: The following figure illustrates the percentage difference in a selected 
        metric between two models across various regions for each patient. In this bar chart, each bar represents the 
        difference in a selected metric for a specific brain region (Average, NEC, ENH, and EDE), comparing the baseline
        model with the new model. The length of each bar indicates the magnitude of the improvement or decline in 
        performance, with longer bars representing larger differences. The green color of the bars indicates the overall
        gain achieved by the new model over the baseline model.
        
        Additionally, there is a checkbox labeled "Aggregated," which, when checked, aggregates the metric across all 
        patients, providing a summarized view of the model's performance differences.
        """

        self.description = """
        When comparing the performance of two models, several metrics can be used to quantify the difference: Absolute, 
        Relative, and Ratio. A detailed explanation can be found below.
        
        - **Absolute improvement** measures the direct difference between the performance metrics of two models. 
        
        - **Relative improvement** provides a measure of the difference between two metrics relative to the magnitude of the 
        reference metric (typically the value of baseline model).
        
        - **Improvement Ratio** measures how much better one model is compared to another by directly comparing their metric ratio. 
        
        For all the formulas are presented, M represents any of the available metrics (Dice score, accuracy, ...).
        """

        self.absolute_formula = r'''\text{Absolute} = M_{\text{New model}} - M_{\text{Baseline model}}'''
        self.relative_formula = r'''\text{Relative} = \frac{M_{\text{New model}} - M_{\text{Baseline model}}}{M_{\text{Baseline model}}}'''
        self.ratio_formula = r'''\text{Ratio} = \frac{M_{\text{New model}}}{M_{\text{Baseline model}}}'''

        self.colorbar = {
            'decrease': '#ffbf69',
            'increase': '#90be6d'
        }

        self.mapping_buttons_columns = {
            "Patient ID": "ID",
            "Lesion size (All labels)": "lesion_size",
            'Lesion size (ENH)': 'lesion_size_enh',
            'Lesion size (EDE)': 'lesion_size_ede',
            'Lesion size (NEC)': 'lesion_size_nec',
            'Tumor location (All labels)': 'whole_tumor_location',
            'Tumor location (ENH)': 'enh_tumor_location',
            'Tumor location (EDE)': 'ede_tumor_location',
            'Tumor location (NEC)': 'nec_tumor_location',
            'Mean intensity (T1)': 't1_mean_intensity',
            'Mean intensity (T1c)': 't1c_mean_intensity',
            'Mean intensity (T2)': 't2_mean_intensity',
            'Mean intensity (FLAIR)': 'flair_mean_intensity'
        }


class MultiModelPerformanceComparisonsPage(ConstantsAPP):

    def __init__(self):
        super().__init__()

        self.header = """Multi-model performance comparison"""
        self.sub_header = """
        **Description**: The following table summarizes the mean and standard deviation obtained by the selected models 
        for a set of metrics. The table provides a comprehensive comparison of different segmentation models across 
        various tumor regions. Each row corresponds to a specific combination of region and model, and the columns 
        present the performance metrics along with their respective standard deviations.
        
        There is also a checkbox labeled "Aggregated," which, when checked, aggregates the performance metrics across all 
        patients, providing a summarized view of the model's performance
        """

        self.description = """
            Additionally, a boxplot is shown to further provide more visual insights about the model performance 
            distribution.
        """


class LongitudinalAnalysis(ConstantsAPP):

    def __init__(self):
        super().__init__()

        self.header = """Longitudinal analysis"""
        self.sub_header = """
            **Description**: The following figures allow visualization of longitudinal data depicting the variation in 
            lesion size over time. Both lineplots are designed to provide insights into how well predicted lesion 
            sizes align with actual values over the course of multiple timepoints. Users can interact with the plot by 
            zooming, panning, and selecting specific data points to obtain more detailed information. This interactivity
            enhances the analytical capabilities, allowing for a more thorough investigation of the data.


        ##### Relative Error in Lesion Size Estimation
        This plot shows two lines representing actual lesion size and predicted lesion size over different timepoints.
        Dashed lines between data points indicate the relative error in the lesion size estimation, displayed as a 
        percentage above each segment. Additionally, annotations highlight the percentage difference between actual 
        and predicted lesion sizes.

            """
        self.description = """
        ##### Absolute Difference in Lesion Size Variation
        This plot displays the absolute difference in variation between actual and predicted lesion sizes over different
        timepoints. Slopes between consecutive points indicate the absolute difference in variation, annotated with 
        numerical values. Each line is color-coded to differentiate between observed and predicted lesion sizes.
        """


class SubjectsExploration(ConstantsAPP):

    def __init__(self):
        super().__init__()

        self.header = """Subjects Exploration"""
        self.sub_header = """
            **Description**: This tab provides a comprehensive exploration of the selected subject, offering detailed 
            insights across several key dimensions. The features are organized into three primary categories: anatomical
             features, first order statistical features, and second order texture features. Additionally, it provides 
             insights into the nature of the subject compared to the rest of the dataset.
            """
        self.description = """
        ##### 
        ....
        """




# class Features:
#     mapping_features = {
#         'Patient ID': 'ID',
#         'Axial dim.': 'axial_dim',
#         'Coronal dim.': 'coronal_dim',
#         'Sagittal dim.': 'sagittal_dim',
#         'Brain CM (Axial)': 'axial_brain_centre_mass',
#         'Brain CM (Coronal)': 'coronal_brain_centre_mass',
#         'Brain CM (Sagittal)': 'sagittal_brain_centre_mass',
#         'No. tumor slices (Axial)': 'axial_tumor_slices',
#         'No. tumor slices (Coronal)': 'coronal_tumor_slices',
#         'No. tumor slices (Sagittal)': 'sagittal_tumor_slices',
#         'Lower tumor slice (Axial)': 'min_axial_tumor_slice',
#         'Upper tumor slice (Axial)': 'max_axial_tumor_slice',
#         'Lower tumor slices (Coronal)': 'min_coronal_tumor_slice',
#         'Upper tumor slice (Coronal)': 'max_coronal_tumor_slice',
#         'Lower. tumor slices (Sagittal)': 'min_sagittal_tumor_slice',
#         'Upper tumor slice (Sagittal)': 'max_sagittal_tumor_slice',
#         'No. pixels (BKG)': 'tumor_pixel_bkg',
#         'No. pixels (ENH)': 'tumor_pixel_enh',
#         'No. pixels (EDE)': 'tumor_pixel_ede',
#         'No. pixels (NEC)': 'tumor_pixel_nec',
#         'Tumor location (All labels)': 'whole_tumor_location',
#         'Tumor location (ENH)': 'enh_tumor_location',
#         'Tumor location (EDE)': 'ede_tumor_location',
#         'Tumor location (NEC)': 'nec_tumor_location',
#         'Lesion size': 'lesion_size',
#         'Tumor CM (Whole Axial)': 'axial_whole_center_mass',
#         'Tumor CM (Whole Coronal)': 'coronal_whole_center_mass',
#         'Tumor CM (Whole Sagittal)': 'sagittal_whole_center_mass',
#         'Tumor CM (ENH Axial)': 'axial_enh_center_mass',
#         'Tumor CM (ENH Coronal)': 'coronal_enh_center_mass',
#         'Tumor CM (ENH Sagittal)': 'sagittal_enh_center_mass',
#         'Tumor CM (EDE Axial)': 'axial_ede_center_mass',
#         'Tumor CM (EDE Coronal)': 'coronal_ede_center_mass',
#         'Tumor CM (EDE Sagittal)': 'sagittal_ede_center_mass',
#         'Tumor CM (NEC Axial)': 'axial_nec_center_mass',
#         'Tumor CM (NEC Coronal)': 'coronal_nec_center_mass',
#         'Tumor CM (NEC Sagittal)': 'sagittal_nec_center_mass',
#         'Max. intensity (T1)': 't1_max_intensity',
#         'Min. intensity (T1)': 't1_min_intensity',
#         'Mean intensity (T1)': 't1_mean_intensity',
#         'Std. intensity (T1)': 't1_std_intensity',
#         'Skewness intensity (T1)': 't1_skewness',
#         'Max. intensity (T1c)': 't1c_max_intensity',
#         'Min. intensity (T1c)': 't1c_min_intensity',
#         'Mean intensity (T1c)': 't1c_mean_intensity',
#         'Std intensity (T1c)': 't1c_std_intensity',
#         'Skewness intensity (T1c)': 't1c_skewness',
#         'Max. intensity (T2)': 't2_max_intensity',
#         'Min. intensity (T2)': 't2_min_intensity',
#         'Mean intensity (T2)': 't2_mean_intensity',
#         'Std intensity (T2)': 't2_std_intensity',
#         'Skewness intensity (T2)': 't2_skewness',
#         'Max. intensity (FLAIR)': 'flair_max_intensity',
#         'Min. intensity (FLAIR)': 'flair_min_intensity',
#         'Mean intensity (FLAIR)': 'flair_mean_intensity',
#         'Std intensity (FLAIR)': 'flair_std_intensity',
#         'Skewness intensity (FLAIR)': 'flair_skewness'
#     }
