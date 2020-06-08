#!/usr/bin/python3

from .hx711 import HX711
import time
import sys
import random
import RPi.GPIO as GPIO

hx = HX711(5, 6)

offset = 0
referenceUnit = -374

class Scale():

	def cleanAndExit():
		GPIO.cleanup()
		sys.exit()

	def setup(config):
		hx.set_reading_format("MSB", "MSB")
		hx.set_reference_unit(referenceUnit)
		tare()
		hx.reset()

	def tare():
		hx.tare()

	def get_weight(self):
		# random.seed()
		hx.power_up()
		weight = hx.get_weight(5)
		hx.power_down()
		# debug_weight = random.randrange(10, 750)

		# return int(round(debug_weight))
		return int(round(weight))
