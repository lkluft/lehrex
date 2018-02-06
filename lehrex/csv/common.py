# -*- coding: utf-8 -*-
"""Load CSV files stored in Wettermast format.
"""
import re
from datetime import datetime

import numpy as np
import pandas as pd
from matplotlib.dates import strpdate2num


__all__ = [
    'read',
    'write',
]


def _get_mpl_date(dates, fmt='%d.%m.%Y %H:%M'):
    """Convert date strings into matplotlib time format.

    Parameters:
        dates (ndarray): Array containing date strings.
        fmt (str): Date string format [0].

    [0] http://pubs.opengroup.org/onlinepubs/009695399/functions/strptime.html

    Returns:
        np.array: Matplotlib time values.
    """
    return np.array([strpdate2num(fmt)(d) for d in dates])


def _get_datetime(dataframe):
    """Convert 'DATE' and 'TIME' columns into list of datetime objects."""
    return [datetime.strptime(' '.join([d, t]), '%d.%m.%Y %H:%M')
            for d, t in zip(dataframe['DATE'], dataframe['TIME'])]


def _get_names(filename):
    """Return list of variable names."""
    with open(filename, "rb") as f:
        for line in f:
            if line.decode().startswith('$Names='):
                return line.decode().split('=')[1].strip().split(';')
    raise Exception('No field names were found.')


def _get_skip_header(filename):
    """Return number of lines to skip at the beginning of the file."""
    with open(filename, 'rb') as f:
        for i, line in enumerate(f):
            if (not line.decode().startswith('$') and
                not line.decode().startswith('#')):
                # Return number of first non-comment line.
                return i

    raise Exception('No valid line found.')


def read(filename, delimiter=';', **kwargs):
    """Read CSV file into DataFrame.

    Parameters:
        filename (str): Path to CSV file.
        delimiter (str): The string used to separate values.
        **kwargs: Additional keyword arguments passed to `pd.read_csv`.

    Returns:
        pd.DataFrame: DataFrame representing the timeseries.
    """
    # Parse CSV file and create `pandas.DataFrame`.
    df = pd.read_csv(
        filename,
        delimiter=delimiter,
        skiprows=_get_skip_header(filename),
        names=_get_names(filename),
        **kwargs,
    )

    # Convert 'DATE' and 'TIME' columns into datetime objects and use them
    # as DataFrame index.
    df['DATETIME'] = _get_datetime(df)
    df = df.set_index('DATETIME')

    return df


def write(filename, data, variables=None):
    """Write data from dictionary to CSV file.

    Parameters:
        filename (str): Path to CSV file.
        data (pd.Dataframe or dict-like): DataFrame or dict-like.
        variables (list[str]): Variables to store.
    """
    if not ('DATE' in data and 'TIME' in data):
        raise Exception('Need DATE and TIME column to write proper files.')

    if variables is None:
        variables = list(sorted(data.keys()))

    # Write date and time to first columns.
    for k in ['TIME', 'DATE']:
        if k in variables:
            variables.remove(k)
        variables.insert(0, k)

    # Convert dictionart entries to data matrix.
    data_matrix = np.vstack(data[v] for v in variables).T

    # Calculate some time statistics in Wettermast style.
    # It looks messy and it is not clear, if those values are needed.
    # But the results arer equivalent to the original files.
    base_date = '27.03.1995 00:00:00'
    dates = [' '.join(d) for d in zip(data['DATE'], data['TIME'])]
    first_date = dates[0] + ':00'
    mpl_times = _get_mpl_date([base_date, first_date], fmt='%d.%m.%Y %H:%M:%S')
    secs_since = np.diff(mpl_times) * 24 * 3600  # time span in seconds
    time_lag = np.round(np.mean(np.diff(_get_mpl_date(dates) * 24 * 3600)))

    # Combine time properties to file header.
    header = '#={}\n'.format(data_matrix.shape[0])
    header += '$FirstDateTime={}\n'.format(first_date)
    header += '$JSDBaseDateTime={}\n'.format(base_date)
    header += '$FirstJSD={}\n'.format(int(secs_since))
    header += '$TimeLagSec={}\n'.format(int(time_lag))
    header += '$DefaultValue=99999\n'
    header += '$Names=' + ";".join(variables)

    np.savetxt(
        filename,
        data_matrix,
        comments='',
        delimiter=';',
        header=header,
        fmt='%s',
    )
