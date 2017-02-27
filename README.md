# lehrex
Python package to support the research during the annual Lehrexkursion at
Universität Hamburg.

## Table of Contents
* [Installation](#installation)
  * [Stable release](#stable-release)
  * [Development](#development)
* [Package structure](#package-structure)
* [Examples](#examples)
    * [Reading files](#reading-files)
    * [Plotting a timeseries](#plotting-a-timeseries)

## Installation
### Stable release
For standard Python installations, install the latest stable version using `pip`:
```bash
pip install lehrex
```

### Development
If you want to do changes to the package, clone the repository and install the
package locally:
```bash
git clone https://github.com/lkluft/lehrex.git
cd lehrex
pip install --user --no-deps -e .
```

## Package structure
* `lehrex.csv`: Functions to read and write common files (e.g. `MASTER.txt`).
* `lehrex.math`: Basic statistical functions (e.g. `moving_average`, `rmse`).
* `lehrex.plots`: General plotting routines like timeseries or heatmaps.

## Examples
### Reading files
```python
import lehrex as lx

data = lx.csv.read('MASTER.txt')
```

### Plotting a timeseries
```python
import matplotlib.pyplot as plt
import lehrex as lx


# Read radiation data.
variables = ['G', 'R', 'L', 'E']
data_dict = lx.csv.read('data/MASTER.txt')

# Plot timeseries.
fig, ax = plt.subplots()
for v in variables:
    lx.plots.timeseries(
        data_dict['MPLTIME'],
        data_dict[v],
        ylabel=lx.plots.get_label(v, label='Radianz {unit}'),
        label=lx.plots.get_label(v, label='{name}'),
        )

plt.show()
```
![Radiation](/doc/plots/radiation.png)
