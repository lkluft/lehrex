# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import lehrex as lex


# Read wind data.
variables = ['W_FF1', 'W_FF3', 'W_FF6']
df = lex.read('data/WERNER.txt')

# Additional variable descriptions.
desc = lex.plots.get_var_desc()
desc.update({
    'W_FF1': ('Windfahne 1', 'm/s'),
    'W_FF3': ('Windfahne 3', 'm/s'),
    'W_FF6': ('Windfahne 6', 'm/s'),
})

# Timeseries
fig, ax = plt.subplots()
for v in variables:
    lex.plots.timeseries(
        df, v, label=lex.plots.get_label(v, label='{name}', var_desc=desc)
    )
ax.set_ylabel('Windstärke [m/s]')

fig.savefig('plots/wind_profile.svg')
