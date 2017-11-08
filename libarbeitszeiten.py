#!/bin/python3
# -*- coding: utf-8 -*-

'''
Aus Zeitwerten die Arbeitszeit berechnen
'''

import sys
import re

TAGESARBEITSMINUTEN = 8*60

def zeitpunkt_zu_minuten(stunden_minuten):
	'''
	Konvertiere einen Zeit-String im Format "hh:mm" zu einem Integer Wert.
	hh kann Werte von 00 bis 24 und mm Werte von 00 bis 59 annehmen
	Also z.B. "11:03" zu 663
	'''
	assert isinstance(stunden_minuten, str),\
		"%r is not a string" % stunden_minuten
	hh,mm = stunden_minuten.split(':')
	try:
		hh = int(hh)
		mm = int(mm)
	except:
		raise ValueError("%r or %r are not base 10 integers." % (hh,mm))
	if hh < 0 or hh > 24:
		raise ValueError("%r is no proper value for hours." % hh)
	if mm < 0 or mm > 59:
		raise ValueError("%r is no proper value for minutes." % mm)
	if hh == 24 and mm > 0:
		raise ValueError("%r:%r is no proper time." % (hh,mm))
	return hh * 60 + mm


def minuten_zu_zeitpunkt(minuten):
	'''
	Diese Funktion konvertiert einen ganzzahligen Wert in ein paar von Zahlen,
	das im "hh:mm" format ist.
	minuten soll keine größeren Werte annehmen, als die Anzahl der Minuten eines
	Tages.
	'''
	assert isinstance(minuten, int),\
		"%r is not an integer" % minuten
	if minuten < 0 or minuten > 24*60:
		raise ValueError("%r is no proper value for minutes." % minuten)
	return (int(minuten / 60),minuten % 60)


def zeitpunkt_zu_string(paar):
	'''
	paar erwartet ein Tupel aus zwei ganzen Zahlen >= 0 und konvertiert dieses 
	zu einem String im Format "hh:mm".
	'''
	assert isinstance(paar[0], int),\
		"%r is not an integer" % paar[0]
	assert isinstance(paar[1], int),\
		"%r is not an integer" % paar[1]
	if paar[0] > 24 or paar[0] < 0:
		raise ValueError('Wert fuer Stunden nicht zulaessig')
	if paar[1] > 60 or paar[0] < 0:
		raise ValueError('Wert fuer Minuten nicht zulaessig')
	mm = paar[1]
	if mm < 10:
		mm = "0" + str(mm)
	hh = paar[0]
	if hh < 10:
		hh = "0" + str(hh)
	return str(hh) + ':' + str(mm)


def ist_zeitpunkt(input_variable):
	'''
	Diese Funktion detektiert, ob ein string einen Zeitpunkt im
	Format "hh:mm" ist und gibt boolsche Werte aus.
	'''
	assert isinstance(input_variable, str),\
		"%r is not a string" % input_variable
	
	pattern = re.compile("^[0-2][0-9]\:[0-9][0-9]$")
	if not pattern.match(input_variable):
		return False
	
	array = str(input_variable).split(':')
	hh = array[0]
	if not hh.isdigit():
		return False
	
	if len(array) == 2:
		mm = array[1]
		if not mm.isdigit():
			return False
	else:
		return False
	
	if mm == '' or mm is None:
		return False
	elif int(mm) <= 60 and int(mm) >= 0 and int(hh) >= 0 and int(hh) <= 24:
		if int(hh) == 24 and int(mm) != 0:
			return False
		return True


def ist_minuten(input_variable):
	'''
	Diese Funktion detektiert, ob ein input_variable ein String im 
	Format "hh:mm" ist und gibt dann einen  boolschen Werte aus.
	'''
	assert isinstance(input_variable, str),\
		"%r is not a string" % input_variable
	if input_variable.isdigit():
		if int(input_variable) >= 0:
			return True
	return False


def liste_auswerten(liste):
	'''
	Generiere eine Liste, in der die Auswertungen zu den Listenelementen
	der übergebenen list enthalten sind. Unterschieden werden Elemente im
	Zeitpunkt- und Ganzzahligen format.
	'''
	assert isinstance(liste, list),\
		"%r is not a list object" % liste
	bool_liste = []
	for wert in liste:
		if ist_zeitpunkt(wert):
			bool_liste.append(True)
		elif ist_minuten(wert):
			bool_liste.append(False)
		else:
			raise ValueError('Falscher Eingabewert: %s' % (wert))
	return bool_liste


def intervall_summen(liste,zeitpunkte,start_gegeben=True):
	'''
	Kernfunktion zur berechnung aller Werte.
	Standard:
	       Bsp: i_1 - i_0 + i_3 - i_2 - Pausen
	            12:00 - 08:00 + 16:30 - 12:30 - 30min
	start_gegeben=True: Startzeit gegeben, Endezeit soll berechnet werden
	       Bsp: i_0 + (i_2 - i_1) + (i_4 - i_3) + Pausen + tagesarbeitsminuten
	            08:00 + (12:20 - 12:00) + (09:30 - 09:00)   +   30min   +   tagesarbeitsminuten
	start_gegeben=False: Endezeit gegeben, Startzeit soll berechnet werden
	       Bsp: i_4 + (- i_3 + i_2) + ( - i_1 + i_0) - Pausen - tagesarbeitsminuten
	            16:30 + (-15:30 + 15:00) + (-10:00 + 09:30)   -  30min   -   tagesarbeitsminuten
	'''
	assert isinstance(liste, list),\
		"%r is not a list object" % liste
	assert isinstance(zeitpunkte, int),\
		"%r is not an integer" % zeitpunkte
	assert isinstance(start_gegeben, bool),\
		"%r is not a boolean" % start_gegeben
	summe = 0
	alt = zeitpunkte
	vorzeichen_von_pausen = 1
	if zeitpunkte % 2 == 0 or not start_gegeben:
		vorzeichen_von_pausen = -1
	for i in range(len(liste)):
		if ist_minuten(liste[i]):
			# Alle ganzzahligen Werte sind Pausenzeiten und werden von der Summe abgezogen
			summe = summe + vorzeichen_von_pausen * int(liste[i])
		elif ist_zeitpunkt(liste[i]):
			'''
			Um die Differenz aus den benachbarten 
			Zeitwerten zu erhalten, alterniert das
			Vorzeichen der Zeitpunktwerte.
			'''
			alt = alt + 1
			summe = summe + (-1)**alt * int(zeitpunkt_zu_minuten(liste[i]))
	return summe


def auswerten(liste,tagesarbeitsminuten,start_gegeben=True):
	'''
	Weitere Auswertung der Elemente analog zu intervall_summen(). Weitere 
	Merkmale wie tagesarbeitsstunden und start_gegeben erfolgen hier. 
	'''
	assert isinstance(liste, list),\
		"%r is not a list object" % liste
	assert isinstance(tagesarbeitsminuten, int),\
		"%r is not an integer" % tagesarbeitsminuten
	assert isinstance(start_gegeben, bool),\
		"%r is not a boolean" % start_gegeben
	liste_bool = liste_auswerten(liste)
	anzahl_zeitpunkte = sum(liste_bool)
	if anzahl_zeitpunkte == 0:
		raise ValueError('No time anchor given. Enter at least a single explicit time (no duration).')
	elif anzahl_zeitpunkte % 2 == 1:
		# End- bzw. Startzeitpunkt berechnen
		if liste_bool[0] == True and start_gegeben == True:
			# Zeitpunkt ist positiv, Pausen und Arbeitszeit werden addiert
			return zeitpunkt_zu_string(minuten_zu_zeitpunkt(intervall_summen(liste,anzahl_zeitpunkte) + tagesarbeitsminuten))
		elif liste_bool[0] == False or start_gegeben == False:
			# Zeitpunkt ist positiv, Arbeitszeit und Pausen werden subtrahiert
			return zeitpunkt_zu_string(minuten_zu_zeitpunkt(intervall_summen(liste,anzahl_zeitpunkte,start_gegeben=False) - tagesarbeitsminuten))
	else:
		# Gesamtarbeitszeit berechnen
		return intervall_summen(liste,anzahl_zeitpunkte)


def pausen_summen(liste,zeitpunkte,start_gegeben=True):
	
	pass
