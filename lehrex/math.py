# -*- coding: utf-8 -*-
"""Mathematical functions.
"""
import collections
import numpy as np


__all__ = ['integrate_spectrum',
           'integrate_angles',
           'moving_average',
           'block_average',
           'bootstrap',
           'correlation',
           'rmse',
           'compare_arrays',
           ]


def integrate_spectrum(f, B, factor=np.pi):
    """Integrate a radiance spectrum.

    Parameters:
        f (np.array): Frequencies.
        B (np.array): Radiances.
        factor (float): Integration faktor.
            Default pi for integration over full halfroom.

    Returns:
        float: Power [W * m**-2].

    """
    B_mean = (B[1:] + B[:-1]) / 2
    df = np.diff(f)

    return factor * np.sum(B_mean * df)


def integrate_angles(f, y_los, los, dtheta):
    """Integrate spectrum over frequency and angles.

    Parameters:
        f: Frequency grid [Hz].
        y_los: Concatenated spectra for all angles.
        los: Viewing angles.
        dtheta (float): Angle resolution.

    Retuns:
        Integrated spectrum [W/m**2].

    """
    y_int = np.zeros(f.size)
    for y, a in zip(np.split(y_los, los.size), los):
        y_int += (2 * np.pi * np.sin(np.deg2rad(a))
                  * np.cos(np.deg2rad(a)) * y
                  * np.deg2rad(dtheta))
    return integrate_spectrum(f, y_int, factor=1)


def moving_average(x, y, N, mode='same'):
    """Calculate running mean for given timeseries.

    Parameters:
        x (np.ndarray): x data.
        y (np.ndarray): y data.
        N (int): Window size.
        mode (str): Convolve mode 'valid' or 'same'.

    Returns:
        np.ndarray, np.ndarray: Adjusted x data, Averaged y data.

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
    """Calculate the average over the last N values in y.

    Parameters:
        x (np.ndarray): x data.
        y (np.ndarray): y dat.
        N (int): Window size to average.

    Returns:
        np.ndarray, np.ndarray: Every n-th x value, Corresponding averages.

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
        np.ndarray, shape (size,): The generated random samples.

    """
    return np.random.choice(x, size=size, replace=True)


def rmse(x, y):
    """Calculate the Root Mean Squared Error.

    Parameters:
        x (np.ndarray): First data array.
        y (np.ndarray): Second data array.

    Returns:
        float: RMSE

    """
    return np.sqrt(np.nanmean((x - y)**2))


def correlation(x, y):
    """Return single correlatin coefficient.

    Parameters:
        x (np.ndarray): First data array.
        y (np.ndarray): Second data array.

    Returns:
        float: Correlation coefficient.

    """
    x = np.ma.masked_invalid(x)
    y = np.ma.masked_invalid(y)
    return np.ma.corrcoef(x, y)[0, 1]


def compare_arrays(x, y, verbose=False):
    """Perform a simple statistic comparison of two arrays.

    Parameters:
        x (np.ndarray): First data array.
        y (np.ndarray): Second data array.
        verbose (bool): Print output.

    Returns:
        float: Correlation coefficient.

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
