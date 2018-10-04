#!/usr/bin/env python3

import time
from rpi_ws281x import *
import argparse
import random

# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
RGB_VALS = []

def generateVals():
	val_file = open('light_values.txt','w')
	for i in range(input('Number of lights?: ')*3):
		line = str(random.randint(0,255))
		val_file.write(line+str(','))
	val_file.close()
		
def parseFile():
	val_file = open('light_values.txt','r')
	vals = val_file.read().split(',')
	vals.pop()
	val_file.close()
	return vals
	
def illuminateLights(strip):
	#TODO
	global RGB_VALS
	j = 0
	while j < (LED_COUNT * 3):
		for i in range(strip.numPixels()):
			color = Color(int(RGB_VALS[j]),int(RGB_VALS[j+1]),int(RGB_VALS[j+2]))
			strip.setPixelColor(i, color)
			strip.show
			time.sleep(.05)
			j+=3
			
def clearLights(strip):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, Color(0,0,0))
		strip.show
		time.sleep(.01)
		
if __name__ == '__main__':
	#maybe use argparser?
	#parseFile()
	global RGB_VALS 
	#generateVals()
	
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	
	RGB_VALS = parseFile()
	print RGB_VALS
	
	try:
		while True:
			illuminateLights(strip)
	except KeyboardInterrupt:
		print('\nClearing lights')
		clearLights(strip)
			
			
			
			
			
			
