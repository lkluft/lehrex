# -*- coding: utf-8 -*-
"""Mathematical functions.
"""
import collections
import numpy as np


__all__ = [
    'moving_average',
    'block_average',
    'bootstrap',
    'correlation',
    'rmse',
    'compare_arrays',
]


def moving_average(x, y, N, mode='same'):
    """Calculate running mean for given timeseries.

    Parameters:
        x (ndarray): x data.
        y (ndarray): y data.
        N (int): Window size.
        mode (str): Convolve mode 'valid' or 'same'.

    Returns:
        ndarray, np.ndarray: Adjusted x data, Averaged y data.
    """
    if mode == 'valid':
        l, t = N//2, -N//2 + 1
        x = x[l:t]
    elif mode == 'full':
        raise Exception(
            'Mode "full" is not supported to prevent boundary effects.'
            'If you know what you are doing, use numpy.convolve to use'
            'full mode.')

    return x, np.convolve(y, np.ones((N,)) / N, mode=mode)


def block_average(x, y, N):
    """Calculate the average over windows of size N.

    Parameters:
        x (ndarray): x data.
        y (ndarray): y dat.
        N (int): Window size to average.

    Returns:
        ndarray, ndarray: Every n-th x value, Corresponding averages.
    """
    x = x[N-1::N]
    y = np.array([np.nanmean(v) for v in np.split(y, y.size / N)])

    return x, y


def bootstrap(x, size=None):
    """Generate a bootstrap of given size from x.

    Note:
        This function is a simple wrapper for np.random.choice

    Parameters:
        a (1-D array-like or int):
            If an ndarray, a random sample is generated from its elements.
            If an int, the random sample is generated as if a was np.arange(n)
        size (int or tuple of ints): Output shape.
            If the given shape is, e.g., ``(m, n, k)``, then
            ``m * n * k`` samples are drawn.  Default is None, in which case a
            single value is returned.

    Returns:
        ndarray, shape (size,): The generated random samples.
    """
    return np.random.choice(x, size=size, replace=True)


def rmse(x, y):
    """Calculate the Root Mean Squared Error.

    Parameters:
        x (ndarray): First data array.
        y (ndarray): Second data array.

    Returns:
        float: RMSE
    """
    return np.sqrt(np.nanmean((x - y)**2))


def correlation(x, y):
    """Return single correlatin coefficient.

    Parameters:
        x (ndarray): First data array.
        y (ndarray): Second data array.

    Returns:
        float: Correlation coefficient.
    """
    x = np.ma.masked_invalid(x)
    y = np.ma.masked_invalid(y)
    return np.ma.corrcoef(x, y)[0, 1]


def compare_arrays(x, y, verbose=False):
    """Perform a simple comparison of two arrays.

    Parameters:
        x (ndarray): First data array.
        y (ndarray): Second data array.
        verbose (bool): Print output.

    Returns:
        namedtuple: Statistical comparison of two arrays.
    """

    ArrayComparison = collections.namedtuple(
        'ArrayComparison',
        ['rmse',
         'corrcoef',
         'mean_first',
         'mean_second',
         ])

    stats = ArrayComparison(
        rmse=rmse(x, y),
        corrcoef=correlation(x, y),
        mean_first=np.nanmean(x),
        mean_second=np.nanmean(y),
        )

    if verbose:
        print(
            'RMSE: {:5.3f}\n'
            'Correlation: {:5.3f}\n'
            'First Array Mean: {:5.3f}\n'
            'Second Array Mean: {:5.3f}\n'
            .format(*stats)
            )

    return stats
