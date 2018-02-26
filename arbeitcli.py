#!/bin/python3
# -*- coding: utf-8 -*-

'''
Ein Interface zu libarbeitszeiten mit interaktiver Shell.
'''

import sys
import os.path
import argparse
import time
import platform


try:
    import libarbeitszeiten as liba
except ImportError:
    eprint('Could not import module libarbeitszeiten. \
Check, if libarbeitszeiten.py is available in this dir.')

__author__ = 'Tobias Mettenbrink'
__version__ = '0.1'


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
        help='Zeitwerte als Berechnungsgrundlage. \
              Argumente im hh:mm Format werden als Zeitpunkte und ganzzahlige Werte als \
              Pausenzeiten intepretiert. Eingaben über stdin in diesen Formaten werden \
              verarbeitet, wenn keine Werte als Argumente übergeben werden. Bei fehlender \
              Eingabe wird der gegenwärtige Zeitpunkt als Startzeit gewählt.')

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


def resultat_wrappen(resultat, konform, unkorrigiert, einzelwert):
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
        if einzelwert:
            eprint('Pause nach gesetzlicher Regelung hinzugefügt.')
        elif not resultat[0] and diff > 0:
            eprint('Arbeits- und/oder Pausenzeiten an gesetzliche Regelung angepasst.')
            eprint('%r Minute(n) Pause hinzugefügt.' % diff)
        elif resultat[0] and diff > 0:
            eprint('Arbeits- und/oder Pausenzeit nicht gesetzesconform')
            eprint('Zusätzliche Pause von %r Minute(n) erforderlich.' % diff)
        else:
            eprint('Arbeits- und/oder Pausenzeit nicht gesetzesconform')
    return


def os_ist_windows():
    '''
    Gib True, wenn das OS Windows ist und False sonst.
    '''
    return platform.system() == 'Windows'

def os_ist_linux():
    '''
    Gib True, wenn das OS Linux ist und False sonst.
    '''
    return platform.system() == 'Linux'

if __name__ == "__main__":
    NEUE_PARSER_INSTANZ = create_parser()
    GEPARSTE_ARGUMENTE = NEUE_PARSER_INSTANZ.parse_args()
    EINZELNER_WERT = False

    if GEPARSTE_ARGUMENTE.version:
        print(__version__)
    elif not os_ist_windows() and not sys.stdin.isatty():
        for zeile in GEPARSTE_ARGUMENTE.zeitwerte:
            if not zeile.rstrip():
                print()
            elif zeile.lstrip('#') != zeile:
                pass
            else:
                print(*liba.auswerten(zeile.split(),\
                                      GEPARSTE_ARGUMENTE.t,\
                                      GEPARSTE_ARGUMENTE.start_gegeben))
    else:
        try:
            len(GEPARSTE_ARGUMENTE.zeitwerte)#Leerer stdin läuft hier in Fehler
        except TypeError:
            GEPARSTE_ARGUMENTE.zeitwerte = [liba.aktuelle_zeit()]
            print("Gegenwärtige Zeit als Startzeit gewählt: "+str(GEPARSTE_ARGUMENTE.zeitwerte[0]))
        if len(GEPARSTE_ARGUMENTE.zeitwerte) == 1:
            EINZELNER_WERT = True
        if GEPARSTE_ARGUMENTE.roh:
            print(*liba.auswerten(GEPARSTE_ARGUMENTE.zeitwerte,\
                                  GEPARSTE_ARGUMENTE.t,\
                                  GEPARSTE_ARGUMENTE.start_gegeben))
        else:
            resultat_wrappen(liba.auswerten(GEPARSTE_ARGUMENTE.zeitwerte,\
                                            GEPARSTE_ARGUMENTE.t,\
                                            GEPARSTE_ARGUMENTE.start_gegeben), \
                             GEPARSTE_ARGUMENTE.konformitaetsinfo, \
                             GEPARSTE_ARGUMENTE.unkorrigiert, \
                             EINZELNER_WERT)
    sys.exit(0)
