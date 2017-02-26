# -*- coding: utf-8 -*-
"""Common variables and functions.

Attributes:
    variable_description (dict): Containing long names and units for variables.
        The keys are the abbrevations used in `MASTER.txt`. The return value is
        a tuple of strings `(name, unit)`.
"""
__all__ = [
    'variable_description',
    'get_label',
]


variable_description = {
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


def get_label(key, label='{name} [{unit}]'):
    """Return label for variable key.

    Parameters:
        key (str): Variable key.
        label (str): Format string to create the label.
            The variables `name` and `unit` can be used.
    Returns:
        str: Variable specific label.

    Examples:
        >>> get_label('TT002')
        'Lufttemperature 2 m [K]'

        >>> get_label('TT002', label='{name} in {unit}')
        'Lufttemperatur in 2 m in K'

    """
    name, unit = variable_description.get(key, (key, ''))

    kwargs = {
        'name': name,
        'unit': unit,
    }
    return label.format(**kwargs)
