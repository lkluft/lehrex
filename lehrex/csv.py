# -*- coding: utf-8 -*-
"""Load CSV files stored in Wettermast format.
"""
import re

from matplotlib.dates import strpdate2num
import numpy as np


__all__ = ['read',
           'read_profile',
           'read_scat',
           'write_dict',
           ]


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
    """Get variable names from CSV file.

    Parameters:
        filename (str): Path to CSV file.

    Returns:
        str: Comma separated list of variable names.
    """
    with open(filename, "rb") as f:
        for line in f:
            if line.decode().startswith('$Names='):
                return line.decode().split('=')[1].replace(';', ',').strip()


def _get_dtype(variable):
    """Define dtypes for variables in CSV files.

    Parameters:
        variable (str): Variable name.

    Returns:
        str: dtype of given variable.
    """
    variable_dtypes = {
            'DATE': '<U10',
            'TIME': '<U5',
            }

    if variable in variable_dtypes:
        dtype = variable_dtypes[variable]
    else:
        dtype = 'f8'

    return dtype


#TODO: The whole stacking functionality is extremely buggy. There are a lot of
# cases where stacking should not be done (e.g. height levels). Currently there
# is no proper way to avoid this.
def read(filename, variables=None, stack=True,
         exclude_stack=None, output=None):
    """Read CSV files.

    Parameters:
        filename (str): Path to CSV file.
        variables (List[str]): List of variables to extract.
        stack (bool): Stack dict entries if key already exists.
        exclude_stack (list[str]): Variables that should not be stacked
            (e.g.  'PROFILE_Z').
        output (dict): Dictionary that is updated with read data.

    Returns:
        dict: Dictionary containing the data arrays.

    """
    names = _get_names(filename)
    dtype = [(n, _get_dtype(n)) for n in names.split(',')]

    # Read DATE and TIME even if they are not explicitly listed.
    if variables is not None:
        usecols = list(set(variables + ['DATE', 'TIME']))
    else:
        variables = names.split(',')
        usecols = None

    if exclude_stack is None:
        exclude_stack = []

    with open(filename, 'rb') as f:
        data = np.genfromtxt(
            f,
            delimiter=';',
            skip_header=7,
            dtype=dtype,
            names=names,
            usecols=usecols,
            )

    # Convert structured array to dictionary.
    if output is None:
        output = {var: data[var] for var in variables}
    else:
        for var in variables:
            if stack is True and var in output and var not in exclude_stack:
                output[var] = np.hstack((output[var], data[var]))
            else:
                output[var] = data[var]

    # Always convert DATE and TIME into matplotlib time.
    dates = [' '.join(d) for d in zip(data['DATE'], data['TIME'])]
    if (stack and 'MPLTIME' in output and 'MPLTIME' not in exclude_stack):
        # Only stack MPLTIME if it is already there and not permitted.
        output['MPLTIME'] = np.hstack(
            (output['MPLTIME'], _get_mpl_date(dates)))
    else:
        output['MPLTIME'] = _get_mpl_date(dates)

    return output


def read_profile(filename, dz=10, var_regex=None, var_key='PROFILE',
                 stack=True, exclude_stack=None, output=None):
    """Read scattering coefficients from CSV file.

    Parameters:
        filename (str): Path to CSV file.
        output (dict): Dictionary that is updated with read data.
        dz (float): Height resolution.
        var_regex (str): Python regular expression [0] matching
            the variable name of the profile.
        var_key (str): Dictionary key for extracted profile.

    [0] https://docs.python.org/3.1/library/re.html

    Returns:
        np.ndarray: Profile.

    """
    profile_key = var_key + '_Z'

    if exclude_stack is None:
        exclude_stack = []

    exclude_stack.append(profile_key)

    output = read(
        filename,
        stack=stack,
        exclude_stack=exclude_stack,
        output=output,
        )

    p = re.compile(var_regex)

    var_names = [var for var in output.keys() if p.match(var)]
    var_names.sort()

    profile = np.vstack([output[v] for v in var_names])

    z = [float(re.sub('[^0-9]', '', v)) for v in var_names]

    # Extract height information from variable name.
    output[var_key] = np.ma.masked_invalid(profile)
    output[profile_key] = np.array(z)

    return output


def read_scat(filename, var_regex='CLB_B\d{5}', output=None):
    """Read scattering coefficients from CSV file.

    Parameters:
        filename (str): Path to CSV file.
        output (dict): Dictionary that is updated with read data.
        dz (float): Height resolution of the ceilometer.
        scat_name (str): Python regular expression [0] matching
            the variable name of the scattering coefficients.

    [0] https://docs.python.org/3.1/library/re.html

    Returns:
        np.array, np.array: scattering coefficient, height levels

    """

    output = read_profile(
        filename,
        stack=False,
        var_key='CLB_MATRIX',
        var_regex=var_regex,
        output=output)

    back_scat = output['CLB_MATRIX']
    back_scat = np.ma.masked_less(back_scat, 0)

    output['CLB_MATRIX'] = back_scat

    return output


def write_dict(filename, data, variables=None):
    """Write data from dictionary to CSV file.

    Parameters:
        filename (str): Path to CSV file.
        data (dict): Dictionary containing data.
        variables (list[str]): Variables to store (default: all).

    """
    if variables is None:
        variables = list(sorted(data.keys()))
        # Write date and time to first columns.
        for k in ['TIME', 'DATE']:
            if k in variables:
                variables.remove(k)
                variables.insert(0, k)

    header = '$Names=' + ";".join(variables)
    data = np.vstack(data[v] for v in variables).T

    np.savetxt(
            filename,
            data,
            comments='',
            delimiter=';',
            header=header,
            fmt='%s')
