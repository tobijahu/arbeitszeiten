#!/bin/python3
# -*- coding: utf-8 -*-

'''
Aus Zeitwerten die Arbeitszeit berechnen
'''

import re

TAGESARBEITSMINUTEN = 8*60

def ist_zeitpunkt(zeit_string):
	'''
	Diese Funktion detektiert, ob ein string einen Zeitpunkt im
	Format "hh:mm" ist und gibt boolsche Werte aus.
	'''
	
	if not isinstance(zeit_string, str):
		return False
	
	pattern = re.compile("^[0-9]*\:[0-9]*$")
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


def ist_minuten(zeit_string):
	'''
	Diese Funktion detektiert, ob ein input_variable ein String im 
	Format "hh:mm" ist und gibt dann einen  boolschen Werte aus.
	'''
	
	if isinstance(zeit_string, str):
		if not zeit_string.isdigit():
			return False
	elif not isinstance(zeit_string, int):
		return False
	
	try:
		zeit_string = float(zeit_string)
	except:
		return False
	
	if zeit_string >= 0:
		return True
	else:
		return False


def bla():
	pass


def zeitpunkt_zu_minuten(stunden_minuten):
	'''
	Konvertiere einen Zeit-String im Format "hh:mm" zu einem Integer Wert.
	hh kann Werte von 00 bis 24 und mm Werte von 00 bis 59 annehmen
	Also z.B. "11:03" zu 663
	'''
	try:
		assert isinstance(stunden_minuten, str),\
			"%r is not a string" % stunden_minuten
	except AssertionError:
		raise
	
	if ist_zeitpunkt(stunden_minuten):
		hh,mm = stunden_minuten.split(':')
	else:
		raise ValueError("%r is not a proper value." % stunden_minuten)
	
	try:
		hh = int(hh)
		mm = int(mm)
	except:
		raise ValueError("%r or %r are not base 10 integers." % (hh,mm))
	
	return hh * 60 + mm


def minuten_zu_zeitpunkt(minuten):
	'''
	Diese Funktion konvertiert einen ganzzahligen Wert in ein paar von Zahlen,
	das im "hh:mm" format ist.
	minuten soll keine größeren Werte annehmen, als die Anzahl der Minuten eines
	Tages.
	'''
	try:
		assert isinstance(minuten, int),\
			"%r is not an integer" % minuten
	except AssertionError:
		raise
	
	if minuten < 0 or minuten > 24*60:
		raise ValueError("%r is no proper value for minutes." % minuten)
	
	return (int(minuten / 60),minuten % 60)


def zeitpunkt_zu_string(paar):
	'''
	paar erwartet ein Tupel aus zwei ganzen Zahlen >= 0 und konvertiert dieses 
	zu einem String im Format "hh:mm".
	'''
	try:
		assert isinstance(paar, tuple),\
			"%r is not a tuple" % paar
		assert isinstance(paar[0], int),\
			"%r is not an integer" % paar[0]
		assert isinstance(paar[1], int),\
			"%r is not an integer" % paar[1]
	except AssertionError:
		raise
	
	try:
		paar = (int(paar[0]),int(paar[1]))
	except:
		raise ValueError('%r nicht zulässig', paar)
	
	if paar[0] > 24 or paar[0] < 0:
		raise ValueError('Wert fuer Stunden nicht zulaessig')
	if paar[1] > 59 or paar[0] < 0 or (paar[1] != 0 and paar[0] == 24):
		raise ValueError('Wert fuer Minuten nicht zulaessig')
	hh = paar[0]
	if hh < 10:
		hh = "0" + str(hh)
	mm = paar[1]
	if mm < 10:
		mm = "0" + str(mm)
	return str(hh) + ':' + str(mm)


def liste_auswerten(liste):
	'''
	Generiere eine Liste, in der die Auswertungen zu den Listenelementen
	der übergebenen list enthalten sind. Unterschieden werden Elemente im
	Zeitpunkt- und Ganzzahligen format.
	'''
	
	try:
		assert isinstance(liste, list),\
			"%r is not a list object" % liste
	except AssertionError:
		raise
	
	bool_liste = []
	
	for wert in liste:
		# Todo? Assert jedes Elementes
		if ist_zeitpunkt(wert):
			bool_liste.append(True)
			continue
		else:
			try:
				float(wert)
			except:
				raise ValueError('Falscher Eingabewert: %s' % wert)
			if float(wert) < 0:
				raise ValueError('Falscher Eingabewert: %s' % wert)
			bool_liste.append(False)
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
	try:
		assert isinstance(liste, list),\
			"%r is not a list object" % liste
		assert isinstance(zeitpunkte, int),\
			"%r is not an integer" % zeitpunkte
		assert isinstance(start_gegeben, bool),\
			"%r is not a boolean" % start_gegeben
	except AssertionError:
		raise
	
	summe = 0
	alt = zeitpunkte
	vorzeichen_von_pausen = 1
	
	if zeitpunkte % 2 == 0 or not start_gegeben:
		vorzeichen_von_pausen = -1
	for i in range(len(liste)):
		if ist_minuten(liste[i]):
			try:
				int(liste[i])
			except:
				raise ValueError('Falscher Eingabewert: %s' % i)
			# Alle ganzzahligen Werte sind Pausenzeiten und werden von der Summe abgezogen
			summe = summe + vorzeichen_von_pausen * int(liste[i])
		elif ist_zeitpunkt(liste[i]):
			'''
			Um die Differenz aus den benachbarten 
			Zeitwerten zu erhalten, alterniert das
			Vorzeichen der Zeitpunktwerte.
			'''
			try:
				assert isinstance(liste[i], str),\
					"%r is not a string" % liste[i]
			except AssertionError:
				raise
			alt = alt + 1
			summe = summe + (-1)**alt * int(zeitpunkt_zu_minuten(liste[i]))
	return summe


def auswerten(liste,tagesarbeitsminuten,start_gegeben=True):
	'''
	Weitere Auswertung der Elemente analog zu intervall_summen(). Weitere 
	Merkmale wie tagesarbeitsstunden und start_gegeben erfolgen hier. 
	'''
	
	try:
		assert isinstance(liste, list),\
			"%r is not a list object" % liste
		assert isinstance(tagesarbeitsminuten, int),\
			"%r is not an integer" % tagesarbeitsminuten
		assert isinstance(start_gegeben, bool),\
			"%r is not a boolean" % start_gegeben
	except AssertionError:
		raise
	
	if int(tagesarbeitsminuten) < 0:
		raise ValueError('Negativer Eingabewert für Tagesarbeitszeit: %s' % tagesarbeitsminuten)
	
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
