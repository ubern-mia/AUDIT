from itertools import combinations

import numpy as np
from scipy.stats import kruskal, ttest_rel
from scipy.stats import mannwhitneyu
from scipy.stats import shapiro
from scipy.stats import wilcoxon
from statsmodels.stats.diagnostic import lilliefors

# TODO: check whether all the functions in here are necessary now or in the future
def kruskal_wallis_test(samples: list, alpha=0.05):
    """
    Compute the Kruskal-Wallis H-test for independent samples.

    The Kruskal-Wallis H-test tests the null hypothesis that the population median of all the groups are equal. It is a
    non-parametric version of ANOVA. The test works on 2 or more independent samples, which may have different sizes.
    Note that rejecting the null hypothesis does not indicate which of the groups differs. Post hoc comparisons between
    groups are required to determine which groups are different.
    """

    # all samples must have more than 5 elements
    if all(len(sample) > 5 for sample in samples):
        statistic, p_value = kruskal(*samples, nan_policy='omit')
        if p_value <= alpha:
            return round(p_value, 3), "rejected"
        else:
            return round(p_value, 3), "accepted"
    else:
        assert "Some of the samples do not contain more than 5 elements."


def mann_whitney_test(samples, alpha=0.05):
    """
    Perform the Mann-Whitney U rank test on two independent samples.

    The Mann-Whitney U test is a nonparametric test of the null hypothesis that the distribution underlying sample x is
    the same as the distribution underlying sample y. It is often used as a test of difference in location between
    distributions.
    """
    sample_a, sample_b = samples
    # all samples must have more than 5 elements
    if all(len(sample) > 5 for sample in samples):
        statistic, p_value = mannwhitneyu(sample_a, sample_b, nan_policy='omit')
        if p_value <= alpha:
            return round(p_value, 3), "rejected"
        else:
            return round(p_value, 3), "accepted"
    else:
        assert "Some of the samples do not contain more than 5 elements."


def mann_whitney_test_post_hoc(samples, alpha=0.05):
    """
    Perform the Mann-Whitney U rank test on pairs of independent samples.

    The Mann-Whitney U test is a nonparametric test of the null hypothesis that the distribution underlying sample x is
    the same as the distribution underlying sample y. It is often used as a test of difference in location between
    distributions.

    Parameters:
    samples (list of array-like): List of samples to be compared.
    alpha (float): Significance level for determining the rejection of the null hypothesis. Default is 0.05.

    Returns:
    tuple: A tuple containing:
        - matrix (numpy.ndarray): Matrix of p-values obtained from pairwise comparisons.
        - rejected (numpy.ndarray): Matrix indicating whether the null hypothesis is rejected based on the specified alpha.
    """

    def combine_matrices(matrix, rejected):
        """
        Combine the matrices of p-values and rejection decisions into a final matrix.

        Parameters:
        matrix (numpy.ndarray): Matrix of p-values obtained from pairwise comparisons.
        rejected (numpy.ndarray): Matrix indicating whether the null hypothesis is rejected based on the specified alpha.

        Returns:
        numpy.ndarray: Combined matrix with lower values for numeric p-values and upper values for rejection decisions.
        """
        N = matrix.shape[0]
        combined_matrix = np.empty((N, N), dtype=object)

        # Fill lower triangular part with p-values
        combined_matrix[np.tril_indices(N, k=-1)] = matrix[np.tril_indices(N, k=-1)]

        # Fill upper triangular part with rejection decisions
        combined_matrix[np.triu_indices(N, k=1)] = rejected[np.triu_indices(N, k=1)]

        # Set diagonal elements to NaN
        np.fill_diagonal(combined_matrix, np.nan)

        return combined_matrix

    N = len(samples)
    matrix = np.zeros((N, N))
    rejected = np.empty((N, N), dtype=object)

    for i, j in combinations(range(N), 2):
        sample_a, sample_b = samples[i], samples[j]
        # all samples must have more than 5 elements
        if all(len(sample) > 5 for sample in [sample_a, sample_b]):
            statistic, p_value = mannwhitneyu(sample_a, sample_b, nan_policy='omit')
            matrix[i, j] = matrix[j, i] = round(p_value, 3)
            if p_value <= alpha:
                rejected[i, j] = rejected[j, i] = "Statistical differences"
            else:
                rejected[i, j] = rejected[j, i] = "No statistical differences"
        else:
            assert "Some of the samples do not contain more than 5 elements."

    return combine_matrices(matrix, rejected)


def paired_ttest(sample1, sample2, alpha=0.05):
    """
    Perform paired t-test between two samples and interpret the result.

    Parameters:
    - sample1 (array-like): The first sample.
    - sample2 (array-like): The second sample.
    - alpha (float): The significance level for the test (default is 0.05).

    Returns:
    - dict: A dictionary containing the test statistic, p-value, and interpretation.
    """

    # Perform paired t-test if both samples are normal
    t_stat, p_value = ttest_rel(sample1, sample2, nan_policy='omit')

    # Interpret the result
    if p_value <= alpha:
        interpretation = (f"Given the alpha {alpha}, reject the null hypothesis. There is a significant difference "
                          f"between the samples.")
    else:
        interpretation = (f"Given the alpha {alpha}, fail to reject the null hypothesis. There is no significant "
                          f"difference between the samples.")

    return {'p-value': p_value, 'interpretation': interpretation}


def wilcoxon_test(sample1, sample2, alpha=0.05):
    """
    Perform the Wilcoxon signed-rank test between two samples and interpret the result.

    Parameters:
    sample1 (array-like): The first sample.
    sample2 (array-like): The second sample.
    alpha (float): The significance level for the test (default is 0.05).

    Returns:
    dict: A dictionary containing the test statistic, p-value, and interpretation.
    """

    # Perform Wilcoxon signed-rank test
    w_stat, p_value = wilcoxon(sample1, sample2, nan_policy='omit')

    # Interpret the result
    if p_value <= alpha:
        interpretation = (f"Given the alpha {alpha}, reject the null hypothesis. There is a significant difference "
                          f"between the samples.")
    else:
        interpretation = (f"Given the alpha {alpha}, fail to reject the null hypothesis. There is no significant "
                          f"difference between the samples.")

    # Return the test statistic, p-value, and interpretation
    return {'p-value': p_value, 'interpretation': interpretation}


"""
NORMALITY TESTS
"""


def shapiro_wilk_test(sample, alpha=0.05):
    """
    Perform the Shapiro-Wilk test for normality on a sample and interpret the result.

    Parameters:
    sample (array-like): The sample to test for normality.
    alpha (float): The significance level for the test (default is 0.05).

    Returns:
    dict: A dictionary containing the test statistic, p-value, and interpretation.
    """
    # Perform Shapiro-Wilk test
    test_statistic, p_value = shapiro(x=sample, nan_policy='omit')

    # Convert to scientific notation
    stat_sci = f"{test_statistic:.3e}"
    p_value_sci = f"{p_value:.3e}"

    # Interpret the result
    if p_value <= alpha:
        interpretation = f"Null hypothesis rejected, the sample does not follow a normal distribution."
        normality = False
    else:
        interpretation = f"Fail to reject the null hypothesis, the sample follows a normal distribution."
        normality = True

    # Return the test statistic, p-value, and interpretation
    return {
        'Statistic': stat_sci,
        'P-value': p_value_sci,
        'Normally distributed': normality,
        'Null hypothesis interpretation': interpretation
    }


def lilliefors_test(sample, alpha=0.05):
    """
    Perform the Lilliefors test for normality on a sample and interpret the result.

    Parameters:
    sample (array-like): The sample to test for normality.
    alpha (float): The significance level for the test (default is 0.05).

    Returns:
    dict: A dictionary containing the test statistic, p-value, and interpretation.
    """
    # Perform Lilliefors test
    test_statistic, p_value = lilliefors(sample, dist='norm', pvalmethod='approx')

    # Convert to scientific notation
    stat_sci = f"{test_statistic:.3e}"
    p_value_sci = f"{p_value:.3e}"

    # Interpret the result
    if p_value <= alpha:
        interpretation = f"Null hypothesis rejected, the sample does not follow a normal distribution."
        normality = False
    else:
        interpretation = f"Fail to reject the null hypothesis, the sample follows a normal distribution."
        normality = True

    # Return the test statistic, p-value, and interpretation
    return {
        'Statistic': stat_sci,
        'P-value': p_value_sci,
        'Normally distributed': normality,
        'Null hypothesis interpretation': interpretation
    }


def normality_test(data, alpha=0.05, threshold_observations=50):
    """
    Check the normality of data using Shapiro-Wilk or Lilliefors test based on the sample size.

    Parameters:
    - data (array-like): The data to be tested for normality.
    - alpha (float): The significance level for the tests (default is 0.05).
    - threshold_observations (int): The sample size threshold for choosing between Shapiro-Wilk and Lilliefors test.

    Returns:
    - dict: A dictionary containing the test name, test statistic, p-value, and normality assessment.
    """
    # Number of observations in the data
    n = len(data)

    if n <= threshold_observations:
        # Use Shapiro-Wilk test for smaller sample sizes
        result = shapiro_wilk_test(data, alpha)
        test_name = "Shapiro-Wilk"
    else:
        # Use Lilliefors test for larger sample sizes
        result = lilliefors_test(data, alpha)
        test_name = "Lilliefors"

    # Building output
    output = {
        "Test performed": test_name,
        "Sample length": n,
        "Alpha": alpha
    }
    output.update(result)

    return output
