# -*- coding: utf-8 -*-
"""Common variables and functions.
"""
__all__ = [
    'get_var_desc',
    'get_label',
]


_variable_description = {
    'AH002': ('Absolute Feuchte 2 m', 'g/m³'),
    'ALB': ('Albedo', '1 '),
    'D': ('Diffuse Himmelsstrahlung', 'W/m²'),
    'DD010': ('Windrichtung 10 m', '°'),
    'DR': ('Diffuse Himmelsstrahlung (unkorrigiert)', 'W/m²'),
    'DT002': ('Taupunkt 2 m', '°C'),
    'E': ('Langwellige Strahlung von unten', 'W/m²'),
    'ETS': ('Oberflächentemperatur (mit EPS aus Standortparametern)', '°C'),
    'FB010': ('Stärkste Böen 10 m', 'm/s'),
    'FF010': ('Windgeschwindigkeit 10 m', 'm/s'),
    'G': ('Globalstrahlung', 'W/m²'),
    'GD': ('Diffuse Himmelsstrahlung (aus Globalstrahlung)', 'W/m²'),
    'GI': ('Direkte Sonnenstrahlung (aus Globalstrahlung)', 'W/m²'),
    'GND': ('Sonnenschein nicht möglich (Nacht)', ''),
    'GP': ('Relative Globalstrahlung', '%'),
    'GSD': ('Sonnenscheindetektion', ''),
    'GSH': ('Sonnenscheindauer', 'h'),
    'GSPT': ('Relative Sonnenscheindauer bzgl. 1 Tag', '%'),
    'GSPX': ('Relative Sonnenscheindauer', '%'),
    'GSW': ('Sonnenscheinschwellwert', 'W/m²'),
    'GSZ': ('Summierte Sonnenscheindetektionen', '1'),
    'GTD': ('Schattendetektion', ''),
    'GTH': ('Schattendauer', 'h'),
    'GTZ': ('Summierte Schattendetektionen', '1'),
    'GXD': ('Sonnenschein möglich', ''),
    'GXH': ('Mögliche Sonnenscheindauer', 'h'),
    'GXT': ('Max. mögliche Tagessonnenscheindauer', 'h'),
    'GXZ': ('Summierter möglicher Sonnenschein', '1'),
    'HTD600': ('HMP-Mast Taupunkt, 6 m', '°C'),
    'HTT050': ('HMP-Mast Lufttemperatur, 0,5 m', '°C'),
    'HTT200': ('HMP-Mast Lufttemperatur, 2 m', '°C'),
    'HTT600': ('HMP-Mast Lufttemperatur, 6 m', '°C'),
    'I': ('Direkte Sonnenstrahlung', 'W/m²'),
    'IC': ('Direkte Sonnenstrahlung bei wolkenlosen Bedingungen', 'W/m²'),
    'L': ('Langwellige Strahlung von oben', 'W/m²'),
    'LTS': ('Himmelstemperatur (mit EPS = 1)', '°C'),
    'MG': ('Theoretische Globalstrahlung bei wolkenlosem Himmel', 'W/m²'),
    'MH002': ('Massenmischungsverhältnis 2 m', 'g/kg'),
    'P000': ('Luftdruck (Meereshöhe)', 'hPa'),
    'P007': ('Luftdruck (Stationshöhe)', 'hPa'),
    'PBA': ('Steigwinkel Pilotballon', '°'),
    'PBG': ('Füllgewicht Pilotballon', 'g'),
    'PBW': ('Steiggeschwindigkeit Pilotballon', 'm/min'),
    'Q': ('Strahlungsbilanz', 'W/m²'),
    'R': ('Kurzwellige Strahlung von unten', 'W/m²'),
    'RH002': ('Relative Feuchte 2 m', '%'),
    'RK': ('Niederschlagsmenge ab 0 Uhr', 'mm'),
    'RR': ('Niederschlagsintensität', 'mm'),
    'SH002': ('Spezifische Feuchte 2 m', 'g/kg'),
    'SOLH': ('Höhenwinkel der Sonne', '°'),
    'TT002': ('Lufttemperatur 2 m', '°C'),
    'VP002': ('Wasserdampfdruck 2 m', 'hPa'),
}


def get_var_desc():
    """Get a copy of the default variable description.

    Returns:
        dict: Dict values are tuples containing full variable name and unit.
            The keys are the abbrevations used in `MASTER.txt`.

    Examples:
        Add description for non-default variables:
        >>> desc = lx.plots.get_var_desc()
        >>> desc.update({'FOO': ('New variable', 'Unit')})
        >>> lx.plots.get_label('FOO', var_desc=desc)
        'New variable [Unit]'
    """
    return _variable_description.copy()


def get_label(key, label='{name} [{unit}]', var_desc=None):
    """Return label for variable key.

    Parameters:
        key (str): Variable key.
        label (str): Format string to create the label.
            The variables `name` and `unit` can be used.
        var_desc (dict): Dictionary with variable descriptions.
            The value behind the key has to be a tuple of strings:
                dict[key] = (name, unit)
            If `None` a default set of variables is used.
    Returns:
        str: Variable specific label.

    Examples:
        Get default axis label for variable key "TT002":
        >>> get_label('TT002')
        'Lufttemperature 2 m [K]'

        Pass different format string for label:
        >>> get_label('TT002', label='{name} in {unit}')
        'Lufttemperatur in 2 m in K'

        Set description for non-default variables:
        >>> desc = lx.plots.get_var_desc()
        >>> desc.update({'FOO': ('New variable', 'Unit')})
        >>> get_label('FOO', var_desc=desc)
        'New variable [Unit]'
    """
    if var_desc is None:
        var_desc = _variable_description

    name, unit = var_desc.get(key, (key, ''))

    kwargs = {
        'name': name,
        'unit': unit,
    }
    return label.format(**kwargs)
