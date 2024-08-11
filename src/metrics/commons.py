

def calculate_relative_error(data, init, end):
    """
    Calculate the relative error between two columns in a DataFrame.

    Parameters:
    - data: DataFrame containing the data.
    - init: Initial column name.
    - end: Ending column name.

    Returns:
    - relative_error: Series containing the relative error.
    """
    return 100 * (data[end] - data[init]) / data[init]


def calculate_absolute_error(data, init, end):
    """
    Calculate the absolute error between two columns in a DataFrame.

    Parameters:
    - data: DataFrame containing the data.
    - init: Initial column name.
    - end: Ending column name.

    Returns:
    - absolute_error: Series containing the relative error.
    """
    return data[end] - data[init]


def calculate_ratio_improvement(data, init, end):
    """
    Calculate the ratio of improvement between two columns in a DataFrame.

    Parameters:
    - data: DataFrame containing the data.
    - init: Initial column name.
    - end: Ending column name.

    Returns:
    - ratio_improvement: Series containing the relative error.
    """

    return (data[end]) / (data[init])

