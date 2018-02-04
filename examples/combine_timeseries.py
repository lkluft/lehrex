# -*- coding: utf-8 -*-
from os.path import join

import matplotlib.pyplot as plt
import lehrex as lex


# Read three radiation timeseries into one DataFrame.
df = lex.read(join('data', 'MASTER0.txt'))
lex.read(join('data', 'MASTER1.txt'), output=df)
lex.read(join('data', 'MASTER2.txt'), output=df)

# Plot timeseries.
fig, ax = plt.subplots()
for v in ['G', 'R', 'L', 'E']:
    lex.plots.timeseries(df, v)
ax.set_ylabel(lex.plots.get_label(v, label='Radianz [{unit}]'))

fig.savefig(join('plots', 'radiation_extended.svg'))
