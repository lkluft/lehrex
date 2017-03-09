# -*- coding: utf-8 -*-
"""Plot basic atmospheric properties conveniently.
"""
from matplotlib import dates
import matplotlib.pyplot as plt


__all__ = [
    'set_date_axis',
    'timeseries',
    'timeseries2d',
    'heatmap',
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


def timeseries(time, data, xlabel='Datum', ylabel='', dateformat='%d.%m.',
               ax=None, **kwargs):
    """Create a basic timeseries plot.

    Parameters:
        time (array): Date array in matplotlib time format.
        data (array): Data array.
        xlabel (str): x label.
        ylabel (str): y label.
        dateformat (str): Format string for date labels on xaxis.
        ax (AxesSubplot): Matplotlib axes.
        **kwargs: Additional keyword arguments passed to `plt.plot`.

    Returns:
        Line2D: A line.
    """
    if ax is None:
        ax = plt.gca()

    line, = ax.plot(time, data, **kwargs)
    set_date_axis(ax, dateformat)

    ax.set_xlim(time.min(), time.max())
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()

    return line


def timeseries2d(time, height, data, xlabel='Datum', ylabel='Höhe [m]',
                 zlabel='', dateformat='%d.%m.', rasterized=True, ax=None,
                 **kwargs):
    """Create a basic 2D timeseries plot.

    Parameters:
        time (array): Date array in matplotlib time format.
        height (array): Height array.
        data (array): Data array.
        xlabel (str): x label.
        ylabel (str): y label.
        zlabel (str): Colorbar label.
        dateformat (str): Format string for date labels on xaxis.
        ax (AxesSubplot): Matplotlib axes.
        **kwargs: Additional keyword arguments passed to `plt.plot`.

    Returns:
        Line2D: A line.
    """
    if ax is None:
        ax = plt.gca()

    def_kwargs = {
        'rasterized': rasterized,
        'cmap': 'viridis',
        }

    def_kwargs.update(kwargs)

    ret = ax.pcolormesh(time, height, data, **def_kwargs)

    cb = ax.get_figure().colorbar(ret)
    cb.set_label(zlabel)

    set_date_axis(ax, dateformat)
    ax.set_xlim(time.min(), time.max())
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    return ret


def heatmap(x, y, bins=20, zlabel='Anzahl', rasterized=True,
            ax=None, **kwargs):
    """Plot a heatmap of given data.

    Parameters:
        x (ndarray): x data.
        y (ndarray): y data.
        bins (None | int | [int, int] | array_like | [array, array]):

            The bin specification:

                - If int, the number of bins for the two dimensions
                (nx=ny=bins).

                - If [int, int], the number of bins in each dimension
                (nx, ny = bins).

                - If array_like, the bin edges for the two dimensions
                (x_edges=y_edges=bins).

                - If [array, array], the bin edges in each dimension
                (x_edges, y_edges = bins).

            The default value is 20.
        zlabel (str): Colobar label.
        ax (AxesSubplot): Axes to plot in.
        **kwargs: Additional keyword argumens passed to `plt.hist2d`.

    Returns:
        Return values of `plt.hist2d`: counts, xedges, yedges, Image.
    """
    if ax is None:
        ax = plt.gca()

    def_kwargs = {
        'bins': bins,
        'rasterized': rasterized,
        'cmap': plt.get_cmap('magma_r', 10),
        }

    def_kwargs.update(kwargs)

    ret = ax.hist2d(x, y, **def_kwargs)

    cb = ax.get_figure().colorbar(ret[3])
    cb.set_label(zlabel)

    return ret
