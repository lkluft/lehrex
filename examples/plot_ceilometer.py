# -*- coding: utf-8 -*-
from os.path import join

import matplotlib.pyplot as plt
import lehrex as lx


# Read back scattering data.
data_dict = lx.csv.read_scat('data/CLB.txt')

# Timeseries
fig, ax = plt.subplots(figsize=(6.5, 4))
lx.plots.timeseries2d(
    data_dict['MPLTIME'],
    data_dict['CLB_MATRIX_Z'],
    data_dict['CLB_MATRIX'],
    dateformat='%H:%M',
    xlabel='Uhrzeit [HH:MM]',
    zlabel='Rückstreuintensität',
    cmap=plt.get_cmap('Blues', 10),
)

fig.savefig(join('plots', 'backscatter.pdf'))
