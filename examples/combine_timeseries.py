# -*- coding: utf-8 -*-
from os.path import join

import matplotlib.pyplot as plt
import lehrex as lx


# Read three radiation timeseries.
d0 = lx.csv.read('data/MASTER0.txt')
d1 = lx.csv.read('data/MASTER1.txt')
d2 = lx.csv.read('data/MASTER2.txt')

# Combine timeseries.
data_dict = lx.utils.stack_dicts(d0, d1, d2)

# Timeseries
fig, ax = plt.subplots()
for v in ['G', 'R', 'L', 'E']:
    lx.plots.timeseries(
        data_dict['MPLTIME'],
        data_dict[v],
        ylabel=lx.plots.get_label(v, label='Radianz {unit}'),
        label=lx.plots.get_label(v, label='{name}'),
        )

fig.savefig(join('plots', 'radiation_extended.pdf'))
