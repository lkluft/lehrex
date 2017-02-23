# -*- coding: utf-8 -*-
"""Load CSV files stored in Wettermast format.

Attributes:
    variable_dtypes (dict): Stores the dtype related to a variable name.
"""
import re

from matplotlib.dates import strpdate2num
import numpy as np


__all__ = [
    'read',
    'read_profile',
    'read_scat',
    'write',
]

variable_dtypes = {
    'DATE': '<U10',
    'TIME': '<U5',
}


def _get_mpl_date(dates, fmt='%d.%m.%Y %H:%M'):
    """Convert date strings into matplotlib time format.

    Parameters:
        dates (np.array): Array containing date strings.
        fmt (str): Date string format [0].

    [0] http://pubs.opengroup.org/onlinepubs/009695399/functions/strptime.html

    Returns:
        np.array: Matplotlib time values.
    """
    return np.array([strpdate2num(fmt)(d) for d in dates])


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


def read(filename, variables=None, delimiter=';', output=None):
    """Read CSV files.

    Parameters:
        filename (str): Path to CSV file.
        variables (List[str]): List of variables to extract.
        delimiter (str): The string used to separate values.
        output (dict): Dictionary that is updated with read data.

    Returns:
        dict: Dictionary containing the data arrays.
    """
    names = _get_names(filename)
    skip_header = _get_skip_header(filename)
    dtype = [(n, variable_dtypes.get(n, 'f8')) for n in names.split(',')]

    # Read DATE and TIME even if they are not explicitly listed.
    if variables is not None:
        usecols = list(set(variables + ['DATE', 'TIME']))
    else:
        variables = names.split(',')
        usecols = None

    with open(filename, 'rb') as f:
        data = np.genfromtxt(
            f,
            delimiter=delimiter,
            skip_header=skip_header,
            dtype=dtype,
            names=names,
            usecols=usecols,
            )

    # Convert structured array to dictionary.
    if output is None:
        output = {var: data[var] for var in variables}
    else:
        for var in variables:
            output[var] = data[var]

    # Always convert DATE and TIME into matplotlib time.
    dates = [' '.join(d) for d in zip(data['DATE'], data['TIME'])]
    output['MPLTIME'] = _get_mpl_date(dates)

    return output


def read_profile(filename, var_regex=None, var_key='PROFILE', output=None):
    """Read scattering coefficients from CSV file.

    Parameters:
        filename (str): Path to CSV file.
        output (dict): Dictionary that is updated with read data.
        var_regex (str): Python regular expression [0] matching
            the variable name of the profile.
        var_key (str): Dictionary key for extracted profile.

    [0] https://docs.python.org/3.1/library/re.html

    Returns:
        np.ndarray: Profile.
    """
    profile_key = var_key + '_Z'

    output = read(filename, output=output)

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
              output=None):
    """Read scattering coefficients from CSV file.

    Parameters:
        filename (str): Path to CSV file.
        output (dict): Dictionary that is updated with read data.
        scat_name (str): Python regular expression [0] matching
            the variable name of the scattering coefficients.

    [0] https://docs.python.org/3.1/library/re.html

    Returns:
        np.array, np.array: scattering coefficient, height levels
    """
    output = read_profile(
        filename,
        var_key=var_key,
        var_regex=var_regex,
        output=output,
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
    if variables is None:
        variables = list(sorted(data.keys()))
        # Write date and time to first columns.
        for k in ['TIME', 'DATE']:
            if k in variables:
                variables.remove(k)
                variables.insert(0, k)

    # TODO: Create full header information.
    header = '$Names=' + ";".join(variables)
    data = np.vstack(data[v] for v in variables).T

    np.savetxt(
        filename,
        data,
        comments='',
        delimiter=';',
        header=header,
        fmt='%s',
        )
