# -*- coding: utf-8 -*-
from os.path import join

import matplotlib.pyplot as plt
import lehrex as lex


# Read radiation data.
df = lex.read(join('data', 'MASTER1.txt'))

# Timeseries
fig, ax = plt.subplots()
for v in ['G', 'R', 'L', 'E']:
    lex.plots.timeseries(df, v)
ax.set_ylabel(lex.plots.get_label(v, label='Radianz [{unit}]'))

fig.savefig(join('plots', 'radiation.svg'))
