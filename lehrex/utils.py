# -*- coding: utf-8 -*-
"""General utility functions.
"""
import re

import numpy as np


__all__ = [
    'stack_series',
]


def stack_series(dataframe, regex=None):
    """Stack all Series in the DataFrame that match a given regular expression.

    This function converts data series into a multidimensional array (e.g.
    time series of height resolved data).

    Parameters:
        dataframe (pd.DataFrame): Dataframe.
        regex (str): Python regular expression [0] matching
            the variable names of the profile.

    [0] https://docs.python.org/3.1/library/re.html

    Returns:
        ndarray, ndarray: data array, height levels.

    Examples:
        >>> import lehrex as lex
        >>> df = lex.read('CLB.txt')
        >>> p, z = lex.utils.stack_series(df, regex='CLB_B\d{5}')

    """
    # Find all variable keys matching the given regular expression.
    pattern = re.compile(regex)
    var_names = list(filter(pattern.match, dataframe.keys()))

    profile = np.vstack([dataframe[v] for v in sorted(var_names)])

    # Retrieve height information from variable names.
    z = [float(re.sub('[^0-9]', '', v)) for v in var_names]

    return np.ma.masked_invalid(profile), np.array(z)
