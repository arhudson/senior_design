import time
from rpi_ws281x import *
import argparse

# LED strip configuration:
LED_COUNT      = 4    # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Functions to illuminate LEDs
def readPatternFromFile():
    pat_file = open('pattern_file.txt', 'r')
    vals = pat_file.read().split(',')
    pat_file.close()
    return vals

def solidColor(strip, pattern):
    j = 0
    while j < len(pattern):
        for i in range(strip.numPixels()):
            #print 'current light is:', i
            print j
            strip.setPixelColor(i, Color(int(pattern[j]),int(pattern[j+1]),int(pattern[j+2])))
            strip.show()
            j+=3
            time.sleep(.05)
        
def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)
    
def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
        
if __name__ == '__main__':
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, strip_type=ws.WS2811_STRIP_RGB)
    strip.begin()

    vals = readPatternFromFile()
    print vals
    
    try:
        print('Select a color to display:\n1. Red\n2. Green\n3. Blue')
        choice = int(raw_input(''))
        if(choice==1):
            color=Color(255,0,0)
        elif(choice==2):
            color=Color(0,255,0)
        else:
            color=Color(0,0,255)
            
        while True:
            print('Starting display.')
            solidColor(strip, vals)
            #rainbow(strip)
            
    except KeyboardInterrupt:
        print('\nClearing strands.')
        solidColor(strip, Color(0,0,0))

