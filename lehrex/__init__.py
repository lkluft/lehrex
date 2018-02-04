# -*- coding: utf-8 -*-
"""Python package to support the research during
the annual Lehrexkursion at Universität Hamburg.
"""
from os.path import dirname, join

from . import csv
from .csv import (read, write)
from . import math
from . import plots
from . import utils


__version__ = open(join(dirname(__file__), 'VERSION')).read().strip()

__all__ = [
    'csv',
    'math',
    'plots',
    'read',
    'write',
    'utils',
]
