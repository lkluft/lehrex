# -*- coding: utf-8 -*-
"""Plot basic atmospheric properties conveniently.
"""
from matplotlib import dates
import matplotlib.pyplot as plt

from .common import get_label


__all__ = [
    'set_date_axis',
    'timeseries',
    'timeseries2d',
]


def set_date_axis(ax=None, dateformat='%d.%m.'):
    """Set DateFormatter for given AxesSubplot.

    Parameters:
        ax (AxesSubplot): Matplotlib axes.
        dateformat (str): Format string for date labels on xaxis.
    """
    if ax is None:
        ax = plt.gca()

    formatter = dates.DateFormatter(dateformat)
    ax.xaxis.set_major_formatter(formatter)
    ax.grid('on', which='both', linestyle='-')


def timeseries(dataframe, key, xlabel='Datum', label=None, dateformat='%d.%m.',
               ax=None, **kwargs):
    """Create a basic timeseries plot.

    Parameters:
        dataframe (pd.Dataframe): Dataframe.
        key (str): Variable key.
        xlabel (str): x label.
        label (str): Line label.
        dateformat (str): Format string for date labels on xaxis.
        ax (AxesSubplot): Matplotlib axes.
        **kwargs: Additional keyword arguments passed to `plt.plot`.

    Returns:
        Line2D: A line.
    """
    if ax is None:
        ax = plt.gca()

    if label is None:
        label = get_label(key, label='{name}')

    line, = ax.plot(dataframe.index, dataframe[key], label=label, **kwargs)
    set_date_axis(ax, dateformat)

    ax.set_xlabel(xlabel)
    ax.legend()

    return line


def timeseries2d(x, y, c, xlabel='Datum', ylabel='Höhe [m]',
                 zlabel='', dateformat='%d.%m.', ax=None, **kwargs):
    """Create a basic 2D timeseries plot.

    Parameters:
        x, y, c (ndarray): Data arrays.
        xlabel (str): x label.
        ylabel (str): y label.
        zlabel (str): Colorbar label.
        dateformat (str): Format string for date labels on xaxis.
        ax (AxesSubplot): Matplotlib axes.
        **kwargs: Additional keyword arguments passed to `plt.pcolormesh`.

    Returns:
        matplotlib.collections.QuadMesh
    """
    if ax is None:
        ax = plt.gca()

    ret = ax.pcolormesh(x, y, c, **kwargs)

    cb = ax.get_figure().colorbar(ret)
    cb.set_label(zlabel)

    set_date_axis(ax, dateformat)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    return ret
