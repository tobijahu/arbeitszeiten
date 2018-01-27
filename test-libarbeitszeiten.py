#!/bin/python3
# -*- coding: utf-8 -*-

import unittest
from libarbeitszeiten import *
#import libarbeitszeiten

class TestStringMethods(unittest.TestCase):
    def test_ist_zeitstring(self):
        self.assertTrue(ist_zeitstring('09:55'))
        self.assertTrue(ist_zeitstring('9:5'))
        self.assertTrue(ist_zeitstring('19:5'))
        self.assertTrue(ist_zeitstring('1:59'))
        self.assertTrue(ist_zeitstring('0:0'))
        self.assertTrue(ist_zeitstring('24:00'))
        self.assertFalse(ist_zeitstring('24:01'))
        self.assertFalse(ist_zeitstring('-02:34'))
        self.assertFalse(ist_zeitstring('34:03'))
        self.assertFalse(ist_zeitstring('24'))
        self.assertFalse(ist_zeitstring('2:22a'))
        self.assertFalse(ist_zeitstring('99:99'))
        self.assertFalse(ist_zeitstring('12:34:56'))
        self.assertFalse(ist_zeitstring(int(90)))
    def test_ist_zeitpunkt(self):
        self.assertTrue(ist_zeitpunkt((9, 55)))
        self.assertTrue(ist_zeitpunkt((9, 5)))
        self.assertTrue(ist_zeitpunkt((19, 5)))
        self.assertTrue(ist_zeitpunkt((1, 59)))
        self.assertTrue(ist_zeitpunkt((0, 0)))
        self.assertTrue(ist_zeitpunkt((24, 0)))
        self.assertFalse(ist_zeitpunkt((-2, 34)))
        self.assertFalse(ist_zeitpunkt((24, 1)))
        self.assertFalse(ist_zeitpunkt((34, 3)))
        self.assertFalse(ist_zeitpunkt((24)))
#        self.assertFalse(ist_zeitpunkt((2, 22a)))
        self.assertFalse(ist_zeitpunkt((99, 99)))
        self.assertFalse(ist_zeitpunkt((12, 34, 56)))
        self.assertFalse(ist_zeitpunkt((int(90))))
    def test_ist_minuten(self):
        self.assertTrue(ist_minuten('90'))
        self.assertTrue(ist_minuten(int(90)))
        self.assertTrue(ist_minuten(90))
        self.assertTrue(ist_minuten(0))
        self.assertFalse(ist_minuten('-1'))
        self.assertFalse(ist_minuten('-1j'))
    def test_zeitstring_zu_zeitpunkt(self):
        self.assertEqual(zeitstring_zu_zeitpunkt("08:21"), (8, 21))
        self.assertEqual(zeitstring_zu_zeitpunkt("24:00"), (24, 0))
        self.assertEqual(zeitstring_zu_zeitpunkt("01:01"), (1, 1))
        self.assertEqual(zeitstring_zu_zeitpunkt("00:00"), (0, 0))
        with self.assertRaises(ValueError):
            zeitstring_zu_zeitpunkt("01:01:06")
        with self.assertRaises(ValueError):
            zeitstring_zu_zeitpunkt("08:2a")
        with self.assertRaises(ValueError):
            zeitstring_zu_zeitpunkt("24:01")
    def test_zeitpunkt_zu_minuten(self):
        self.assertEqual(zeitpunkt_zu_minuten((8, 21)), 8*60+21)
        self.assertEqual(zeitpunkt_zu_minuten((24, 0)), 24*60)
        self.assertEqual(zeitpunkt_zu_minuten((1, 1)), 61)
        with self.assertRaises(AssertionError):
            zeitpunkt_zu_minuten(40)
        with self.assertRaises(AssertionError):
            zeitpunkt_zu_minuten("22:01")
    def test_minuten_zu_zeitpunkt(self):
        self.assertEqual(minuten_zu_zeitpunkt(135), (2, 15))
        minuten_gleitkommazahl = minuten_zu_zeitpunkt(523.7249)
        self.assertEqual((round(minuten_gleitkommazahl[0], 4),\
                          round(minuten_gleitkommazahl[1], 4)\
                         ),\
                         (8, 43.7249)\
                        )
        with self.assertRaises(ValueError):
            minuten_zu_zeitpunkt(25*60)
    def test_zeitpunkt_zu_zeitstring(self):
        self.assertEqual(zeitpunkt_zu_zeitstring((2, 15)), "02:15")
        self.assertEqual(zeitpunkt_zu_zeitstring((0, 0)), "00:00")
        self.assertEqual(zeitpunkt_zu_zeitstring((24, 0)), "24:00")
        with self.assertRaises(AssertionError):
            zeitpunkt_zu_zeitstring((2, '15a'))
        with self.assertRaises(AssertionError):
            zeitpunkt_zu_zeitstring((24, 1))
        with self.assertRaises(AssertionError):
            zeitpunkt_zu_zeitstring((25, 1))
        with self.assertRaises(AssertionError):
            zeitpunkt_zu_zeitstring((22, 61))
    def test_filter_zpkte_pausen(self):
        self.assertEqual(filter_zpkte_pausen( \
                         [(8, 15), 55, (12, 15), (13, 0), 30]), \
                         ([8*60+15, 12*60+15, 13*60], [55, 30]))
        with self.assertRaises(TypeError):
            filter_zpkte_pausen([(8, 15), 55, (12, 15), (25, 0), (13, 0), 30])
        with self.assertRaises(TypeError):
            filter_zpkte_pausen([(8, 15), 55, (12, 15), (22, 66), (13, 0), 30])
    def test_intervall_summe(self):
#        12:00 - 08:00 + 16:30 - 12:30 - 30min
        self.assertEqual(intervall_summe( \
                         [8*60, 12*60, 12*60+30, 16*60+30]), \
                         8*60)
        self.assertEqual(intervall_summe( \
                         [8*60, 9*60+30, 9*60+45, 12*60, 12*60+30, 16*60+30]), \
                         8*60-15)
        # '08:00','09:30','09:45','12:00','12:30',30,'16:30'
        self.assertEqual(intervall_summe( \
                         [8*60, 9*60+30, 9*60+45, 12*60, 12*60+30, 16*60+30]), \
                         8*60-15)
        # '12:00','12:30','16:30'
        self.assertEqual(intervall_summe( \
                         [12*60, 12*60+30, 16*60+30]), \
                         (12*60)-(12*60+30)+(16*60+30))
        with self.assertRaises(AssertionError):
            intervall_summe("['08:00', 30, '16:30']")
    def test_auswerten(self):
        self.assertEqual(auswerten([(8, 0), (12, 0), (12, 30), (16, 30)], 8*60), \
                         (480, None, None, 30, 0, True))
        # 2 Zeitpunkte und Pausendauer:
        self.assertEqual(auswerten([(8, 0), 30, (16, 30)], 8*60), \
                         (480, None, None, 30, 0, True))
        # 2 Zeitpunkte und 2 Pausendauern:
        self.assertEqual(auswerten([45, (8, 0), 30, (16, 30)], 8*60), \
                         (435, None, None, 75, 0, True))
        self.assertEqual(auswerten([(8, 0), 30, (16, 30), 45], 8*60), \
                         (435, None, None, 75, 0, True))
        # 1 Zeitpunkt und 2 Pausendauern:
        self.assertEqual(auswerten([45, 30, (16, 30)], 8*60), \
                         (None, 7*60+15, None, 75, 0, True))
        self.assertEqual(auswerten([45, 30, (16, 30)], 8*60, start_gegeben=False), \
                         (None, 7*60+15, None, 75, 0, True))
        self.assertEqual(auswerten([(8, 0), 30, 46], 8*60), \
                         (None, None, 17*60+16, 30+46, 0, True))
        # 3 Zeitpunkte:
        self.assertEqual(auswerten([(12, 0), (12, 30), (16, 30)], \
                                   8*60, start_gegeben=False), \
                         (None, 8*60, None, 30, 0, True))
        self.assertEqual(auswerten([(12, 0), (12, 30), (16, 30)], 8*60), \
                         (None, None, 24*60, 4*60, 0, True))
        self.assertEqual(auswerten([(8, 0), (12, 00), (12, 30)], 8*60), \
                         (None, None, (8+8)*60+30, 30, 0, True))
        # unsortierte Zeitpunkte
        self.assertEqual(auswerten([(16, 30), (12, 0)], 8*60), \
                         (16*60+30 - 12*60, None, None, 0, 0, True))
        self.assertEqual(auswerten([(16, 30), (12, 0), (12, 30)], 8*60), \
                         (None, None, 24*60, 16*60+30-(12*60+30), 0, True))
        self.assertEqual(auswerten([(13, 0), (7, 0), (12, 30)], 8*60), \
                         (None, None, 15*60+30, 30, 0, True))
        self.assertEqual(auswerten([(13, 0), (16, 30), (12, 30)], 8*60, False), \
                         (None, 8*60, None, 30, 0, True))
        # nicht-konforme Pausenzeiten
        self.assertEqual(auswerten([5, (16, 30)], 8*60), \
                         (None, 8*60+25, None, 5, 25, False))
        with self.assertRaises(AssertionError):
            auswerten("[(12,0), (12,30), (16,30)]", 50)
        with self.assertRaises(AssertionError):
            auswerten([(12, 0), (12, 30), (16, 30)], '50')
        with self.assertRaises(AssertionError):
            auswerten([(12, 0), (12, 30), (16, 30)], 50, 0)
        with self.assertRaises(TypeError):
            auswerten([(12, 0), (12, 30), (24, 1)], 50)
        with self.assertRaises(ValueError):
            auswerten([(12, 0), (12, 30), (16, 30)], -50)
    def test_pausengesetz_vereinfacht(self):
        self.assertTrue(pausengesetz_vereinfacht(6*60, 0))
        self.assertFalse(pausengesetz_vereinfacht(6*60+1, 29))
        self.assertTrue(pausengesetz_vereinfacht(6*60+1, 30))
        self.assertTrue(pausengesetz_vereinfacht(9*60, 30))
        self.assertFalse(pausengesetz_vereinfacht(9*60+1, 44))
        self.assertTrue(pausengesetz_vereinfacht(9*60+1, 45))
        self.assertTrue(pausengesetz_vereinfacht(10*60, 45))
        self.assertFalse(pausengesetz_vereinfacht(10*60+1, 45))
    def test_pausengesetz(self):
        pass


if __name__ == '__main__':
    unittest.main()
