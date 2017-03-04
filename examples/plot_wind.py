# -*- coding: utf-8 -*-
from os.path import join
import matplotlib.pyplot as plt
import lehrex as lx


# Read wind data.
variables = ['W_FF1', 'W_FF3', 'W_FF6']
data_dict = lx.csv.read('data/WERNER.txt')

# Additional variable descriptions.
desc = lx.plots.get_var_desc()
desc.update({
    'W_FF1': ('Windfahne 1', 'm/s'),
    'W_FF3': ('Windfahne 3', 'm/s'),
    'W_FF6': ('Windfahne 6', 'm/s'),
})

# Timeseries
fig, ax = plt.subplots()
for v in variables:
    lx.plots.timeseries(
        data_dict['MPLTIME'],
        data_dict[v],
        ylabel='Windstärke [m/s]',
        label=lx.plots.get_label(v, label='{name}', var_desc=desc),
        )

fig.savefig(join('plots', 'wind_profile.pdf'))
