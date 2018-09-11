# -*- coding: utf-8 -*-

"""
Aus Zeitwerten die Arbeitszeit und Pausen berechnen
"""

#
# Variables with meta information about this module
# This is used in order to have a run-time queryable
# mechanism.
#
__author__ = "Tobias Mettenbrink"
__copyright__ = "Copyright 2018, Tobias Mettenbrink"
__credits__ = ["Tobias Mettenbrink"]
__license__ = "GPL v3.0"
__version__ = "0.1"
__maintainer__ = "Tobias Mettenbrink"
__email__ = ""
__status__ = "Production"

import re
import time

TAGESARBEITSMINUTEN = 8*60


def ist_zeitstring(zeit_string):
    """
    Enthält der übergebene String einen gültigen Zeitwert?
    Diese Funktion detektiert, ob ein string einen Zeitpunkt im
    Format "hh:mm" ist und gibt entsprechend einen boolschen Wert
    aus.
    """
    if not isinstance(zeit_string, str):
        return False

    pattern = re.compile("^[0-9]*:[0-9]*$")
    if not pattern.match(zeit_string):
        return False

    zeit = str(zeit_string).split(':')
    if len(zeit) != 2:
        return False

    if int(zeit[1]) < 60 and int(zeit[0]) <= 24:
        if int(zeit[0]) == 24 and int(zeit[1]) != 0:
            return False
        return True

    return False


def ist_minuten(zeit_wert):
    """
    Kann der übergebene Wert als Zeitwert verwendet werden?
    Diese Funktion detektiert, ob zeit_wert ein String ist, der
    einen numerischen Wert enthält, welcher zum Typ num oder
    float gecastet werden kann. Oder selbst bereits vom Typ int
    oder float ist.
    Die Funktion gibt einen boolschen Werte zurück.
    """
    if isinstance(zeit_wert, str):
        if not zeit_wert.isdigit():
            return False
        else:
            zeit_wert = float(zeit_wert)
    elif not isinstance(zeit_wert, (int, float)):
        return False

    if zeit_wert >= 0:
        return True

    return False


def zeitstring_zu_minuten(zeit_string):
    """
    Konvertiere einen Zeit-String im Format "hh:mm" zu einem Integer, wobei hh für Stunde und mm
    für Minute. hh kann Werte von 00 bis 24 und mm Werte von 00 bis 59 annehmen.
    Also z.B. "11:03" zu 663.
    """
    try:
        assert isinstance(zeit_string, str), "%r is not a tuple" % zeit_string
    except AssertionError:
        raise

    if not ist_zeitstring(zeit_string):
        raise ValueError('%r has no correct Values.' % zeit_string)

    stunden, minuten = zeit_string.split(':')
    try:
        stunden = int(stunden)
        minuten = int(minuten)
    except:
        raise ValueError("%r or %r are not base 10 integers." % (stunden, minuten))

    return stunden*60 + minuten


def minuten_zu_zeitstring(minuten):
    """
    Diese Funktion konvertiert einen ganzzahligen Wert in ein paar von Zahlen,
    das im Format eines Tupels (h,m) ist.
    Bsp.: 30 wird zu (0,30) konvertiert, was 00:30 Uhr entspricht.
    Bem.: minuten soll keine größeren Werte annehmen, als die Anzahl der Minuten
    eines Tages.
    minuten
        minutes, range [0, 1440]
    """
    try:
        assert isinstance(minuten, (int, float)), "%r is not an integer or float" % minuten
    except AssertionError:
        raise

    if not 0 <= minuten <= 24*60:
        raise ValueError("%r is no proper value for minutes." % minuten)

    stunden = int(minuten / 60)
    if stunden < 10:
        stunden = "0" + str(stunden)

    minuten = int(round(minuten)) % 60
    if minuten < 10:
        minuten = "0" + str(minuten)

    return str(stunden) + ':' + str(minuten)


def filter_zpkte_pausen(liste_gemischt):
    """
    Diese Funktion sortiert eine Liste von Zeitobjekten Pausendauer und Zeitpunkt
    zu zwei Listen, in welchen nur Pausendauern oder Zeitpunkte jeweils enthalten
    sind.
    """
    try:
        assert isinstance(liste_gemischt, list),\
            "%r is not a list object" % liste_gemischt
    except AssertionError:
        raise

    zeitpunkt_liste = []
    pausen_liste = []
    for item in liste_gemischt:
        if ist_zeitstring(item):
            zeitpunkt_liste.append(int(zeitstring_zu_minuten(item)))
        elif ist_minuten(item):
            pausen_liste.append(int(item))
        else:
            raise ValueError('Falscher Eingabewert %r' % item)

    return zeitpunkt_liste, pausen_liste


def intervall_summe(zeitpunktliste):
    """
    Summe der Abstände der Zeitpunktpaare. Die Paarbildung findet nach
    Anzahl der Zeitpunkte statt.
    Sind die Zeitpunktpaare aus Anfangs und Endwert vollständig, be-
    schreibt die Summe die Gesamtlänge aller Zeiträume, die die Arbeits-
    zeit ergibt.
    ----------------------------------------------------------------------
    Bsp:     t_0 = 8:00 Uhr
        t_1 = 12:00 Uhr
        t_2 = 12:30 Uhr
        t_3 = 16:30 Uhr
    seien Zeitwerte und die Intervalle (t_0,t_1) und (t_2,t_3) beschreiben
    Arbeitszeiten. Dann beschreibt
        (t_1 - t_0) + (t_3 - t_2)
    die Gesamtlänge der beiden Intervalle, also die Gesamtarbeitszeit.
    ----------------------------------------------------------------------
    Fehlt zu genau einem Zeitpunktpaar ein Wert, ist die Summe ent-
    sprechend positiv oder negativ.
    Die weitere Verarbeitung dieser Summe findet in der Funktion
    auswerten() Anwendung.
    """
    try:
        assert isinstance(zeitpunktliste, list),\
            "%r is not a list object" % zeitpunktliste
    except AssertionError:
        raise

    summe = 0
    for i, item in enumerate(zeitpunktliste):
        try:
            assert isinstance(item, int),\
                "%r is not an integer" % item
        except AssertionError:
            raise
        summe += (-1)**(i+len(zeitpunktliste)+1) * item

    return summe


def auswerten(gemischte_liste, tagesarbeitsminuten=None, start_gegeben=True, sortieren=True):
    """
    Mit Hilfe der Summe, welche von der Funktion intervall_summe() aus-
    gegeben wird, wird hier mit Hilfe der, als bekannt vorausgesetzten
    Ziel-/Gesamtarbeitszeit, ggf. ein fehlender Zeitwert ausgegeben oder
    die Gesamtarbeitszeit aus den vollständigen Zeitwertpaaren und zu-
    sätzlich angegebenen Pausen berechnet.
    Ausgegeben wird also entweder die Gesamtarbeitszeit sowie die Gesamt-
    pausenzeit oder ein fehlender Startwert sowie Gesamtpausenzeit.
    ----------------------------------------------------------------------
    Kernfunktion zur berechnung aller Werte.
    Standard:
          Bsp: t_1 - t_0 + t_3 - t_2 - Pausen
              12:00 - 08:00 + 16:30 - 12:30 - 30min
    start_gegeben=True: Startzeit gegeben, Endezeit soll berechnet werden
          Bsp: t_0 + (t_2 - t_1) + (t_4 - t_3) + Pausen + tagesarbeitsminuten
              08:00 + (12:20 - 12:00) + (09:30 - 09:00)   +   30min   +   tagesarbeitsminuten
    start_gegeben=False: Endezeit gegeben, Startzeit soll berechnet werden
          Bsp: t_4 + (- t_3 + t_2) + ( - t_1 + t_0) - Pausen - tagesarbeitsminuten
              16:30 + (-15:30 + 15:00) + (-10:00 + 09:30)   -  30min   -   tagesarbeitsminuten
    """
    try:
        assert isinstance(gemischte_liste, list),\
            "%r is not a list object" % gemischte_liste
        assert isinstance(tagesarbeitsminuten, int) or not tagesarbeitsminuten,\
            "%r is not an integer" % tagesarbeitsminuten
        assert isinstance(start_gegeben, bool),\
            "%r is not a boolean" % start_gegeben
    except AssertionError:
        raise

    zeitpunkte_liste, pausen_liste = filter_zpkte_pausen(gemischte_liste)

    if not zeitpunkte_liste:
        raise TypeError('No time anchor given. Enter at least a single \
explicit time (no duration).')

    if sortieren:
        zeitpunkte_liste = sorted(zeitpunkte_liste)

    zeit_differenz = intervall_summe(zeitpunkte_liste)

    startzeit = None
    pausenzeit = None
    endzeit = None

    if len(zeitpunkte_liste) % 2 == 1:
        if not tagesarbeitsminuten:
            raise AssertionError('Eingabewert für Tagesarbeitszeit ist %s' % tagesarbeitsminuten)
        if int(tagesarbeitsminuten) < 0:
            raise ValueError('Negativer Eingabewert für Tagesarbeitszeit: %s' % tagesarbeitsminuten)
        # End- bzw. Startzeitpunkt n
        if ist_zeitstring(gemischte_liste[0]) and start_gegeben:
            # Zeitpunkt ist positiv, Pausen und Arbeitszeit werden addiert
            endzeit = zeit_differenz + sum(pausen_liste) + tagesarbeitsminuten
            pausenzeit = endzeit - tagesarbeitsminuten - min(zeitpunkte_liste)  # prognose
        elif not ist_zeitstring(gemischte_liste[0]) or not start_gegeben:
            # Zeitpunkt ist positiv, Arbeitszeit und Pausen werden subtrahiert
            startzeit = zeit_differenz - sum(pausen_liste) - tagesarbeitsminuten
            pausenzeit = max(zeitpunkte_liste) - tagesarbeitsminuten - startzeit  # prognose
    else:
        # Gesamtarbeitszeit berechnen
        tagesarbeitsminuten = zeit_differenz - sum(pausen_liste)
        pausenzeit = max(zeitpunkte_liste) - min(zeitpunkte_liste) - tagesarbeitsminuten
    pausenzeit_diff = pausenzeit_korrektur(tagesarbeitsminuten, pausenzeit)
    konform = pausengesetz_vereinfacht(tagesarbeitsminuten, pausenzeit)
    return tagesarbeitsminuten, startzeit, endzeit, pausenzeit, pausenzeit_diff, konform


def pausengesetz_vereinfacht(tagesarbeitsminuten, tagespausenzeit):
    """
    Diese Funktion wertet die gesetzlichen Bestimmungen zu Pausenzeiten
    des Arbeitszeitgesetzes aus. Es wird überprüft, ob die gearbeitete
    Zeit tagesarbeitsminuten und die Pausen tagespausenzeit den Bestim-
    mungen genügen.
    tagesarbeitsminuten
        minutes, range [0, 1440]
    tagespausenzeit
        minutes, range [0, 1440]
    """
    try:
        assert isinstance(tagesarbeitsminuten, int),\
            "%r is not an integer" % tagesarbeitsminuten
        assert isinstance(tagespausenzeit, int),\
            "%r is not an integer" % tagespausenzeit
    except AssertionError:
        raise

    if tagesarbeitsminuten <= 6*60:
        return True
    elif 6*60 < tagesarbeitsminuten <= 9*60 and tagespausenzeit >= 30:
        return True
    elif 9*60 < tagesarbeitsminuten <= 10*60 and tagespausenzeit >= 45:
        return True

    return False


def pausenzeit_korrektur(tagesarbeitsminuten, tagespausenzeit):
    """
    Hier wird die in der BRD gesetzlich vorgeschriebene Pausenzeit aus-
    gewertet und ggf. ein Differenzwert zur gesetzlichen Regelung aus-
    gegeben.
    tagesarbeitsminuten
        minutes, range [0, 1440]
    tagespausenzeit
        minutes, range [0, 1440]
    """
    try:
        assert isinstance(tagesarbeitsminuten, int),\
            "%r is not an integer" % tagesarbeitsminuten
        assert isinstance(tagespausenzeit, int),\
            "%r is not an integer" % tagespausenzeit
    except AssertionError:
        raise

    diff_pausenzeit = 0
    if tagesarbeitsminuten <= 6*60:
        diff_pausenzeit = 0
    elif 6*60 < tagesarbeitsminuten <= 9*60 and tagespausenzeit < 30:
        diff_pausenzeit = 30 - tagespausenzeit
    elif 9*60 < tagesarbeitsminuten <= 10*60 and tagespausenzeit < 45:
        diff_pausenzeit = 45 - tagespausenzeit

    return diff_pausenzeit


def pausengesetz():
    """
    Diese Funktion wertet aus, ob Pausen zum richtigen Zeitpunkt nach
    Gesetz angegeben wurden.
    """
    pass


def aktuelle_zeit():
    return str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min)
