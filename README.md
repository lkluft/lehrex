# lehrex
Python package to support the research during the annual Lehrexkursion at
Universität Hamburg.

## Structure
* `lehrex.csv`: Functions to read and write common files (e.g. `MASTER.txt`).
* `lehrex.math`: Basic statistical functions (e.g. `moving_average`, `rmse`).
* `lehrex.plots`: General plotting routines like timeseries or heatmaps.

## Installation
For standard Python installations, install `lehrex` using `pip`:
```bash
pip install lehrex
```

If you want to do local changes to the package, you can install the cloned
repository. In the root directory type:
```bash
pip install --user --no-deps -e .
```
