#!/bin/python3
# -*- coding: utf-8 -*-

import unittest
import libarbeitszeiten as libaz
# from ping import create_parser, ping
# from arbeitcli import create_parser, command_line_interface
from arbeitcli import create_parser

import subprocess

__author__ = "Tobias Mettenbrink"
__copyright__ = "Copyright 2018, Tobias Mettenbrink"
__credits__ = ["Tobias Mettenbrink"]
__license__ = "GPL v3.0"
__version__ = "0.1"
__maintainer__ = "Tobias Mettenbrink"
__email__ = ""
__status__ = "Production"


class CommandLineTestCase(TestCase):
    """
    Base TestCase class, sets up a CLI parser
    """

    @classmethod
    def setUpClass(cls):
        parser = create_parser()
        cls.parser = parser


class ArbeitCLITestCase(CommandLineTestCase):
    def test_with_empty_args():
        """
        User passes no args, should fail with SystemExit
        """
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])

    #    def test_arbeitszeit_berechnen():
    #        """
    #
    #        """
    #        command_line_interface(GEPARSTE_ARGUMENTE.zeitwerte, GEPARSTE_ARGUMENTE.t, GEPARSTE_ARGUMENTE.start_gegeben, GEPARSTE_ARGUMENTE.roh, GEPARSTE_ARGUMENTE.version, \
    #                               GEPARSTE_ARGUMENTE.dateiname, GEPARSTE_ARGUMENTE.konformitaetsinfo, GEPARSTE_ARGUMENTE.unkorrigiert)
    #        args = self.parser.parse_args(['-r', '8:0', '30', '1', '20:30'])
    #        result = ping(args.zeitwerte, args.region, args.ami)
    #        self.assertIsNotNone(result)
    #        # Do some othe assertions on the result

    def test_standard_input(self):
        """
        Find database servers with the Ubuntu AMI in Australia region
        """
        args = self.parser.parse_args(['-r', '8:0', '-t', '361', '-e'])
        result = libaz.auswerten(args.zeitwerte, args.t, args.start_gegeben)
        self.assertIsNotNone(result)
        # Do some othe assertions on the result


'''
http://dustinrcollins.com/testing-python-command-line-apps
'''

"""
def run_cli_programm(programm, parameter_input_string):
#    subprocess.run([programm, parameter_input_string], shell=True, check=True)
    return subprocess.check_output([str(programm), str(parameter_input_string)])


'''
arbeit-cli 8:50 12:00 13:00 19:00
Startzeit: 01:50
Pausenzeit: 03:10

arbeit-cli -e 11:30 12:00 18:00
Startzeit: 09:30
Pausenzeit: 00:30

arbeit-cli 8:50 12:00 13:00
'''

class TestStringMethods(unittest.TestCase):
    def test_ist_zeitstring(self):
        self.assertTrue(ist_zeitstring('09:55'))
        self.assertTrue(ist_zeitstring('9:5'))
        self.assertTrue(ist_zeitstring('19:5'))
        self.assertTrue(ist_zeitstring('1:59'))
        self.assertFalse(ist_zeitstring('-02:34'))
        self.assertFalse(ist_zeitstring('24:03'))
        self.assertFalse(ist_zeitstring('34:03'))
        self.assertFalse(ist_zeitstring('24'))
        self.assertFalse(ist_zeitstring('2:22a'))
        self.assertFalse(ist_zeitstring('99:99'))
        self.assertFalse(ist_zeitstring('12:34:56'))
        self.assertFalse(ist_zeitstring(int(90)))
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
        a = minuten_zu_zeitpunkt(523.7249)
        self.assertEqual((round(a[0],4),round(a[1],4)), (8, 43.7249))
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


if __name__ == '__main__':
#    unittest.main()
##    print(run_cli_programm("/home/tobias/github/arbeitszeiten/arbeit-cli", "08:00 12:00 12:30 16:00"))
##    print(run_cli_programm("/home/tobias/github/arbeitszeiten/arbeit-cli", ["08:00", "12:00", "12:30", "16:00"]))
#    print(run_cli_programm("/home/tobias/github/arbeitszeiten/arbeit-cli", "08:00 12:00"))

    test_case = "/home/tobias/github/arbeitszeiten/arbeit-cli" + " " + "08:00 16:00"
    print(subprocess.getoutput(test_case))
    run_cli_programm(test_case, 'nicht das richtige ergebnis')

"""
