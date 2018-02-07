#!/bin/python3
# -*- coding: utf-8 -*-

'''
This script may be used to...
Or to process a file with a record of start and end times as well as breaks.
In a linux environment this may be called using
cat example-arbeitszeiten.csv | awk '{ $1=""; print}' | sed -e 's/,//g' \
| sed -e 's/\"Gleitzeit\"//g;s/\"Feiertag\"//g;s/\"Urlaub\"//g;s/\"Krank\"//g' \
| python arbeit-cli
'''

import sys
import os.path
import argparse


def eprint(*args, **kwargs):
    '''
    Print to stderr
    '''
    print(*args, file=sys.stderr, **kwargs)


def is_valid_file(parser_instanz, arg):
    '''
    Prüfe, ob arg eine valide Datei ist
    '''
    if not os.path.exists(arg):
        parser_instanz.error("The file %s does not exist!" % arg)
    return open(arg, 'r')  # return an open file handle


try:
    import libarbeitszeiten as liba
except ImportError:
    eprint('Could not import module libarbeitszeiten. \
Check, if libarbeitszeiten.py is available in this dir.')

__version__ = '0.1'

def create_parser():
    '''
    Parser  für CLI bauen
    '''
    parser_objekt = argparse.ArgumentParser(
        description='Berechne Arbeitszeiten oder schlage gesetzeskonforme Arbeitszeiten vor',
        prog='arbeitcli',
        prefix_chars='-/')

    parser_objekt.add_argument(
        'zeitwerte', nargs='*',
        default=sys.stdin,
        metavar="Zeitwerte",
        help='Zeitwerte als Berechnungsgrundlage')

    parser_objekt.add_argument(
        '--datei',
        dest='dateiname',
        required=False,
        metavar="Dateiname",
        type=lambda x: is_valid_file(parser_objekt, x),
        help='Datei oder stdin als Eingabemethode für Zeitwerte')

    parser_objekt.add_argument(
        '-t', type=str, required=False,
        default=liba.TAGESARBEITSMINUTEN,
        help='Gesamte Arbeitszeit des Tages in Minuten')

    parser_objekt.add_argument(
        '-e', '--ende', dest='start_gegeben', action='store_const',
        const=False, default=True,
        help='Endezeit gegeben / Startzeit nicht gegeben')

    parser_objekt.add_argument(
        '-o', '--outlaw', dest='konformitaetsinfo', action='store_const',
        const=False, default=True,
        help='Info zu nicht-gesetzeskonformen Eingaben ausgeben')

    parser_objekt.add_argument(
        '-r', '--raw', dest='roh', action='store_const',
        const=True, default=False,
        help='Rohausgabe')

    parser_objekt.add_argument(
        '-u', '--uncorrected', dest='unkorrigiert', action='store_const',
        const=True, default=False,
        help='Zeiten unkorrigiert ausgeben')

    parser_objekt.add_argument(
        '-v', '--version', dest='version', action='store_const',
        const=True, default=False,
        help='Versionsinformation anzeigen und beenden')

    return parser_objekt


def option_tagesarbeitsminuten(arg):
    '''
    Auswertung der Option -t. Die Nutzung dieser Option sieht die Übergabe
    eines Wertes vor, der hier ausgewertet wird.
    '''
    if not arg.split("=")[0] == '-t':
        return None
    if len(arg.split("=")) > 1:
        if arg.split("=")[1] == '':
            eprint('Kein Minutenwert spezifiziert.')
            sys.exit(1)
        elif int(arg.split("=")[1]) < 0:
            eprint('%r ist zu klein' % arg.split("=")[1])
            sys.exit(1)
        elif int(arg.split("=")[1]) > 24*60:
            eprint('%r ist zu groß' % arg.split("=")[1])
            sys.exit(1)
        tagesarbeitsminuten = arg.split("=")[1]
        return int(tagesarbeitsminuten)
    return None


def mini_wrapper(string, bezeichnung, wert):
    '''
    Bezeichnung, Zeitwert und Komma an übergebenen String weitergeben
    '''
    if string:
        string += ', '
    string += str(bezeichnung)
    tage, minuten = divmod(wert, 24*60)
    string += liba.minuten_zu_zeitstring(minuten)
    if tage == 1:
        string += ' (n. T.)'
    elif tage > 0:
        string += ' (i. ' + str(tage) + ' T.)'
    return string


def resultat_wrappen(resultat, konform, unkorrigiert):
    '''
    Je nach zurückgegebenen Werten, wird das Ergebnis angezeigt.
    '''

    if len(resultat) != 6:
        raise AssertionError
    if unkorrigiert:
        diff = 0
    else:
        diff = resultat[4]
    string = ''
    if resultat[0]:
        string = mini_wrapper(string, 'Arbeitszeit: ', resultat[0])
    if resultat[1]:
        string = mini_wrapper(string, 'Startzeit: ', resultat[1] - diff)
    if resultat[2]:
        string = mini_wrapper(string, 'Endzeit: ', resultat[2] + diff)
    if (resultat[3] or resultat[3] == 0) and (resultat[1] or resultat[2]):
        string = mini_wrapper(string, 'Pausenzeit: ', resultat[3] + diff)
    else:
        string = mini_wrapper(string, 'Pausenzeit: ', resultat[3])
    print(string)
    if konform and not resultat[5]:
        if not resultat[0] and diff > 0:
            eprint('Arbeits- und/oder Pausenzeiten an gesetzliche Regelung angepasst.')
            eprint('%r Minute(n) Pause hinzugefügt.' % diff)
        elif resultat[0] and diff > 0:
            eprint('Arbeits- und/oder Pausenzeit nicht gesetzesconform')
            eprint('Zusätzliche Pause von %r Minute(n) erforderlich.' % diff)
        else:
            eprint('Arbeits- und/oder Pausenzeit nicht gesetzesconform')


def command_line_interface(zeitwerte=None, t=None, start_gegeben=None, roh=None, version=None, \
                           dateiname=None, konformitaetsinfo=None, unkorrigiert=None):
    if version:
        print(__version__)

    elif dateiname:
        # Dateieingabe verarbeiten. argumente.zeitwerte werden dabei verworfen.
        if zeitwerte:
            eprint('Ignoriere ', *zeitwerte)
        for zeile in dateiname:
            if not zeile.rstrip():
                print()
            elif zeile.lstrip('#') != zeile:
                pass
            else:
                print(*liba.auswerten(zeile.split(),\
                                      t,\
                                      start_gegeben))


    elif zeitwerte:
        if roh:
            print(*liba.auswerten(zeitwerte,\
                                  t,\
                                  start_gegeben))
        else:
            resultat_wrappen(liba.auswerten(zeitwerte,\
                                            t,\
                                            start_gegeben), \
                             konformitaetsinfo, \
                             unkorrigiert)
    return


if __name__ == "__main__":
    NEUE_PARSER_INSTANZ = create_parser()
    GEPARSTE_ARGUMENTE = NEUE_PARSER_INSTANZ.parse_args()

    command_line_interface(GEPARSTE_ARGUMENTE.zeitwerte, GEPARSTE_ARGUMENTE.t, GEPARSTE_ARGUMENTE.start_gegeben, GEPARSTE_ARGUMENTE.roh, GEPARSTE_ARGUMENTE.version, \
                           GEPARSTE_ARGUMENTE.dateiname, GEPARSTE_ARGUMENTE.konformitaetsinfo, GEPARSTE_ARGUMENTE.unkorrigiert)

'''
    if GEPARSTE_ARGUMENTE.version:
        print(__version__)

    elif GEPARSTE_ARGUMENTE.dateiname:
        # Dateieingabe verarbeiten. argumente.zeitwerte werden dabei verworfen.
        if GEPARSTE_ARGUMENTE.zeitwerte:
            eprint('Ignoriere ', *GEPARSTE_ARGUMENTE.zeitwerte)
        for zeile in GEPARSTE_ARGUMENTE.dateiname:
            if not zeile.rstrip():
                print()
            elif zeile.lstrip('#') != zeile:
                pass
            else:
                print(*liba.auswerten(zeile.split(),\
                                      GEPARSTE_ARGUMENTE.t,\
                                      GEPARSTE_ARGUMENTE.start_gegeben))


    elif GEPARSTE_ARGUMENTE.zeitwerte:
        if GEPARSTE_ARGUMENTE.roh:
            print(*liba.auswerten(GEPARSTE_ARGUMENTE.zeitwerte,\
                                  GEPARSTE_ARGUMENTE.t,\
                                  GEPARSTE_ARGUMENTE.start_gegeben))
        else:
            resultat_wrappen(liba.auswerten(GEPARSTE_ARGUMENTE.zeitwerte,\
                                            GEPARSTE_ARGUMENTE.t,\
                                            GEPARSTE_ARGUMENTE.start_gegeben), \
                             GEPARSTE_ARGUMENTE.konformitaetsinfo, \
                             GEPARSTE_ARGUMENTE.unkorrigiert)

    sys.exit(0)
'''
