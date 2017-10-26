# -*- coding: utf-8 -*-
from os.path import join

import matplotlib.pyplot as plt
import lehrex as lx


# Read radiation data.
data_dict = lx.csv.read('data/MASTER1.txt')

# Timeseries
fig, ax = plt.subplots()
for v in ['G', 'R', 'L', 'E']:
    lx.plots.timeseries(
        data_dict['MPLTIME'],
        data_dict[v],
        ylabel=lx.plots.get_label(v, label='Radianz {unit}'),
        label=lx.plots.get_label(v, label='{name}'),
        )

fig.savefig(join('plots', 'radiation.svg'))
