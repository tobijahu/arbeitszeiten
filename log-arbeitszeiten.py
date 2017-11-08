#!/bin/python3
# -*- coding: utf-8 -*-

import time
import datetime

while True:
	time_stamp = datetime.datetime.now()
	time.sleep(60)
	time_stamp2 = datetime.datetime.now()
	#if datetime.datetime.now() - time_stamp < datetime.timedelta(minutes=30):
	print(time_stamp2 - time_stamp)
	if time_stamp2 - time_stamp < datetime.timedelta(minutes=1):
		print(time_stamp2 - time_stamp)
