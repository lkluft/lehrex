# -*- coding: utf-8 -*-
"""This package provides modules and functions to estimate the
cloud base height (CLB) by measuring the downward longwave radiation.

"""
import numpy as np

from . import csv
from . import math
from . import physics
from . import plots


__all__ = ['csv',
           'math',
           'physics',
           'plots',
           'estimate_cloud_height',
           'delta_Tb',
           'lwr_surrounding',
           ]


def estimate_cloud_height(lwr, T_s, lapse_rate=-0.0065):
    """Estimate the cloud base height from LWR and 2m temperature.

    Parameters:
        lwr (np.array): LWR.
        T_s (np.array): Near-surface temperature.
        lapse_rate (float): Vertical temperature gradient.

    Returns:
        np.array: Estimated cloud base height.

    """
    return delta_Tb(lwr, T_s) / lapse_rate


def delta_Tb(lwr, T_s):
    """Calculate the difference between measured spectrum and Planck.

    Parameters:
        lwr: Measure longwave radiation [Wm**-2].
        T: Surface temperature [K].

    Returns:
        Integrated spectrum difference [K].

    """
    a = physics.irradiance2temperature(lwr)
    b = physics.irradiance2temperature(lwr_surrounding(T_s))
    return a - b


def lwr_surrounding(T):
    """Calculate the integrated radiances for a pyrgeoemter.

    A pyrgeoemter measures the atmospheric infra-red radiation spectrum.
    We assume that it is sensitive to frequencies between 3 THz and 60 THz.

    Parameters:
        T (np.array): Near surface temperature.

    Returns:
        np.array: Integrated radiances for a simplified pyrgeoemter.

    """
    f = np.linspace(3e12, 60e12, 1000)

    return physics.irradiance(f, T)
