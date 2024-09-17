#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import *
import argparse
import random
import numpy as np

# LED strip configuration:
LED_COUNT      = 1500      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

######   TREE DEFINITIONS
TREE_HEIGHT  = 50
TREE_WIDTH   = 30

VTree = np.zeros((TREE_HEIGHT,TREE_WIDTH))

###  IMPORTANT - this Color uses (G, R, B) not RGB.
colorWhite  = Color(255,255,255)
colorRed    = Color(0,255,0)
colorBlue   = Color(0,0,255)
colorGreen  = Color(255,0,0)
colorOrange = Color(35,255,0)
colorYellow = Color(255,255,0)
colorBlack  = Color(0,0,0)


# Jack-o-lantern - orange with yellow/white eyes/mouth, green stem
def jacko(strip):
    setTreeColor(strip, colorOrange)
    # Make stem at top
    for col in range(TREE_WIDTH):
        for row in range(5):
            setColorAt(strip,colorGreen,col,row)

    # Make eyes
    eyecols = [2,3,6,7]
    eyerows = range(45,50)
    for count in range(100):
        for col in eyecols:
            for row in eyerows:
                if random.randint(0,4)>0:
                    setColorAt(strip,colorWhite,col,row)
                else:
                    setColorAt(strip,colorYellow,col,row)
        # Make mouth
        for col in range(2,8):
            for row in range(100,102):
                if random.randint(0,4)>0:
                    setColorAt(strip,colorWhite,col,row)
                else:
                    setColorAt(strip,colorYellow,col,row)

        for col in range(3,7):
            for row in range(102,104):
                if random.randint(0,4)>0:
                    setColorAt(strip,colorWhite,col,row)
                else:
                    setColorAt(strip,colorYellow,col,row)

        for col in range(4,5):
            for row in range(104,106):
                if random.randint(0,4)>0:
                    setColorAt(strip,colorWhite,col,row)
                else:
                    setColorAt(strip,colorYellow,col,row)
        strip.show()
        time.sleep(0.1)

# DEBUG CODE::: VTreeTop shows the top 5 rows of VTree
def topVTree():
    print("TOP...")
    for count in range (5):
        print(VTree[count])

# Falling Bars - horizontal colors moving down - two COLORS
def fallingBars(strip, color1, color2):
    setTreeColor(strip, color1)
    clearVTree()
    for count in range(300):
        adjustVTreeDown()
        strand = (count//5)%2
        for col in range(TREE_WIDTH):
            VTree[0][col]=strand
        displayVTree12s(strip,color1,color2)
        strip.show()

# Clear the tree array - set all to zero.
def clearVTree():
    for col in range(TREE_WIDTH):
        for row in range(TREE_HEIGHT):
            VTree[row][col] = 0

# Display tree array, only where there is a 1, with specified COLOR
def displayVTree12s (strip, color1, color2):
    for col in range (TREE_WIDTH):
        for row in range (TREE_HEIGHT):
            if VTree[row][col] == 0:
                setColorAt(strip,color1,col,row)
            else:
                setColorAt(strip,color2,col,row)


# Display tree array, only where there is a 1, with specified COLOR
def displayVTree1s (strip, color):
    for col in range (TREE_WIDTH):
        for row in range (TREE_HEIGHT):
            if VTree[row][col] == 1:
                setColorAt(strip,color,col,row)

# Adjust tree array, shifting each row down one, top gets all zeros
def adjustVTreeDown ():
    for row in range (TREE_HEIGHT - 1,0,-1):
        for col in range(TREE_WIDTH):
            VTree[row][col] = VTree[row-1][col]
    for col in range (TREE_WIDTH):
        VTree[0][col] = 0

# Snow COLOR1 down on a tree of COLOR2
def snow (strip, color1, color2):
    clearVTree()
    setTreeColor(strip,color2)
    for count in range (100):
        displayVTree1s(strip,color2)
        adjustVTreeDown()
        for col in range (TREE_WIDTH):
            if random.randint(0,5) == 0:
                VTree[0][col] = 1
        displayVTree1s(strip,color1)
        strip.show()

def ratRace(stip, color):
    for x in range(TREE_WIDTH):
        for y in range(TREE_HEIGHT):
            setColorAt(strip, color, x, y);
        strip.show();

# Set color at x,y  !!!!  DOES NOT SHOW.... you do it when you want it
def setColorAt(strip, color, x, y):
    if x >= 0 and x < TREE_WIDTH and y >= 0 and y < TREE_HEIGHT:
        strandOffset = x * TREE_HEIGHT
        if x%2 != 0:
            bulb = strandOffset + y
        else:
            bulb = strandOffset + (TREE_HEIGHT - 1  - y)
        strip.setPixelColor(bulb, color)

#  Test setColorAt by trickling a color down from top to bottom
def trickleDown (strip, color):
    for row in range(TREE_HEIGHT):
        for col in range(TREE_WIDTH):
            setColorAt(strip, color, col, row)
        if row%2 == 0:
            strip.show()
    strip.show()

#  Set whole tree to one color
def setTreeColor (strip, color):
    for i in range (LED_COUNT):
        strip.setPixelColor(i,color)
    strip.show()

# Set one strand to one COLOR  !!!!! DOES NOT SHOW you do it when you want it
def setStrandColor(strip, strand, color):
    if strand >= 0 and strand < TREE_WIDTH:
        for bulb in range(TREE_HEIGHT):
            setColorAt(strip, color, strand, bulb)

# Two color Stripes on tree, given two colors
def stripes (strip, color1, color2):
    for strand in range (TREE_WIDTH):
        if strand%2 == 0:
            setStrandColor(strip, strand, color1)
        else:
            setStrandColor(strip, strand, color2)
    strip.show()

# Three color Stripes on tree, given three colors
def stripes3 (strip, color1, color2, color3):
    for strand in range (TREE_WIDTH):
        if strand%3 == 0:
            setStrandColor(strip, strand, color1)
        else:
            if strand%3 == 1:
                setStrandColor(strip, strand, color2)
            else:
                setStrandColor(strip, strand, color3)
    strip.show()

# Spin two colors - stripes with rotation
def spinTwo (strip, color1, color2):
    for i in range(10):
        stripes (strip, color1, color2)
        time.sleep(0.5)
        stripes (strip, color2, color1)
        time.sleep(0.5)

# Spin three colors - stripes with rotation
def spinThree (strip, color1, color2, color3):
    for i in range(20):
        stripes3 (strip, color1, color2, color3)
        time.sleep(0.1)
        stripes3 (strip, color2, color3, color1)
        time.sleep(0.1)
        stripes3 (strip, color3, color1, color2)
        time.sleep(0.1)


# Random Sparkle sets tree to COLOR then places random colors at random places
def randomSparkle (strip, color):
    setTreeColor(strip, color)
    for count in range (1500):
        strip.setPixelColor(random.randint(0,LED_COUNT-1), Color(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        if count%10 == 0:
            strip.show()






#######################  OLD INITIAL TESTS ###############################33

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=5):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=5, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

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

def rainbow(strip, wait_ms=2, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        #time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=2, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        #time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=5):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            #time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def trashcan():
            print('falling bars red and white')
            fallingBars(strip,colorWhite,colorRed)
            print('random sparkle')
            randomSparkle(strip,colorGreen)
            print('trickle Down green')
            trickleDown(strip, colorGreen)
            print('falling bars green and red ')
            fallingBars(strip,colorGreen,colorRed)
            print('3 stripes green, white, red')
            stripes3(strip, colorGreen, colorRed, colorWhite)
            time.sleep(5)
            print('trickle Down blue')
            trickleDown(strip, colorBlue)
            print('falling bars blue and Yellow ')
            fallingBars(strip,colorBlue,colorYellow)
            print('spin two green red')
            spinTwo(strip, colorRed, colorGreen)
            print('random sparkle')
            randomSparkle(strip,colorRed)
            print('spin three blue green red')
            spinThree(strip, colorRed, colorGreen, colorGreen)
            time.sleep(1)
            print('trickle Down orange')
            trickleDown(strip, colorOrange)
            print('falling bars colorOrange and Black ')
            fallingBars(strip,colorOrange,colorBlack)
            print('random sparkle yellow')
            randomSparkle(strip,colorOrange)
            #setTreeColor(strip, colorWhite)
            #time.sleep(5)
            #print ('Theater chase animations.')
            #theaterChase(strip, Color(127, 127, 127))  # White theater chase
            #theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            #theaterChaseRainbow(strip)
            #theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            #print('white tree')
            #time.sleep(5)
            #print('green tree')
            #setTreeColor(strip, Color(222,0,00))
            #time.sleep(5)
            #print('blue tree')
            #setTreeColor(strip, Color(0,0,222))
            #time.sleep(5)
            #print('snow')
            #snow(strip,Color(100,100,100),Color(255,0,0))
            #print('white-- tree')
            #setTreeColor(strip, Color(100,100,100))
            #setTreeColor(strip, Color(100,100,100))
            #setTreeColor(strip, Color(100,100,100))
            # print ('Color wipe animations.')
            # colorWipe(strip, Color(255, 0, 0))  # Red wipe
            # colorWipe(strip, Color(0, 255, 0))  # Blue wipe
            # colorWipe(strip, Color(0, 0, 255))  # Green wipe
            # print ('Rainbow animations.')
            # rainbow(strip)
            # rainbowCycle(strip)



# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            print('white tree')
            setTreeColor(strip, colorBlue)
            ratRace(strip, colorRed);
            print('falling bars red and white')
            setTreeColor(strip, colorWhite)
            fallingBars(strip,colorWhite,colorRed)
            print('random sparkle')
            randomSparkle(strip,colorGreen)
            print('trickle Down green')
            trickleDown(strip, colorGreen)
            print('falling bars green and red ')
            fallingBars(strip,colorGreen,colorRed)
            print('3 stripes green, white, red')
            stripes3(strip, colorGreen, colorRed, colorWhite)
            time.sleep(5)
            print('trickle Down blue')
            trickleDown(strip, colorBlue)
            print('falling bars blue and Yellow ')
            fallingBars(strip,colorBlue,colorYellow)
            print('spin two green red')
            spinTwo(strip, colorRed, colorGreen)
            print('random sparkle')
            randomSparkle(strip,colorRed)
            print('spin three blue green red')
            spinThree(strip, colorRed, colorGreen, colorGreen)
            time.sleep(1)
            print('trickle Down orange')
            trickleDown(strip, colorOrange)
            print('falling bars colorOrange and Black ')
            fallingBars(strip,colorOrange,colorBlack)
            print('random sparkle yellow')
            randomSparkle(strip,colorOrange)
            #setTreeColor(strip, colorWhite)
            #time.sleep(5)
            #print ('Theater chase animations.')
            #theaterChase(strip, Color(127, 127, 127))  # White theater chase
            #theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            #theaterChaseRainbow(strip)
            #theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            #print('white tree')
            #time.sleep(5)
            #print('green tree')
            #setTreeColor(strip, Color(222,0,00))
            #time.sleep(5)
            #print('blue tree')
            #setTreeColor(strip, Color(0,0,222))
            #time.sleep(5)
            #print('snow')
            #snow(strip,Color(100,100,100),Color(255,0,0))
            #print('white-- tree')
            #setTreeColor(strip, Color(100,100,100))
            #setTreeColor(strip, Color(100,100,100))
            #setTreeColor(strip, Color(100,100,100))
            # print ('Color wipe animations.')
            # colorWipe(strip, Color(255, 0, 0))  # Red wipe
            # colorWipe(strip, Color(0, 255, 0))  # Blue wipe
            # colorWipe(strip, Color(0, 0, 255))  # Green wipe
            # print ('Rainbow animations.')
            # rainbow(strip)
            # rainbowCycle(strip)


    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)

