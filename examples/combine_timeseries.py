# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import lehrex as lex


# Read three radiation timeseries into one DataFrame.
df = lex.read('data/MASTER0.txt')
df = lex.read('data/MASTER1.txt', output=df)
df = lex.read('data/MASTER2.txt', output=df)

# Plot timeseries.
fig, ax = plt.subplots()
for v in ['G', 'R', 'L', 'E']:
    lex.plots.timeseries(df, v)
ax.set_ylabel(lex.plots.get_label('G', label='Radianz [{unit}]'))

fig.savefig('plots/radiation_extended.svg')
