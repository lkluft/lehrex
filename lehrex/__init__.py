# -*- coding: utf-8 -*-
"""Support the research during the annual Lehrexkursion at Universität Hamburg.
"""
from os.path import dirname, join

from .csv import *
from . import plots
from . import utils


__all__ = [s for s in dir() if not s.startswith('_')]
__version__ = open(join(dirname(__file__), 'VERSION')).read().strip()
