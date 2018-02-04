# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import lehrex as lex


# Read back scattering data.
df = lex.read('data/CLB.txt')
scattering, z = lex.utils.stack_series(df, regex='CLB_B\d{5}')

# Timeseries
fig, ax = plt.subplots(figsize=(6.5, 4))
lex.plots.timeseries2d(
    df.index, z, scattering,
    dateformat='%H:%M',
    xlabel='Uhrzeit [HH:MM]',
    zlabel='Rückstreuintensität',
    cmap=plt.get_cmap('Blues', 10),
    vmin=0,
    rasterized=True,
)

fig.savefig('plots/backscatter.svg')
