# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import lehrex as lex


# Read three input files and concatenate them to one DataFrame.
df = lex.read_mfdataset('data/MASTER*.txt')

# Plot timeseries.
fig, ax = plt.subplots()
for v in ['G', 'R', 'L', 'E']:
    lex.plots.timeseries(df, v)
ax.set_ylabel(lex.plots.get_label('G', label='Radianz [{unit}]'))

# fig.savefig('plots/radiation_extended.svg')
plt.show()
