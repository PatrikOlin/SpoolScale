#!/usr/bin/python3

from hx711 import HX711
import RPi.GPIO as GPIO
import time
import sys
import argparse
import yaml

hx = HX711(5, 6)
parser = argparse.ArgumentParser()

parser.add_argument("--calibrate", "-c", help="calibrate the scale by putting an item of known weight on the scale and enter the weight in grams", action="store_true")
parser.add_argument("--debug", "-d", help="verbose debugging mode", action="store_true")

args = parser.parse_args()
fname = './conf.yml'

offset = 0
referenceUnit = -374
old_weight = 0

def cleanAndExit():
	if args.debug:
		print("Cleaning up...")
	GPIO.cleanup()
	sys.exit()

def setup(config):
	hx.set_reading_format("MSB", "MSB")
	ref = config["calibratedRefUnit"]
	if ref is None:		     
		ref = config["defaultRefUnit"]
	hx.set_reference_unit(ref)
	tare()
	hx.reset()

def tare():
	hx.tare()

def loadConfig():
	with open(fname, 'r') as file:
		config = yaml.load(file, Loader=yaml.FullLoader)
		if args.debug:
			print("DEBUG: config loaded %s" % config)
	return config

def saveConfig(config):
	with open(fname, 'w') as file:			       
		file.write(yaml.dump(config))		       
		if args.debug:
			print("DEBUG: config saved %s" % config)
	
def calibrate(loadedConfig):
	print("Place an item of known weight on the scale and enter its weight in grams.\n")
	known_weight = int(input("Weight: "))		       
	print("Calibrating...")
	val = hx.get_weight(5)
	referenceUnit = int(val / known_weight)
	if args.debug:
		print("DEBUG: referenceUnit is %s" % referenceUnit)
	print("Calibration successful, please remove calibration weight.\n")
	loadedConfig["calibratedRefUnit"] = referenceUnit
	saveConfig(loadedConfig)			       		       
	input("Press Enter to continue...")
	

def loop():
	try:
		val = hx.get_weight(5)
		global old_weight
		if args.debug:
			print("DEBUG: raw weight %s" % val)
		weight = int(round(val))
		if args.debug:
			print("DEBUG: weight is %s" % weight)
		if old_weight != weight:
			print(str(round(val)) + " gram.")
			old_weight = weight

		hx.power_down()
		time.sleep(0.001)
		hx.power_up()

		time.sleep(0.5)
			    
	except (KeyboardInterrupt, SystemExit):
		cleanAndExit()

if __name__ == "__main__":

	loadedConfig = loadConfig()
	if args.calibrate:
		calibrate(loadedConfig)

	setup(loadedConfig)
	while True:	    
		loop()
