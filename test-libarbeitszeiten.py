#!/bin/python3
# -*- coding: utf-8 -*-

from libarbeitszeiten import *
import unittest

class TestStringMethods(unittest.TestCase):
	def test_zeitpunkt_zu_minuten(self):
		self.assertEqual(zeitpunkt_zu_minuten("08:21"),8*60+21)
		self.assertEqual(zeitpunkt_zu_minuten("24:00"),24*60)
		with self.assertRaises(ValueError):
			zeitpunkt_zu_minuten("08:2a")
		with self.assertRaises(ValueError):
			zeitpunkt_zu_minuten("24:01")
	def test_minuten_zu_zeitpunkt(self):
		self.assertEqual(minuten_zu_zeitpunkt(135),(2,15))
		with self.assertRaises(ValueError):
			minuten_zu_zeitpunkt(25*60)
	def test_zeitpunkt_zu_string(self):
		self.assertEqual(zeitpunkt_zu_string((2,15)),"02:15")
	def test_ist_zeitpunkt(self):
		self.assertTrue(ist_zeitpunkt('09:55'))
		self.assertFalse(ist_zeitpunkt('24:03'))
		self.assertFalse(ist_zeitpunkt('34:03'))
		self.assertFalse(ist_zeitpunkt('24'))
	def test_liste_auswerten(self):
		self.assertEqual(liste_auswerten(['24:00','456']), [True,False])
		self.assertEqual(liste_auswerten(['23:09','456']), [True,False])
		self.assertEqual(sum(liste_auswerten(['23:09','22:22','456'])), 2)
		with self.assertRaises(ValueError):
			liste_auswerten(['-456'])
		with self.assertRaises(ValueError):
			liste_auswerten(['-24:01'])
	def test_auswerten(self):
		self.assertEqual(auswerten(['08:00','12:00','12:30','16:30'],8*60),480)
		# 2 Zeitpunkte und Pausendauer:
		self.assertEqual(auswerten(['08:00','30','16:30'],8*60),480)
		# 2 Zeitpunkte und 2 Pausendauern:
		self.assertEqual(auswerten(['45','08:00','30','16:30'],8*60),435)
		self.assertEqual(auswerten(['08:00','30','16:30','45'],8*60),435)
		# 1 Zeitpunkt und 2 Pausendauern:
		self.assertEqual(auswerten(['45','30','16:30'],8*60),"07:15")
		self.assertEqual(auswerten(['45','30','16:30'],8*60,start_gegeben=False),"07:15")
		self.assertEqual(auswerten(['45','30','16:30'],8*60),"07:15")
		self.assertEqual(auswerten(['08:00','30','46'],8*60),"17:16")
		self.assertEqual(auswerten(['45','30','16:30'],8*60),"07:15")
		# 3 Zeitpunkte:
		self.assertEqual(auswerten(['12:00','12:30','16:30'],8*60,start_gegeben=False),'08:00')
		self.assertEqual(auswerten(['12:00','12:30','16:30'],8*60),'24:00')
		

if __name__ == '__main__':
	unittest.main()
