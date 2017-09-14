# -*- coding: utf-8 -*-
"""Python package to support the research during
the annual Lehrexkursion at Universität Hamburg.
"""
from . import csv
from . import math
from . import plots
from . import utils

from .version import __version__


__all__ = [
    'csv',
    'math',
    'plots',
    'utils',
]
