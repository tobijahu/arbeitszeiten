#!/bin/python3
# -*- coding: utf-8 -*-

from libarbeitszeiten import *
import unittest

class TestStringMethods(unittest.TestCase):
	def test_ist_zeitpunkt(self):
		self.assertTrue(ist_zeitpunkt('09:55'))
		self.assertTrue(ist_zeitpunkt('9:5'))
		self.assertTrue(ist_zeitpunkt('19:5'))
		self.assertTrue(ist_zeitpunkt('1:59'))
		self.assertFalse(ist_zeitpunkt('-02:34'))
		self.assertFalse(ist_zeitpunkt('24:03'))
		self.assertFalse(ist_zeitpunkt('34:03'))
		self.assertFalse(ist_zeitpunkt('24'))
		self.assertFalse(ist_zeitpunkt('2:22a'))
		self.assertFalse(ist_zeitpunkt('99:99'))
		self.assertFalse(ist_zeitpunkt('12:34:56'))
		self.assertFalse(ist_zeitpunkt(int(90)))
	def test_ist_minuten(self):
		self.assertTrue(ist_minuten('90'))
		self.assertTrue(ist_minuten(int(90)))
		self.assertTrue(ist_minuten(90))
		self.assertTrue(ist_minuten(0))
		self.assertFalse(ist_minuten('-1'))
		self.assertFalse(ist_minuten('-1j'))
	def test_zeitpunkt_zu_minuten(self):
		self.assertEqual(zeitpunkt_zu_minuten("08:21"),8*60+21)
		self.assertEqual(zeitpunkt_zu_minuten("24:00"),24*60)
		self.assertEqual(zeitpunkt_zu_minuten("01:01"),61)
		with self.assertRaises(ValueError):
			zeitpunkt_zu_minuten("01:01:06")
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
		self.assertEqual(zeitpunkt_zu_string((0,0)),"00:00")
		self.assertEqual(zeitpunkt_zu_string((24,0)),"24:00")
		with self.assertRaises(AssertionError):
			zeitpunkt_zu_string((2,'15a'))
		with self.assertRaises(ValueError):
			zeitpunkt_zu_string((24,1))
		with self.assertRaises(ValueError):
			zeitpunkt_zu_string((25,1))
		with self.assertRaises(ValueError):
			zeitpunkt_zu_string((22,61))
	def test_intervall_summen(self):
#		12:00 - 08:00 + 16:30 - 12:30 - 30min
		self.assertEqual(intervall_summen([8*60,12*60,12*60+30,16*60+30]),8*60)
		self.assertEqual(intervall_summen([8*60,9*60+30,9*60+45,12*60,12*60+30,16*60+30]),8*60-15)
		# '08:00','09:30','09:45','12:00','12:30',30,'16:30'
		self.assertEqual(intervall_summen([8*60,9*60+30,9*60+45,12*60,12*60+30,16*60+30]),8*60-15)
		# '12:00','12:30','16:30'
		self.assertEqual(intervall_summen([12*60,12*60+30,16*60+30]),(12*60)-(12*60+30)+(16*60+30))
		with self.assertRaises(AssertionError):
			intervall_summen("['08:00',30,'16:30']")
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
		with self.assertRaises(AssertionError):
			auswerten("['12:00','12:30','16:30']",50)
		with self.assertRaises(AssertionError):
			auswerten(['12:00','12:30','16:30'],'50')
		with self.assertRaises(AssertionError):
			auswerten(['12:00','12:30','16:30'],50,0)
		with self.assertRaises(ValueError):
			auswerten(['12:00','12:30','24:01'],50)
		with self.assertRaises(ValueError):
			auswerten(['12:00','12:30','24:00'],-50)
		

if __name__ == '__main__':
	unittest.main()
