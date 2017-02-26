# lehrex
Python package to support the research during the annual Lehrexkursion at
Universität Hamburg.

## Structure
* `lehrex.csv`: Functions to read and write common files (e.g. `MASTER.txt`).
* `lehrex.math`: Basic statistical functions (e.g. `moving_average`, `rmse`).
* `lehrex.plots`: General plotting routines like timeseries or heatmaps.

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
