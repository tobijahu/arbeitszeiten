#!/bin/python3
# -*- coding: utf-8 -*-

'''
Aus Zeitwerten die Arbeitszeit und Pausen berechnen
'''

import re

TAGESARBEITSMINUTEN = 8*60

def ist_zeitstring(zeit_string):
	'''
	Enthält der übergebene String einen gültigen Zeitwert?
	Diese Funktion detektiert, ob ein string einen Zeitpunkt im
	Format "hh:mm" ist und gibt entsprechend einen boolschen Wert
	aus.
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


def ist_minuten(zeit_wert):
	'''
	Kann der übergebene Wert als Zeitwert verwendet werden?
	Diese Funktion detektiert, ob zeit_wert ein String ist, der 
	einen numerischen Wert enthält, welcher zum Typ num oder 
	float gecastet werden kann. Oder selbst bereits vom Typ int 
	oder float ist. 
	Die Funktion gibt einen boolschen Werte zurück.
	'''
	if isinstance(zeit_wert, str):
		if not zeit_wert.isdigit():
			return False
	elif not (isinstance(zeit_wert, int) or isinstance(zeit_wert, float)):
		return False
	try:
		zeit_wert = float(zeit_wert)
	except:
		return False
	if zeit_wert >= 0:
		return True
	return False


def ist_zeitpunkt(integer_tupel):
	'''
	Ist die Eingabe ein gültiges Tupel aus Stunden und Minuten?
	Diese Funktion erwartet eine Eingabe in Form eines Zahlen-
	tupels mit zwei positiven Werten. D.h. für 08:00 Uhr das 
	Tupel (8,0).
	Die Funktion gibt einen boolschen Wert zurück.
	'''
	try:
		assert isinstance(integer_tupel, tuple),\
			"%r is not a tuple" % integer_tupel
		assert isinstance(integer_tupel[0], int) or isinstance(integer_tupel[0], float),\
			"%r is not an integer" % integer_tupel[0]
		assert isinstance(integer_tupel[1], int) or isinstance(integer_tupel[1], float),\
			"%r is not an integer" % integer_tupel[1]
	except AssertionError:
		return False
	if len(integer_tupel) != 2:
		return False
	try:
		integer_tupel = (int(integer_tupel[0]),int(integer_tupel[1]))
	except:
		return False
	if not 0 <= integer_tupel[0] <= 24:
		return False
	if (not 0 <= integer_tupel[1] <= 59) or (integer_tupel[1] != 0 and integer_tupel[0] == 24):
		return False
	return True


def zeitstring_zu_zeitpunkt(zeit_string):
	'''
	Konvertiere einen Zeit-String im Format "hh:mm" zu einem Integer
	Wertetupel im Format (hh,mm), wobei hh für Stunde und mm für Minute.
	hh kann Werte von 00 bis 24 und mm Werte von 00 bis 59 annehmen
	Also z.B. "11:03" zu 663
	'''
	try:
		assert isinstance(zeit_string, str),\
			"%r is not a tuple" % zeit_string
	except AssertionError:
		raise
	if not ist_zeitstring(zeit_string):
		raise ValueError('%r has no correct Values.' % zeit_string)
	hh,mm = zeit_string.split(':')
	try:
		hh = int(hh)
		mm = int(mm)
	except:
		raise ValueError("%r or %r are not base 10 integers." % (hh,mm))
	return (hh,mm)
	


def zeitpunkt_zu_minuten(tupel):
	'''
	Der übergebene Zeitwert-Tupel (hh,mm) wird hier in einen 
	Minuten-Zeitwert umgerechnet.
	'''
	try:
		assert ist_zeitpunkt(tupel),\
			"%r is not a tupel (hh,mm)" % tupel
	except AssertionError:
		raise
	return tupel[0] * 60 + tupel[1]


def minuten_zu_zeitpunkt(minuten):
	'''
	Diese Funktion konvertiert einen ganzzahligen Wert in ein paar von Zahlen,
	das im Format eines Tupels (h,m) ist. 
	Bsp.: 30 wird zu (0,30) konvertiert, was 00:30 Uhr entspricht.
	Bem.: minuten soll keine größeren Werte annehmen, als die Anzahl der Minuten 
	eines Tages.
	'''
	try:
		assert isinstance(minuten, int) or isinstance(minuten, float),\
			"%r is not an integer or float" % minuten
	except AssertionError:
		raise
	if not 0 <= minuten <= 24*60:
		raise ValueError("%r is no proper value for minutes." % minuten)
	return (int(minuten / 60),minuten % 60)


def zeitpunkt_zu_zeitstring(tupel):
	'''
	Die Funktion erwartet ein Tupel aus zwei ganzen Zahlen >= 0 (d.h. (8,30) für 
	08:30 Uhr) und konvertiert dieses zu einem String im Format "hh:mm" (das ent-
	spräche im vorangegangenen Beispiel also "08:30").
	'''
	try:
		assert ist_zeitpunkt(tupel),\
			"input is not a tupel (hh,mm)"
	except AssertionError:
		raise
	hh = tupel[0]
	if hh < 10:
		hh = "0" + str(hh)
	mm = tupel[1]
	if mm < 10:
		mm = "0" + str(mm)
	return str(hh) + ':' + str(mm)


def filter_zpkte_pausen(liste_gemischt):
	'''
	Diese Funktion sortiert eine Liste von Zeitobjekten Pausendauer und Zeitpunkt
	zu zwei Listen, in welchen nur Pausendauern oder Zeitpunkte jeweils enthalten
	sind. 
	'''
	try:
		assert isinstance(liste_gemischt, list),\
			"%r is not a list object" % liste_gemischt
	except AssertionError:
		raise
	zeitpunkt_liste = []
	pausen_liste = []
	for i in range(len(liste_gemischt)):
		if ist_zeitpunkt(liste_gemischt[i]):
			zeitpunkt_liste.append(int(zeitpunkt_zu_minuten(liste_gemischt[i])))
		elif ist_minuten(liste_gemischt[i]):
			pausen_liste.append(int(liste_gemischt[i]))
		else:
			raise ValueError('Falscher Eingabewert')
	return zeitpunkt_liste,pausen_liste


def intervall_summe(zeitpunktliste):
	'''
	Summe der Abstände der Zeitpunktpaare. Die Paarbildung findet nach 
	Anzahl der Zeitpunkte statt. 
	Sind die Zeitpunktpaare aus Anfangs und Endwert vollständig, be-
	schreibt die Summe die Gesamtlänge aller Zeiträume, die die Arbeits-
	zeit ergibt.
	----------------------------------------------------------------------
	Bsp: 	t_0 = 8:00 Uhr
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
	'''
	try:
		assert isinstance(zeitpunktliste, list),\
			"%r is not a list object" % zeitpunktliste
	except AssertionError:
		raise
	summe = 0
	for i in range(len(zeitpunktliste)):
		try:
			assert isinstance(zeitpunktliste[i], int),\
				"%r is not an integer" % zeitpunktliste[i]
		except AssertionError:
			raise
		summe += (-1)**(i+len(zeitpunktliste)+1) * zeitpunktliste[i]
	return summe


def auswerten(gemischte_liste,tagesarbeitsminuten,start_gegeben=True):
	'''
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
	'''
	
	try:
		assert isinstance(gemischte_liste, list),\
			"%r is not a list object" % gemischte_liste
		assert isinstance(tagesarbeitsminuten, int),\
			"%r is not an integer" % tagesarbeitsminuten
		assert isinstance(start_gegeben, bool),\
			"%r is not a boolean" % start_gegeben
	except AssertionError:
		raise
	if int(tagesarbeitsminuten) < 0:
		raise ValueError('Negativer Eingabewert für Tagesarbeitszeit: %s' % tagesarbeitsminuten)
	zeitpunkte_liste,pausen_liste = filter_zpkte_pausen(gemischte_liste)
	if len(zeitpunkte_liste) == 0:
		raise ValueError('No time anchor given. Enter at least a single explicit time (no duration).')
	zeit_differenz = intervall_summe(zeitpunkte_liste)
	if len(zeitpunkte_liste) % 2 == 1:
		# End- bzw. Startzeitpunkt berechnen
		if ist_zeitpunkt(gemischte_liste[0]) == True and start_gegeben == True:
			# Zeitpunkt ist positiv, Pausen und Arbeitszeit werden addiert
			prognose_endzeit = zeit_differenz + sum(pausen_liste) + tagesarbeitsminuten
			prognose_pausenzeit = prognose_endzeit - tagesarbeitsminuten - min(zeitpunkte_liste)
			return None, prognose_endzeit, prognose_pausenzeit
		elif ist_zeitpunkt(gemischte_liste[0]) == False or start_gegeben == False:
			# Zeitpunkt ist positiv, Arbeitszeit und Pausen werden subtrahiert
			prognose_startzeit = zeit_differenz - sum(pausen_liste) - tagesarbeitsminuten
			prognose_pausenzeit = max(zeitpunkte_liste) - tagesarbeitsminuten - prognose_startzeit
			return None, prognose_startzeit, prognose_pausenzeit
	else:
		# Gesamtarbeitszeit berechnen
		arbeitsminuten = zeit_differenz - sum(pausen_liste)
		pausenzeit = max(zeitpunkte_liste) - min(zeitpunkte_liste) - arbeitsminuten
		return arbeitsminuten, None, pausenzeit


def erfuellt_vorschrift_pausen_vereinfacht(tagesarbeitsminuten,tagespausenzeit):
	'''
	Diese Funktion wertet die gesetzlichen Bestimmungen zu Pausenzeiten 
	des Arbeitszeitgesetzes aus. Es wird überprüft, ob die gearbeitete 
	Zeit tagesarbeitsminuten und die Pausen tagespausenzeit den Bestim-
	mungen genügen.
	'''
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
	else:
		return False


def erfuellt_vorschrift_pausen():
	pass


