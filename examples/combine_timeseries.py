# -*- coding: utf-8 -*-
import glob

import matplotlib.pyplot as plt
import lehrex as lex
import pandas as pd


# Read three input files and concatenate them to one DataFrame.
df = pd.concat(map(lex.read, glob.iglob('data/MASTER*.txt')))

# Plot timeseries.
fig, ax = plt.subplots()
for v in ['G', 'R', 'L', 'E']:
    lex.plots.timeseries(df, v)
ax.set_ylabel(lex.plots.get_label('G', label='Radianz [{unit}]'))

fig.savefig('plots/radiation_extended.svg')
