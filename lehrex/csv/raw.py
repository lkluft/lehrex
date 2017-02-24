# -*- coding: utf-8 -*-
"""Load CSV files stored in RAW format.
"""
import numpy as np


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


def read_raw(filename, delimiter=';', comments='%', variables=None,
             output=None, **kwargs):
    """Read file in RAW format.

    Parameters:
        filename (str): Path to CSV file.
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

    # TODO: Create time array using start time and data rate.
    # output['MPLTIME'] = 42

    return output
