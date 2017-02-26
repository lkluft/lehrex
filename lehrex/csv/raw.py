# -*- coding: utf-8 -*-
"""Load CSV files stored in RAW format.
"""
import numpy as np
from matplotlib import dates


__all__ = [
    'read_raw',
]


def _get_names(filename, delimiter=';', comments='%'):
    """Get variable names from CSV file in RAW format.

    Parameters:
        filename (str): Path to CSV file.
        delimiter (str): The string used to separate values.
        comments (str): The character used to indicate the start of a comment.

    Returns:
        list[str]: Variable names.
    """
    for line in open(filename, 'rt', encoding='UTF-8', errors='ignore'):
        if not line.startswith(comments):
            return line.strip().split(delimiter)


def _get_mpl_start(filename):
    with open(filename) as f:
        return dates.datestr2num(':'.join(f.readline().split(':')[1:]))


def _decimal_converter(filename, comments='%'):
    """Convert decimal separator from comma to period.

    While doing so also ignore weirdly encoded characters.

    Parameters:
        filename (str): Path to CSV file.
        comments (str): The character used to indicate the start of a comment.

    Returns:
        iterator: Return byte objects that can be read by `np.genfromtxt`.
    """
    for line in open(filename, 'rt', encoding='UTF-8', errors='ignore'):
        if line.startswith(comments):
            yield line.encode()
        else:
            yield line.replace(',', '.').encode()


def read_raw(filename, datarate=20, delimiter=';', comments='%',
             variables=None, output=None, **kwargs):
    """Read file in RAW format.

    Parameters:
        filename (str): Path to CSV file.
        datarate (float): Measurement rate [Hz].
        delimiter (str): The string used to separate values.
        comments (str): The character used to indicate the start of a comment.
        filling_values (float): Value to use for missing values.
            If `None`, use the `DefaultValue` specified in file header.
        variables (List[str]): List of variables to extract.
        output (dict): Dictionary that is updated with read data.
        **kwargs: Additional keyword arguments passed to `np.genfromtxt`.

    Returns:
        dict: Dictionary containing the data arrays.
    """
    names = _get_names(filename, delimiter, comments)
    if variables is None:
        variables = names

    data = np.genfromtxt(
        _decimal_converter(filename, comments),
        delimiter=';',
        comments=comments,
        names=names,
        usecols=variables,
        skip_header=2,
        **kwargs,
        )

    # Convert structured array to dictionary.
    if output is None:
        output = {var: data[var] for var in variables}
    else:
        for var in variables:
            output[var] = data[var]

    # TODO: Parsing the actual data rate from file.
    # Create time array using start time and data rate.
    start = _get_mpl_start(filename)  # Start time in MPL format.
    N = data.shape[0]  # Number of measurements.
    dt = 1 / (24 * 60 * 60 * datarate)  # Time difference betwen measurements.
    output['MPLTIME'] = np.arange(start, start + N * dt, dt)

    return output
