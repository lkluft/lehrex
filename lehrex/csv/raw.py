# -*- coding: utf-8 -*-
"""Load CSV files stored in RAW format.
"""
import re
from warnings import warn
from datetime import datetime

import pandas as pd


__all__ = [
    'read_raw',
]


def _parse_starttime(filename):
    """Parse start time from file header and return date string."""
    with open(filename, 'rt', encoding='UTF-8', errors='ignore') as f:
        header = f.readline()

    return re.compile('.*: (.*) UTC.*').match(header).group(1)


def _get_date_range(filename, freq, periods, datefmt='%d.%m.%Y %H:%M:%S,%f'):
    """Return array of datetime objects from file."""
    start = datetime.strptime(_parse_starttime(filename), datefmt)

    return pd.date_range(start, freq=freq, periods=periods)


def read_raw(filename, freq='50ms', decimal=',', delimiter=';', comment='%',
             header=0, output=None, **kwargs):
    """Read file in RAW format.

    Parameters:
        filename (str): Path to CSV file.
        freq (str or pd.DateOffset): Data frequency see `pd.read_csv`.
        decimal (str): Character to recognize as decimal point.
        delimiter (str): The string used to separate values.
        comment (str): The character used to indicate a comment line.
        header (int): Row number to use as the column names.
            See `pd.read_csv` for further information.
        output (pd.DataFrame): DataFrame to append read data to.
        **kwargs: Additional keyword arguments passed to `pd.read_csv`.

    Returns:
        dict: Dictionary containing the data arrays.
    """
    df = pd.read_csv(
        filename,
        comment=comment,
        decimal=decimal,
        delimiter=delimiter,
        header=header,
        **kwargs,
    )

    try:
        # Try to parse the start time from file header.
        df['DATETIME'] = _get_date_range(
            filename, freq=freq, periods=df.shape[0])
    except ValueError:
        # Do not set index, if the regex in `_get_date_range` does not match.
        warn('Could not parse dateformat in file header. No data index set.')
    else:
        # Use date range as index if it is parsed correctly.
        df = df.set_index('DATETIME')

    # Convert structured array to dictionary.
    if output is not None:
        return output.append(df)

    return df
