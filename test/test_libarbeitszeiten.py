#!/bin/python3
# -*- coding: utf-8 -*-

'''
Testscript für libarbeitszeiten.py mit unittests für alle Funktionen.
'''

import unittest
import libarbeitszeiten as liba

class TestStringMethods(unittest.TestCase):
    '''
    TestCase-Testklasse aus unittest modul
    '''
    def test_ist_zeitstring(self):
        '''
        Positiv- und Negativtests von liba.ist_zeitstring()
        Äquivalenzklassen: 1) t < 0:0 (negativ)
                           2) 0:0 <= t <= 24:00 (positiv)
                           3) t > 24:00 (negativ)
                           4) Ausdrücke ohne ':' (negativ)
                           5) Ausdrücke mit mehr als einem ':' (negativ)
                           6) Ausdrücke mit Zeichen nicht aus '0-9:-' (negativ)
                           7) nicht-String-Ausdrücke (negativ)
        '''
        self.assertFalse(liba.ist_zeitstring('-1:01'))
        self.assertFalse(liba.ist_zeitstring('-0:01'))
        self.assertFalse(liba.ist_zeitstring('-1:0'))
        self.assertTrue(liba.ist_zeitstring('0:0'))
        self.assertTrue(liba.ist_zeitstring('23:59'))
        self.assertTrue(liba.ist_zeitstring('24:00'))
        self.assertTrue(liba.ist_zeitstring('23:60'))
        self.assertFalse(liba.ist_zeitstring('24:01'))
        self.assertFalse(liba.ist_zeitstring('23:61'))
        self.assertFalse(liba.ist_zeitstring('25:00'))
        self.assertTrue(liba.ist_zeitstring('09:55'))
        self.assertTrue(liba.ist_zeitstring('9:5'))
        self.assertTrue(liba.ist_zeitstring('19:5'))
        self.assertFalse(liba.ist_zeitstring('99:99'))
        self.assertFalse(liba.ist_zeitstring('24'))
        self.assertFalse(liba.ist_zeitstring('12:34:56'))
        self.assertFalse(liba.ist_zeitstring('2:22a'))
        self.assertFalse(liba.ist_zeitstring(90))
        self.assertFalse(liba.ist_zeitstring(60))
        self.assertFalse(liba.ist_zeitstring('-:1'))

    def test_ist_zeitpunkt(self):
        '''
        Positiv- und Negativtests von liba.ist_zeitstring()
        Äquivalenzklassen: 1) (h, m) < (0, 0) (negativ)
                           2) (0, 0) <= (h, m) <= (24, 00) (positiv)
                           3) (h, m) > (24, 00) (negativ)
                           4) Einzelwerte (negativ)
                           5) Tripel (negativ)
        '''
        self.assertFalse(liba.ist_zeitpunkt((-1, 0)))
        self.assertFalse(liba.ist_zeitpunkt((0, -1)))
        self.assertTrue(liba.ist_zeitpunkt((0, 0)))
        self.assertTrue(liba.ist_zeitpunkt((0, 1)))
        self.assertTrue(liba.ist_zeitpunkt((1, 0)))
        self.assertTrue(liba.ist_zeitpunkt((23, 59)))
        self.assertTrue(liba.ist_zeitpunkt((24, 0)))
        self.assertTrue(liba.ist_zeitpunkt((23, 60)))
        self.assertFalse(liba.ist_zeitpunkt((24, 1)))
        self.assertFalse(liba.ist_zeitpunkt((25, 0)))
        self.assertFalse(liba.ist_zeitpunkt((23, 61)))
        self.assertFalse(liba.ist_zeitpunkt((24)))
        self.assertFalse(liba.ist_zeitpunkt((12, 34, 56)))

    def test_ist_minuten(self):
        '''
        Äquivalenzklassen: 1) t < 0 (negativ)
                           2) t >= 0 (positiv)
                           3) Interessante Werte (positiv)
                           4) Alles noch einmal als Strings (negativ + positiv)
                           5) Nicht-erlaubte Zeichen (negativ)
        '''
        self.assertTrue(liba.ist_minuten(-1))
        self.assertTrue(liba.ist_minuten(0))
        self.assertTrue(liba.ist_minuten(1))
        self.assertTrue(liba.ist_minuten(59))
        self.assertTrue(liba.ist_minuten(60))
        self.assertTrue(liba.ist_minuten(61))
        self.assertTrue(liba.ist_minuten(24*60))
        self.assertTrue(liba.ist_minuten(24*60+1))
        self.assertFalse(liba.ist_minuten('-1'))
        self.assertTrue(liba.ist_minuten('0'))
        self.assertTrue(liba.ist_minuten('-0'))
        self.assertTrue(liba.ist_minuten('1'))
        self.assertTrue(liba.ist_minuten('60'))
        self.assertTrue(liba.ist_minuten('61'))
        self.assertTrue(liba.ist_minuten('1440'))
        self.assertTrue(liba.ist_minuten('1441'))
        self.assertFalse(liba.ist_minuten('-1j'))
        self.assertFalse(liba.ist_minuten('-1:0'))
    def test_zeitstring_zu_zeitpunkt(self):
        '''
        Äquivalenzklassen: 1) hh:mm < 00:00 (negativ)
                           2) 00:00 <= hh:mm <= 24:00 (positiv)
                           3) hh:mm > 24:00 (negativ)
                           4) Tripel (negativ)
                           5) Nicht-erlaubte Zeichen (negativ)
        '''
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_zeitpunkt("-01:00")
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_zeitpunkt("-1:00")
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_zeitpunkt("00:-01")
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_zeitpunkt("00:-1")
        self.assertEqual(liba.zeitstring_zu_zeitpunkt("00:00"), (0, 0))
        self.assertEqual(liba.zeitstring_zu_zeitpunkt("00:01"), (0, 1))
        self.assertEqual(liba.zeitstring_zu_zeitpunkt("01:00"), (1, 0))
        self.assertEqual(liba.zeitstring_zu_zeitpunkt("23:59"), (23, 59))
        self.assertEqual(liba.zeitstring_zu_zeitpunkt("24:00"), (24, 0))
        self.assertEqual(liba.zeitstring_zu_zeitpunkt("23:60"), (23, 60))
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_zeitpunkt("24:01")
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_zeitpunkt("25:00")
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_zeitpunkt("25:01")
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_zeitpunkt("01:01:06")
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_zeitpunkt("08:2a")

    def test_zeitpunkt_zu_minuten(self):
        '''
        Äquivalenzklassen: 1) 
        '''
        self.assertEqual(liba.zeitpunkt_zu_minuten((8, 21)), 8*60+21)
        self.assertEqual(liba.zeitpunkt_zu_minuten((24, 0)), 24*60)
        self.assertEqual(liba.zeitpunkt_zu_minuten((1, 1)), 61)
        with self.assertRaises(AssertionError):
            liba.zeitpunkt_zu_minuten(40)
        with self.assertRaises(AssertionError):
            liba.zeitpunkt_zu_minuten("22:01")

    def test_minuten_zu_zeitpunkt(self):
        self.assertEqual(liba.minuten_zu_zeitpunkt(135), (2, 15))
        minuten_gleitkommazahl = liba.minuten_zu_zeitpunkt(523.7249)
        self.assertEqual((round(minuten_gleitkommazahl[0], 4),\
                          round(minuten_gleitkommazahl[1], 4)\
                         ),\
                         (8, 43.7249)\
                        )
        with self.assertRaises(ValueError):
            liba.minuten_zu_zeitpunkt(25*60)

    def test_zeitpunkt_zu_zeitstring(self):
        self.assertEqual(liba.zeitpunkt_zu_zeitstring((2, 15)), "02:15")
        self.assertEqual(liba.zeitpunkt_zu_zeitstring((0, 0)), "00:00")
        self.assertEqual(liba.zeitpunkt_zu_zeitstring((24, 0)), "24:00")
        with self.assertRaises(AssertionError):
            liba.zeitpunkt_zu_zeitstring((2, '15a'))
        with self.assertRaises(AssertionError):
            liba.zeitpunkt_zu_zeitstring((24, 1))
        with self.assertRaises(AssertionError):
            liba.zeitpunkt_zu_zeitstring((25, 1))
        with self.assertRaises(AssertionError):
            liba.zeitpunkt_zu_zeitstring((22, 61))

    def test_filter_zpkte_pausen(self):
        self.assertEqual(liba.filter_zpkte_pausen( \
                         [(8, 15), 55, (12, 15), (13, 0), 30]), \
                         ([8*60+15, 12*60+15, 13*60], [55, 30]))
        with self.assertRaises(TypeError):
            liba.filter_zpkte_pausen([(8, 15), 55, (12, 15), (25, 0), (13, 0), 30])
        with self.assertRaises(TypeError):
            liba.filter_zpkte_pausen([(8, 15), 55, (12, 15), (22, 66), (13, 0), 30])

    def test_intervall_summe(self):
#        12:00 - 08:00 + 16:30 - 12:30 - 30min
        self.assertEqual(liba.intervall_summe( \
                         [8*60, 12*60, 12*60+30, 16*60+30]), \
                         8*60)
        self.assertEqual(liba.intervall_summe( \
                         [8*60, 9*60+30, 9*60+45, 12*60, 12*60+30, 16*60+30]), \
                         8*60-15)
        # '08:00','09:30','09:45','12:00','12:30',30,'16:30'
        self.assertEqual(liba.intervall_summe( \
                         [8*60, 9*60+30, 9*60+45, 12*60, 12*60+30, 16*60+30]), \
                         8*60-15)
        # '12:00','12:30','16:30'
        self.assertEqual(liba.intervall_summe( \
                         [12*60, 12*60+30, 16*60+30]), \
                         (12*60)-(12*60+30)+(16*60+30))
        with self.assertRaises(AssertionError):
            liba.intervall_summe("['08:00', 30, '16:30']")

    def test_auswerten(self):
        self.assertEqual(liba.auswerten([(8, 0), (12, 0), (12, 30), (16, 30)], 8*60), \
                         (480, None, None, 30, 0, True))
        # 2 Zeitpunkte und Pausendauer:
        self.assertEqual(liba.auswerten([(8, 0), 30, (16, 30)], 8*60), \
                         (480, None, None, 30, 0, True))
        # 2 Zeitpunkte und 2 Pausendauern:
        self.assertEqual(liba.auswerten([45, (8, 0), 30, (16, 30)], 8*60), \
                         (435, None, None, 75, 0, True))
        self.assertEqual(liba.auswerten([(8, 0), 30, (16, 30), 45], 8*60), \
                         (435, None, None, 75, 0, True))
        # 1 Zeitpunkt und 2 Pausendauern:
        self.assertEqual(liba.auswerten([45, 30, (16, 30)], 8*60), \
                         (None, 7*60+15, None, 75, 0, True))
        self.assertEqual(liba.auswerten([45, 30, (16, 30)], 8*60, start_gegeben=False), \
                         (None, 7*60+15, None, 75, 0, True))
        self.assertEqual(liba.auswerten([(8, 0), 30, 46], 8*60), \
                         (None, None, 17*60+16, 30+46, 0, True))
        # 3 Zeitpunkte:
        self.assertEqual(liba.auswerten([(12, 0), (12, 30), (16, 30)], \
                                   8*60, start_gegeben=False), \
                         (None, 8*60, None, 30, 0, True))
        self.assertEqual(liba.auswerten([(12, 0), (12, 30), (16, 30)], 8*60), \
                         (None, None, 24*60, 4*60, 0, True))
        self.assertEqual(liba.auswerten([(8, 0), (12, 00), (12, 30)], 8*60), \
                         (None, None, (8+8)*60+30, 30, 0, True))
        # unsortierte Zeitpunkte
        self.assertEqual(liba.auswerten([(16, 30), (12, 0)], 8*60), \
                         (16*60+30 - 12*60, None, None, 0, 0, True))
        self.assertEqual(liba.auswerten([(16, 30), (12, 0), (12, 30)], 8*60), \
                         (None, None, 24*60, 16*60+30-(12*60+30), 0, True))
        self.assertEqual(liba.auswerten([(13, 0), (7, 0), (12, 30)], 8*60), \
                         (None, None, 15*60+30, 30, 0, True))
        self.assertEqual(liba.auswerten([(13, 0), (16, 30), (12, 30)], 8*60, False), \
                         (None, 8*60, None, 30, 0, True))
        # nicht-konforme Pausenzeiten
        self.assertEqual(liba.auswerten([5, (16, 30)], 8*60), \
                         (None, 8*60+25, None, 5, 25, False))
        with self.assertRaises(AssertionError):
            liba.auswerten("[(12,0), (12,30), (16,30)]", 50)
        with self.assertRaises(AssertionError):
            liba.auswerten([(12, 0), (12, 30), (16, 30)], '50')
        with self.assertRaises(AssertionError):
            liba.auswerten([(12, 0), (12, 30), (16, 30)], 50, 0)
        with self.assertRaises(TypeError):
            liba.auswerten([(12, 0), (12, 30), (24, 1)], 50)
        with self.assertRaises(ValueError):
            liba.auswerten([(12, 0), (12, 30), (16, 30)], -50)

    def test_pausengesetz_vereinfacht(self):
        self.assertTrue(liba.pausengesetz_vereinfacht(6*60, 0))
        self.assertFalse(liba.pausengesetz_vereinfacht(6*60+1, 29))
        self.assertTrue(liba.pausengesetz_vereinfacht(6*60+1, 30))
        self.assertTrue(liba.pausengesetz_vereinfacht(9*60, 30))
        self.assertFalse(liba.pausengesetz_vereinfacht(9*60+1, 44))
        self.assertTrue(liba.pausengesetz_vereinfacht(9*60+1, 45))
        self.assertTrue(liba.pausengesetz_vereinfacht(10*60, 45))
        self.assertFalse(liba.pausengesetz_vereinfacht(10*60+1, 45))

    def test_pausengesetz(self):
        pass


if __name__ == '__main__':
    unittest.main()
