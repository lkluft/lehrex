# -*- coding: utf-8 -*-
"""Plot basic atmospheric properties conveniently.
"""
from matplotlib import dates
import matplotlib.pyplot as plt


__all__ = [
    'set_date_axis',
    'timeseries',
    'heatmap',
]


def set_date_axis(ax=None, dateformat='%d.%m.'):
    """Set DateFormatter for given AxesSubplot.

    Parameters:
        ax (AxesSubplot): Matplotlib axes.
        dateformat (str): Format string for date labels on xaxis.
    """
    formatter = dates.DateFormatter(dateformat)
    ax.xaxis.set_major_formatter(formatter)
    ax.grid('on', which='both', linestyle='-')


def timeseries(time, data, ax=None, ylabel='', **kwargs):
    """Create a basic timeseries plot.

    Parameters:
        time (nd.array): Date array in matplotlib time format.
        data (nd.array): Data array.
        ax (AxesSubplot): Matplotlib axes.
        ylabel (str): y label.
        **kwargs: Additional keyword arguments passed to `plt.plot`.

    Returns:
        Line2D: A line.

    """
    if ax is None:
        ax = plt.gca()

    line, = ax.plot(time, data, **kwargs)
    set_date_axis(ax)

    ax.set_xlim(time.min(), time.max())
    ax.set_xlabel('Datum')
    ax.set_ylabel(ylabel)
    ax.legend()

    return line


def heatmap(x, y, gridsize=100, rasterized=True, ax=None, **kwargs):
    """Plot a heatmap of given data.

    Parameters:
        x (np.ndarray): x data.
        y (np.ndarray): y data.
        gridsize (int or (int, int)):
            The number of hexagons in the *x*-direction, default is
            100. The corresponding number of hexagons in the
            *y*-direction is chosen such that the hexagons are
            approximately regular. Alternatively, gridsize can be a
            tuple with two elements specifying the number of hexagons
            in the *x*-direction and the *y*-direction.
        ax (AxesSubplot): Axes to plot in.
        **kwargs: Additional keyword argumens passed to `plt.hexbin`.

    Returns: Return values of `plt.hexbin`.
    """
    if ax is None:
        ax = plt.gca()

    def_kwargs = {
        'gridsize': gridsize,
        'rasterized': rasterized,
        'cmap': 'cubehelix_r',
        }

    def_kwargs.update(kwargs)

    return ax.hexbin(x, y, **def_kwargs)
