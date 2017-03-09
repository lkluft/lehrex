# -*- coding: utf-8 -*-
"""General utility functions.
"""
import numpy as np


__all__ = [
    'stack_dicts',
]


def stack_dicts(a, b, *args, variables=None):
    """Stack the entries of given dictionaries.

    This function stacks the entries of (at least) two dictionaries. The data
    arrays stored with a specific key are combined using `np.hstack` and
    returned in a new dictionary. The variable keys have to exist in every
    given dictionary.

    Parameters:
        a, b (dict): Data dictionaries.
        *args: Arbitrary number of additional dictionaries.
        variables (list[str]): List of variables to extract and stack.

    Returns:
        dict: Dictionary containing the stacked data arrays.
    """
    if variables is None:
        variables = a.keys()

    dicts = [a, b] + list(args)

    return {k: np.hstack([d[k] for d in dicts]) for k in variables}
