import numpy as np


# TODO: A bit isolated. May be ok, but if so, the filename should be changed. Other option could be to include it
#  within the commons
def mistakes_per_class(ground_truth, predicted, unique_classes):

    # find all unique classes present in the ground truth data and predictions
    num_classes = len(unique_classes)

    # initialize a zero matrix with the maximum range of classes
    errors = np.zeros((num_classes, num_classes), dtype=np.int32)

    for i in range(num_classes):
        # find indices where class i in ground_truth was misclassified in the prediction
        indices_error = np.where(ground_truth == unique_classes[i], predicted, -1)
        unique, counts = np.unique(indices_error, return_counts=True)

        # count the number of errors made for each class
        for j, count in zip(unique, counts):
            if j != -1 and j != unique_classes[i]:
                # find the index corresponding to class j in unique_classes
                index_j = np.where(unique_classes == j)[0][0]
                errors[i, index_j] = count

    return errors


def mistakes_per_class_optim(ground_truth, predicted, unique_classes):
    # Find all unique classes present in the ground truth data and predictions
    num_classes = len(unique_classes)

    # Initialize a zero matrix with the maximum range of classes
    errors = np.zeros((num_classes, num_classes), dtype=np.int32)

    # Convert ground truth and predicted to arrays for indexing
    ground_truth = np.array(ground_truth)
    predicted = np.array(predicted)

    # Calculate indices where ground truth and prediction match
    match_indices = (ground_truth == predicted)

    # Calculate errors per class
    for i, class_i in enumerate(unique_classes):
        # Find indices where ground truth equals class_i
        class_indices = (ground_truth == class_i)

        # Count errors for each unique class predicted when ground truth is class_i
        unique, counts = np.unique(predicted[class_indices & ~match_indices], return_counts=True)

        # Map unique classes to their indices in unique_classes
        unique_to_index = {class_j: index for index, class_j in enumerate(unique_classes)}

        # Update errors matrix
        for class_j, count in zip(unique, counts):
            if class_j in unique_to_index:
                errors[i, unique_to_index[class_j]] = count

    return errors


def normalize_matrix_per_row(matrix):
    row_sums = matrix.sum(axis=1)
    zero_sum_mask = (row_sums == 0)
    row_sums[zero_sum_mask] = 1
    normalized_matrix = 100 * matrix / row_sums[:, np.newaxis]
    normalized_matrix[zero_sum_mask] = 0
    return normalized_matrix
