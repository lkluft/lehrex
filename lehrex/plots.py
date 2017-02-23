# -*- coding: utf-8 -*-
"""Plot basic atmospheric properties conveniently.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import typhon.cm


__all__ = ['set_date_axis',
           'time_series',
           'plot_clb',
           'plot_lwr',
           'plot_T_b',
           'plot_back_scat',
           'heatmap',
           ]


def set_date_axis(ax=None, dateformat='%d.%m.'):
    """Set DateFormatter for given AxesSubplot."""
    formatter = mpl.dates.DateFormatter(dateformat)
    ax.xaxis.set_major_formatter(formatter)
    ax.grid('on', which='both', linestyle='-')


def time_series(data, key, ylabel='', nticks=10, ax=None, **kwargs):
    """Create a basic timeseries plot.

    Notes:
        The passed dictionary is expected to store a np.ndarray containing date
        and time information in matplotlib time format. This information has
        to be accessible through the key 'MPLTIME'.

    Parameters:
        data (dict): Dictionary containing time and data.
        key (str): Dictionary key of variable to plot.
            If key is a list of keys, each element in plotted.
        ylabel (str): y label.
        nticks (int): Maximum number of xticks.
        ax (AxesSubplot): Matplotlib axes.

    Returns:
        Line2D: A line.

    """
    if type(key) is list:
        line = []
        for k in key:
            line.append(time_series(data, k, ylabel=ylabel, ax=ax, **kwargs))
        return line

    if ax is None:
        ax = plt.gca()

    if 'label' not in kwargs:
        kwargs['label'] = key

    date = data['MPLTIME']

    line, = ax.plot(date, data[key], **kwargs)

    set_date_axis(ax)

    ax.set_xlim(date.min(), date.max())
    xticks = np.arange(np.floor(date.min()), np.ceil(date.max()))
    # TODO: Sometimes `nticks + 1` labels are generated.
    if xticks.size > nticks:
        ax.xaxis.set_minor_locator(mpl.ticker.FixedLocator(xticks))
        ax.set_xticks(xticks[::xticks.size//nticks])
    ax.set_xlabel('Datum')
    ax.set_ylabel(ylabel)
    ax.legend()

    return line


def plot_clb(data, key='CBH', detection_height=2300, ax=None, **kwargs):
    """Plot cloud base height time series.

    Parameters:
        data (dict): Dictionary containing time and data.
        detection_height (float): Maximal detection height.
        ax (AxesSubplot): Matplotlib axes.

    """
    ylabel = 'Höhe [m]'

    line = time_series(data, key,
                       ax=ax,
                       ylabel=ylabel,
                       color='darkorange',
                       alpha=0.7,
                       linewidth=2,
                       label='Abgeleitete Wolkenhöhe',
                       **kwargs)

    # data['DETECTION_HEIGHT'] = detection_height * np.ones(data['MPLTIME'].size)
    # time_series(data, 'DETECTION_HEIGHT',
    #             ax=ax,
    #             ylabel=ylabel,
    #             color='darkred',
    #             alpha=0.7,
    #             linewidth=2,
    #             linestyle='--',
    #             label='Max. Detektionshöhe')

    ax.legend()

    return line


def plot_lwr(data, key='L', ax=None, **kwargs):
    """Plot LWR time series.

    Parameters:
        data (dict): Dictionary containing time and data.
        ax (AxesSubplot): Matplotlib axes.

    Returns:
        Line2D: A line.

    """
    ylabel = r'Langwellige Rückstrahlung [$W\,m^{-2}$]'

    line = time_series(data, key, ylabel, ax=ax, **kwargs)

    return line


def plot_T_b(data, key='L', ax=None, **kwargs):
    """Plot brightness temperature time series.

    Parameters:
        data (dict): Dictionary containing time and data.
        ax (AxesSubplot): Matplotlib axes.

    Returns:
        Line2D: A line.

    """
    ylabel = r'$\Delta T_B$ [K]'
    color = 'darkred'

    line = time_series(data, key, ylabel, ax=ax, color=color, **kwargs)

    return line


def plot_back_scat(date, z, back_scat, ax=None):
    """Create a basic timeseries plot of ceilometer scattering profiles.

    Parameters:
        date (np.array): Dates in matplotlib format.
        z (np.array): Height level data array.
        back_scat (np.array): Ceilometer back scattering coefficients.
        ax (AxesSubplot): Matplotlib axes.

    Returns:
        QuadMesh, Colorbar

    """
    if ax is None:
        ax = plt.gca()

    pcm = ax.pcolormesh(date, z, back_scat,
                        cmap=plt.get_cmap('density', lut=8),
                        vmin=0,
                        vmax=400,
                        rasterized=True)

    ax.set_ylim(0, 4000)
    ax.set_yticks(np.arange(0, 4001, 1000))
    ax.set_yticks(np.arange(0, 4001, 500), minor=True)
    set_date_axis(ax)

    cb = ax.get_figure().colorbar(pcm)
    cb.set_ticks(np.arange(0, 401, 100))
    cb.set_label('Rückstreuintensität des Ceilometers')

    return pcm, cb


def heatmap(x, y, nbins=(10, 10), cmap='cubehelix_r',
            rasterized=True, ax=None, **kwargs):
    """Plot a heatmap of given data.

    Parameters:
        x (np.ndarray): x data.
        y (np.ndarray): y data.
        nbins (tuple[int]): Number of bins in both dimensions.
        ax (AxesSubplot, optional): Axes to plot in.

    Returns:
        N, xedges, yedges, AxesImage

    """
    if ax is None:
        ax = plt.gca()

    ret = ax.hist2d(
        x, y, nbins, cmap=cmap, rasterized=rasterized, **kwargs)

    return ret
