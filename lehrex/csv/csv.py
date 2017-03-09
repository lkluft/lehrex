# -*- coding: utf-8 -*-
"""Load CSV files stored in Wettermast format.
"""
import re
from warnings import warn

from matplotlib.dates import strpdate2num
import numpy as np


__all__ = [
    'read',
    'read_profile',
    'read_scat',
    'write',
]

VARIABLE_DTYPES = {
    'DATE': '<U10',
    'TIME': '<U5',
}


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


def _get_default_value(filename):
    """Get default value for missing data from CSV file header.

    Parameters:
        filename (str): Path to CSV file.

    Returns:
        float or str: Default value for mising values.
    """
    with open(filename, "rb") as f:
        for line in f:
            if line.decode().startswith('$DefaultValue='):
                default = line.decode().split('=')[1]
                try:
                    return int(default)
                except:
                    return default
        return np.nan


def _get_names(filename):
    """Get variable names from CSV file header.

    Parameters:
        filename (str): Path to CSV file.

    Returns:
        str: Comma separated list of variable names.
    """
    with open(filename, "rb") as f:
        for line in f:
            if line.decode().startswith('$Names='):
                return line.decode().split('=')[1].replace(';', ',').strip()
    raise Exception('No field names were found.')


def _get_skip_header(filename):
    """Get number of lines to skip header of CSV file.

    Parameters:
        filename (str): Path to CSV file.

    Returns:
        int: Number of lines to skip at the beginning of the file.
    """
    i = 0
    with open(filename, 'rb') as f:
        for line in f:
            if line.decode()[0] == '$' or line.decode()[0] == '#':
                i += 1
            else:
                return i
    raise Exception('No valid line found.')


def read(filename, variables=None, delimiter=';', filling_values=np.nan,
         output=None, **kwargs):
    """Read CSV files.

    Parameters:
        filename (str): Path to CSV file.
        variables (List[str]): List of variables to extract.
        delimiter (str): The string used to separate values.
        filling_values (float): Value to use for missing values.
            If `None`, use the `DefaultValue` specified in file header.
        output (dict): Dictionary that is updated with read data.
        **kwargs: Additional keyword arguments passed to `np.genfromtxt`.

    Returns:
        dict: Dictionary containing the data arrays.
    """
    skip_header = _get_skip_header(filename)
    names = _get_names(filename)
    dtype = [(n, VARIABLE_DTYPES.get(n, 'f8')) for n in names.split(',')]
    if filling_values is None:
        filling_values = _get_default_value(filename)

    if variables is None:
        variables = names.split(',')

    with open(filename, 'rb') as f:
        data = np.genfromtxt(
            f,
            delimiter=delimiter,
            skip_header=skip_header,
            dtype=dtype,
            names=names,
            filling_values=filling_values,
            usecols=variables,
            **kwargs,
            )

    # Convert structured array to dictionary.
    if output is None:
        output = {var: data[var] for var in variables}
    else:
        for var in variables:
            output[var] = data[var]

    # If present, convert DATE and TIME into matplotlib time.
    if 'DATE' in output and 'TIME' in output:
        dates = [' '.join(d) for d in zip(data['DATE'], data['TIME'])]
        output['MPLTIME'] = _get_mpl_date(dates)
    else:
        warn('It is highly recommended to read the DATE and TIME variables!')

    return output


def read_profile(filename, var_regex=None, var_key='PROFILE', **kwargs):
    """Read scattering coefficients from CSV file.

    Parameters:
        filename (str): Path to CSV file.
        var_regex (str): Python regular expression [0] matching
            the variable name of the profile.
        var_key (str): Dictionary key for extracted profile.
        **kwargs: Additional keyword arguments passed to `read`.

    [0] https://docs.python.org/3.1/library/re.html

    Returns:
        dict: Dictionary containing the data arrays and the stacked profile.
    """
    profile_key = var_key + '_Z'

    output = read(filename, **kwargs)

    p = re.compile(var_regex)

    var_names = [var for var in output.keys() if p.match(var)]
    var_names.sort()

    profile = np.vstack([output[v] for v in var_names])

    z = [float(re.sub('[^0-9]', '', v)) for v in var_names]

    # Extract height information from variable name.
    output[var_key] = np.ma.masked_invalid(profile)
    output[profile_key] = np.array(z)

    return output


def read_scat(filename, var_regex='CLB_B\d{5}', var_key='CLB_MATRIX',
              **kwargs):
    """Read scattering coefficients from CSV file.

    Parameters:
        filename (str): Path to CSV file.
        var_regex (str): Python regular expression [0] matching
            the variable name of the profile.
        var_key (str): Dictionary key for extracted profile.
        **kwargs: Additional keyword arguments passed to `read_profile`.

    [0] https://docs.python.org/3.1/library/re.html

    Returns:
        ndarray, ndarray: scattering coefficient, height levels
    """
    output = read_profile(
        filename,
        var_key=var_key,
        var_regex=var_regex,
        **kwargs,
        )

    back_scat = output[var_key]
    back_scat = np.ma.masked_less(back_scat, 0)

    output[var_key] = back_scat

    return output


def write(filename, data, variables=None):
    """Write data from dictionary to CSV file.

    Parameters:
        filename (str): Path to CSV file.
        data (dict): Dictionary containing data.
        variables (list[str]): Variables to store.
    """
    if not ('DATE' in data and 'TIME' in data):
        raise Exception('Need DATE and TIME to write proper files.')

    if variables is None:
        variables = list(sorted(data.keys()))
        # Write date and time to first columns.
        for k in ['TIME', 'DATE']:
            if k in variables:
                variables.remove(k)
                variables.insert(0, k)

    # Never write MPLTIME. It is created when reading anyways.
    variables.remove('MPLTIME')

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
