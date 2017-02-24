# -*- coding: utf-8 -*-
"""Common variables and functions.

Attributes:
    clear_names (dict): Containing full names for variables
        stored in the `MASTER.txt`.
"""
__all__ = [
    'clear_names',
]


clear_names = {
    'FF010': 'Windgeschwindigkeit 10 m',
    'DD010': 'Windrichtung 10 m',
    'FB010': 'Stärkste Böen 10 m',
    'RR': 'Niederschlagsintensität',
    'RK': 'Niederschlagsmenge ab 0 Uhr',
    'TT002': 'Lufttemperatur 2 m',
    'P007': 'Luftdruck (Stationshöhe)',
    'P000': 'Luftdruck (Meereshöhe)',
    'RH002': 'Relative Feuchte 2 m',
    'DT002': 'Taupunkt 2 m',
    'VP002': 'Wasserdampfdruck 2 m',
    'AH002': 'Absolute Feuchte 2 m',
    'SH002': 'Spezifische Feuchte 2 m',
    'MH002': 'Massenmischungsverhältnis 2 m',
    'G': 'Globalstrahlung',
    'R': 'Kurzwellige Strahlung von unten',
    'L': 'Langwellige Strahlung von oben',
    'E': 'Langwellige Strahlung von unten',
    'Q': 'Strahlungsbilanz',
    'ALB': 'Albedo',
    'ETS': 'Oberflächentemperatur (mit EPS aus Standortparametern)',
    'LTS': 'Himmelstemperatur (mit EPS = 1)',
    'MG': 'Theoretische Globalstrahlung bei wolkenlosem Himmel',
    'GP': 'Relative Globalstrahlung',
    'GXT': 'Max. mögliche Tagessonnenscheindauer',
    'GSW': 'Sonnenscheinschwellwert',
    'GXD': 'Sonnenschein möglich',
    'GND': 'Sonnenschein nicht möglich (Nacht)',
    'GSD': 'Sonnenscheindetektion',
    'GTD': 'Schattendetektion',
    'GSZ': 'Summierte Sonnenscheindetektionen',
    'GSH': 'Sonnenscheindauer',
    'GTZ': 'Summierte Schattendetektionen',
    'GTH': 'Schattendauer',
    'GXZ': 'Summierter möglicher Sonnenschein',
    'GXH': 'Mögliche Sonnenscheindauer',
    'GSPX': 'Relative Sonnenscheindauer',
    'GSPT': 'Relative Sonnenscheindauer bzgl. 1 Tag',
    'SOLH': 'Höhenwinkel der Sonne',
    'IC': 'Direkte Sonnenstrahlung bei wolkenlosen Bedingungen',
    'GI': 'Direkte Sonnenstrahlung (aus Globalstrahlung)',
    'GD': 'Diffuse Himmelsstrahlung (aus Globalstrahlung)',
    'DR': 'Diffuse Himmelsstrahlung (unkorrigiert)',
    'D': 'Diffuse Himmelsstrahlung',
    'I': 'Direkte Sonnenstrahlung',
    'HTT600': 'HMP-Mast Lufttemperatur, 6 m',
    'HTT200': 'HMP-Mast Lufttemperatur, 2 m',
    'HTT050': 'HMP-Mast Lufttemperatur, 0,5 m',
    'HTD600': 'HMP-Mast Taupunkt, 6 m',
    'PBA': 'Steigwinkel Pilotballon',
    'PBW': 'Steiggeschwindigkeit Pilotballon',
    'PBG': 'Füllgewicht Pilotballon',
}
