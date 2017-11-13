#!/bin/python3
# -*- coding: utf-8 -*-

from libarbeitszeiten import *
import sys

		

if __name__ == '__main__':
	werte = sys.argv
#	werte.remove(0)
	
	print(auswerten(werte[1:len(werte)],8*60))
