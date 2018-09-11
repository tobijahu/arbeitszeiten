#!/bin/python3
# -*- coding: utf-8 -*-

import time
import datetime

__author__ = "Tobias Mettenbrink"
__copyright__ = "Copyright 2018, Tobias Mettenbrink"
__credits__ = ["Tobias Mettenbrink"]
__license__ = "GPL v3.0"
__version__ = "0.1"
__maintainer__ = "Tobias Mettenbrink"
__email__ = ""
__status__ = "Production"

while True:
	time_stamp = datetime.datetime.now()
	time.sleep(60)
	time_stamp2 = datetime.datetime.now()
	#if datetime.datetime.now() - time_stamp < datetime.timedelta(minutes=30):
	print(time_stamp2 - time_stamp)
	if time_stamp2 - time_stamp < datetime.timedelta(minutes=1):
		print(time_stamp2 - time_stamp)
