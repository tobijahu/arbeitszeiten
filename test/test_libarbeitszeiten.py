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
        Weitere            *) Ausdrücke ohne ':' (negativ)
                           *) Ausdrücke mit mehr als einem ':' (negativ)
                           *) Ausdrücke mit Zeichen nicht aus '0-9:-' (negativ)
                           *) nicht-String-Ausdrücke (negativ)
        '''
        # Äquivalenzklassen
        self.assertTrue(liba.ist_zeitstring('09:55'))
        self.assertTrue(liba.ist_zeitstring('9:5'))
        self.assertTrue(liba.ist_zeitstring('19:5'))
        self.assertFalse(liba.ist_zeitstring('99:99'))
        self.assertFalse(liba.ist_zeitstring('-09:05'))
        self.assertFalse(liba.ist_zeitstring('-:1'))
        # Grenzwertanalyse
        self.assertFalse(liba.ist_zeitstring('-1:01'))
        self.assertFalse(liba.ist_zeitstring('-0:01'))
        self.assertFalse(liba.ist_zeitstring('-1:0'))
        self.assertTrue(liba.ist_zeitstring('0:0'))
        self.assertTrue(liba.ist_zeitstring('23:59'))
        self.assertTrue(liba.ist_zeitstring('24:00'))
        self.assertFalse(liba.ist_zeitstring('23:60'))
        self.assertFalse(liba.ist_zeitstring('24:01'))
        self.assertFalse(liba.ist_zeitstring('23:61'))
        self.assertFalse(liba.ist_zeitstring('25:00'))
        # Ausdrücke ohne ':'
        self.assertFalse(liba.ist_zeitstring('24'))
        # Ausdrücke mit mehr als einem ':'
        self.assertFalse(liba.ist_zeitstring('12:34:56'))
        # Ausdrücke mit Zeichen nicht aus '0-9:-'
        self.assertFalse(liba.ist_zeitstring('2:22a'))
        # nicht-String-Ausdrücke
        self.assertFalse(liba.ist_zeitstring(90))
        self.assertFalse(liba.ist_zeitstring(60))

    def test_ist_minuten(self):
        '''
        Äquivalenzklassen: 1) t < 0 (negativ)
                           2) t >= 0 (positiv)
                           3) Alles noch einmal als Strings (negativ + positiv)
        Weitere:           *) Interessante Werte (positiv)
                           *) Nicht-erlaubte Zeichen (negativ)
        '''
        # Äquivalenzklassen / Grenzwertanalyse
        self.assertFalse(liba.ist_minuten(-1))
        self.assertTrue(liba.ist_minuten(0))
        self.assertTrue(liba.ist_minuten(1))
        self.assertTrue(liba.ist_minuten(59))
        self.assertTrue(liba.ist_minuten(60))
        self.assertTrue(liba.ist_minuten(61))
        self.assertTrue(liba.ist_minuten(24*60))
        self.assertTrue(liba.ist_minuten(24*60+1))
        self.assertFalse(liba.ist_minuten('-1'))
        self.assertTrue(liba.ist_minuten('0'))
        self.assertTrue(liba.ist_minuten('1'))
        self.assertTrue(liba.ist_minuten('60'))
        self.assertTrue(liba.ist_minuten('61'))
        self.assertTrue(liba.ist_minuten('1440'))
        self.assertTrue(liba.ist_minuten('1441'))
        # Nicht-erlaubte Zeichen
        self.assertFalse(liba.ist_minuten('-0'))
        self.assertFalse(liba.ist_minuten('-1:0'))
        self.assertFalse(liba.ist_minuten('-1j'))

    def test_zeitstring_zu_minuten(self):
        '''
        Äquivalenzklassen: 1) hh:mm < 00:00 (negativ)
                           2) 00:00 <= hh:mm <= 24:00 (positiv)
                           3) hh:mm > 24:00 (negativ)
        Weitere            *) Tripel (negativ)
                           *) Nicht-erlaubte Zeichen (negativ)
        '''
        # Äquivalenzklassen
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_minuten("-12:34")
        self.assertEqual(liba.zeitstring_zu_minuten("07:45"), 7*60+45)
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_minuten("45:31")
        # Grenzwertanalyse
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_minuten("-01:00")
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_minuten("-1:00")
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_minuten("00:-01")
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_minuten("00:-1")
        self.assertEqual(liba.zeitstring_zu_minuten("00:00"), 0)
        self.assertEqual(liba.zeitstring_zu_minuten("00:01"), 1)
        self.assertEqual(liba.zeitstring_zu_minuten("01:00"), 1*60)
        self.assertEqual(liba.zeitstring_zu_minuten("23:59"), 23*60+59)
        self.assertEqual(liba.zeitstring_zu_minuten("24:00"), 24*60)
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_minuten("23:60")
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_minuten("24:01")
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_minuten("25:00")
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_minuten("25:01")
        # Tripel:
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_minuten("01:01:06")
        # Nicht-erlaubte Zeichen:
        with self.assertRaises(ValueError):
            liba.zeitstring_zu_minuten("08:2a")
        with self.assertRaises(AssertionError):
            liba.zeitstring_zu_minuten(8)

    def test_minuten_zu_zeitstring(self):
        # Äquivalenzklassen
        self.assertEqual(liba.minuten_zu_zeitstring(2*60+15), "02:15")
        self.assertEqual(liba.minuten_zu_zeitstring(523.7249), "08:44")
        with self.assertRaises(ValueError):
            liba.minuten_zu_zeitstring(-12*60-15)
        with self.assertRaises(ValueError):
            liba.minuten_zu_zeitstring(25*60)
        # Grenzwertanalyse
        with self.assertRaises(ValueError):
            liba.minuten_zu_zeitstring(-1)
        self.assertEqual(liba.minuten_zu_zeitstring(0), "00:00")
        self.assertEqual(liba.minuten_zu_zeitstring(1), "00:01")
        self.assertEqual(liba.minuten_zu_zeitstring(24*60), "24:00")
        with self.assertRaises(ValueError):
            liba.minuten_zu_zeitstring(24*60+1)
        # Nicht erlaubte Eingaben:
        with self.assertRaises(AssertionError):
            liba.minuten_zu_zeitstring("24*60+1")

    def test_filter_zpkte_pausen(self):
        self.assertEqual(liba.filter_zpkte_pausen( \
                         ["8:15", 55, "12:15", "13:0", 30]), \
                         ([8*60+15, 12*60+15, 13*60], [55, 30]))
        with self.assertRaises(ValueError):
            liba.filter_zpkte_pausen(["8:15", 55, "12:15", "25:0", "13:0", 30])
        with self.assertRaises(ValueError):
            liba.filter_zpkte_pausen(["8:15", 55, "12:15", "22:66", "13:0", 30])

    def test_intervall_summe(self):
        # 12:00 - 08:00 + 16:30 - 12:30 - 30min
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
        # Grenzwertanalyse
        self.assertEqual(liba.intervall_summe([-1]), -1)
        self.assertEqual(liba.intervall_summe([0]), 0)
        self.assertEqual(liba.intervall_summe([24*60]), 24*60)
        self.assertEqual(liba.intervall_summe([24*60+1]), 24*60+1)
        # Weitere tests
        self.assertEqual(liba.intervall_summe([23*60, 5*60]), -23*60+5*60)
        with self.assertRaises(AssertionError):
            liba.intervall_summe("['08:00', 30, '16:30']")

    def test_auswerten(self):
        self.assertEqual(liba.auswerten(["8:0", "12:0", "12:30", "16:30"], 8*60), \
                         (480, None, None, 30, 0, True))
        # 2 Zeitpunkte und Pausendauer:
        self.assertEqual(liba.auswerten(["8:0", 30, "16:30"], 8*60), \
                         (480, None, None, 30, 0, True))
        # 2 Zeitpunkte und 2 Pausendauern:
        self.assertEqual(liba.auswerten([45, "8:0", 30, "16:30"], 8*60), \
                         (435, None, None, 75, 0, True))
        self.assertEqual(liba.auswerten(["8:0", 30, "16:30", 45], 8*60), \
                         (435, None, None, 75, 0, True))
        # 1 Zeitpunkt und 2 Pausendauern:
        self.assertEqual(liba.auswerten([45, 30, "16:30"], 8*60), \
                         (8*60, 7*60+15, None, 75, 0, True))
        self.assertEqual(liba.auswerten([45, 30, "16:30"], 8*60, start_gegeben=False), \
                         (8*60, 7*60+15, None, 75, 0, True))
        self.assertEqual(liba.auswerten(["8:0", 30, 46], 8*60), \
                         (8*60, None, 17*60+16, 30+46, 0, True))
        # 3 Zeitpunkte:
        self.assertEqual(liba.auswerten(["12:0", "12:30", "16:30"], \
                                   8*60, start_gegeben=False), \
                         (8*60, 8*60, None, 30, 0, True))
        self.assertEqual(liba.auswerten(["12:0", "12:30", "16:30"], 8*60), \
                         (8*60, None, 24*60, 4*60, 0, True))
        self.assertEqual(liba.auswerten(["8:0", "12:00", "12:30"], 8*60), \
                         (8*60, None, (8+8)*60+30, 30, 0, True))
        # unsortierte Zeitpunkte
        self.assertEqual(liba.auswerten(["16:30", "12:0"], 8*60), \
                         (16*60+30 - 12*60, None, None, 0, 0, True))
        self.assertEqual(liba.auswerten(["16:30", "12:0", "12:30"], 8*60), \
                         (8*60, None, 24*60, 16*60+30-(12*60+30), 0, True))
        self.assertEqual(liba.auswerten(["13:0", "7:0", "12:30"], 8*60), \
                         (8*60, None, 15*60+30, 30, 0, True))
        self.assertEqual(liba.auswerten(["13:0", "16:30", "12:30"], 8*60, False), \
                         (8*60, 8*60, None, 30, 0, True))
        # nicht-konforme Pausenzeiten
        self.assertEqual(liba.auswerten([5, "16:30"], 8*60), \
                         (8*60, 8*60+25, None, 5, 25, False))
        with self.assertRaises(AssertionError):
            liba.auswerten('["12:0", "12:30", "16:30"]', 50)
        with self.assertRaises(AssertionError):
            liba.auswerten(["12:0", "12:30", "16:30"], '50')
        with self.assertRaises(AssertionError):
            liba.auswerten(["12:0", "12:30", "16:30"], 50, 0)
        with self.assertRaises(ValueError):
            liba.auswerten(["12:0", "12:30", "24:1"], 50)
        with self.assertRaises(ValueError):
            liba.auswerten(["12:0", "12:30", "16:30"], -50)

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
