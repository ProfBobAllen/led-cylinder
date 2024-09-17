#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

################################################################
#  Cylinder code:
#
#  30 strands, 9 leds on base, 32 leds on sides, 9 leds on top
#
################################################################

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

######   CYLINDER DEFINITIONS
CYLINDER_HEIGHT  = 50
CYLINDER_WIDTH   = 30

VCylinder = np.zeros((CYLINDER_HEIGHT,CYLINDER_WIDTH))

###  IMPORTANT - this Color uses (G, R, B) not RGB.
colorWhite  = Color(255,255,255)
colorRed    = Color(0,255,0)
colorBlue   = Color(0,0,255)
colorGreen  = Color(255,0,0)
colorDarkGreen  = Color(100,0,0)
colorOrange = Color(35,255,0)
colorYellow = Color(255,255,0)
colorBlack  = Color(0,0,0)
colorPurple = Color(0,55,155)

# datastructures for random dot movements.
xCoord = []
yCoord = []
numDots = 10
for i in range(numDots):
    xCoord.append(random.randint(0,CYLINDER_WIDTH-3))
    yCoord.append(random.randint(0,CYLINDER_HEIGHT-3))

def placeDots(strip,color):
    for i in range(numDots):
        setColorAt(strip,color,xCoord[i],yCoord[i])
        setColorAt(strip,color,xCoord[i]+1,yCoord[i])
        setColorAt(strip,color,xCoord[i]+2,yCoord[i])
        setColorAt(strip,color,xCoord[i],yCoord[i]+1)
        setColorAt(strip,color,xCoord[i]+1,yCoord[i]+1)
        setColorAt(strip,color,xCoord[i]+2,yCoord[i]+1)
        setColorAt(strip,color,xCoord[i],yCoord[i]+2)
        setColorAt(strip,color,xCoord[i]+1,yCoord[i]+2)
        setColorAt(strip,color,xCoord[i]+2,yCoord[i]+2)

def displayDots(strip,dotColor,bgColor):
    setCylinderColor(strip, bgColor)
    for i in range(50):
        placeDots(strip,dotColor)
        strip.show()
        time.sleep(0.125)
        placeDots(strip,bgColor)
        adjustDots()
    
def adjustDots2():
    for i in range(numDots):
        if random.randint(0,2) == 0:
            xCoord[i] = (xCoord[i] + 1)%CYLINDER_WIDTH
        else:
            xCoord[i] = (xCoord[i] + CYLINDER_WIDTH-1)%CYLINDER_WIDTH
        if random.randint(0,2) == 0:
            yCoord[i] = (yCoord[i] + 1)%CYLINDER_HEIGHT
        else:
            yCoord[i] = (yCoord[i] + CYLINDER_HEIGHT-1)%CYLINDER_HEIGHT
    
def adjustDots():
    for i in range(numDots):
        xCoord[i] = (xCoord[i] + 1)%(CYLINDER_WIDTH-2)
        yCoord[i] = (yCoord[i] + 1)%(CYLINDER_HEIGHT-2)


# DEBUG CODE::: VCylinderTop shows the top 5 rows of VCylinder
def topVCylinder():
    print("TOP...")
    for count in range (5):
        print(VCylinder[count])

# Barber Pole init in VCylinder
def makeBarberPole():
    clearVCylinder()
    for row in range(CYLINDER_HEIGHT):
        for col in range(row,row+6):
            VCylinder[row][col%CYLINDER_WIDTH] = 1
            VCylinder[row][(col+10)%CYLINDER_WIDTH] = 1
            VCylinder[row][(col+20)%CYLINDER_WIDTH] = 1

def spinBarberPole(strip,color1,color2):
    makeBarberPole()
    for row in range(CYLINDER_HEIGHT):
        displayVCylinder12s(strip,color1,color2)
        strip.show()
        time.sleep(0.05)
        adjustVCylinderDown()
        for col in range(row,row+6):
            VCylinder[0][col%CYLINDER_WIDTH] = 1
            VCylinder[0][(col+10)%CYLINDER_WIDTH] = 1
            VCylinder[0][(col+20)%CYLINDER_WIDTH] = 1

# Barber Pole init in VCylinder
def makeBarberPole2():
    clearVCylinder()
    for row in range(CYLINDER_HEIGHT):
        for col in range(row,row+16):
            VCylinder[row][col%CYLINDER_WIDTH] = 1

def spinBarberPole2(strip,color1,color2):
    makeBarberPole2()
    for row in range(CYLINDER_HEIGHT):
        displayVCylinder12s(strip,color1,color2)
        strip.show()
        time.sleep(0.05)
        adjustVCylinderDown()
        for col in range(row,row+16):
            VCylinder[0][col%CYLINDER_WIDTH] = 1

# Falling Bars - horizontal colors moving down - two COLORS
def fallingBars(strip, color1, color2):
    setCylinderColor(strip, color1)
    clearVCylinder()
    for count in range(100):
        adjustVCylinderDown()
        strand = (count//5)%2
        for col in range(CYLINDER_WIDTH):
            VCylinder[0][col]=strand
        displayVCylinder12s(strip,color1,color2)
        strip.show()

# Clear the cylinder array - set all to zero.
def clearVCylinder():
    for col in range(CYLINDER_WIDTH):
        for row in range(CYLINDER_HEIGHT):
            VCylinder[row][col] = 0

# Display cylinder array, only where there is a 1, with specified COLOR
def displayVCylinder12s (strip, color1, color2):
    for col in range (CYLINDER_WIDTH):
        for row in range (CYLINDER_HEIGHT):
            if VCylinder[row][col] == 0:
                setColorAt(strip,color1,col,row)
            else:
                setColorAt(strip,color2,col,row)


# Display cylinder array, only where there is a 1, with specified COLOR
def displayVCylinder1s (strip, color):
    for col in range (CYLINDER_WIDTH):
        for row in range (CYLINDER_HEIGHT):
            if VCylinder[row][col] == 1:
                setColorAt(strip,color,col,row)

# Adjust cylinder array, shifting each row down one, top gets all zeros
def adjustVCylinderDown ():
    for row in range (CYLINDER_HEIGHT - 1,0,-1):
        for col in range(CYLINDER_WIDTH):
            VCylinder[row][col] = VCylinder[row-1][col]
    for col in range (CYLINDER_WIDTH):
        VCylinder[0][col] = 0

# Snow COLOR1 down on a cylinder of COLOR2
def christmassnow (strip, color1, color2):
    clearVCylinder()
    setCylinderColor(strip,color2)
    for count in range (50):
        displayVCylinder1s(strip,color2)
        adjustVCylinderDown()
        for col in range (CYLINDER_WIDTH):
            if random.randint(0,5) == 0:
                VCylinder[0][col] = 1
        displayVCylinder1s(strip,color1)
        strip.show()
        time.sleep(0.05)

# Snow COLOR1 down on a cylinder of COLOR2
def snow (strip, color1, color2):
    clearVCylinder()
    setCylinderColor(strip,color2)
    for count in range (50):
        displayVCylinder1s(strip,color2)
        adjustVCylinderDown()
        for col in range (CYLINDER_WIDTH):
            if random.randint(0,5) == 0:
                VCylinder[0][col] = 1
        displayVCylinder1s(strip,color1)
        strip.show()
        time.sleep(0.05)

def spin2Colors(stip, color1,color2):
    for times in range(30):
        for x in range(CYLINDER_WIDTH):
            for y in range(CYLINDER_HEIGHT):
                if (x//5)%2 == 0:
                    setColorAt(strip, color1, (x+times)%CYLINDER_WIDTH, y);
                else:
                    setColorAt(strip, color2, (x+times)%CYLINDER_WIDTH, y);
        strip.show();
        time.sleep(0.05)

def wrap2Colors(stip, color1,color2):
    for x in range(CYLINDER_WIDTH):
        for y in range(CYLINDER_HEIGHT):
            if (x//5)%2 == 0:
                setColorAt(strip, color1, x, y);
            else:
                setColorAt(strip, color2, x, y);
        strip.show();

def wrapColor(stip, color):
    for x in range(CYLINDER_WIDTH):
        for y in range(CYLINDER_HEIGHT):
            setColorAt(strip, color, x, y);
        strip.show();

def purpleTest(strip):
    for b in range(50,256,10):
        for r in range(0,b-25,10):
            setCylinderColor(strip,Color(0,r,b))
    #        print('blue: ' + b + ' red: ' + r)
            time.sleep(.1)

            

def growColorUp(strip,color1,color2):
    setCylinderColor(strip,color1)
    for y in range(CYLINDER_HEIGHT-1,-1,-1):
        for x in range(CYLINDER_WIDTH):
            setColorAt(strip,color2,x,y)
        strip.show()
        time.sleep(.01)

def pourColorDown(strip,color1,color2):
    setCylinderColor(strip,color1)
    for y in range(CYLINDER_HEIGHT):
        for x in range(CYLINDER_WIDTH):
            setColorAt(strip,color2,x,y)
        strip.show()
        time.sleep(.01)

def ringDrop(strip,color1,color2):
    setCylinderColor(strip,color1)
    for y in range(CYLINDER_HEIGHT):
        for x in range(CYLINDER_WIDTH):
            setColorAt(strip,color2,x,y)
        strip.show()
        time.sleep(.01)
        for x in range(CYLINDER_WIDTH):
            setColorAt(strip,color1,x,y)
        strip.show()

# Set color at x,y  !!!!  DOES NOT SHOW.... you do it when you want it
def setColorAt(strip, color, x, y):
    if x >= 0 and x < CYLINDER_WIDTH and y >= 0 and y < CYLINDER_HEIGHT:
        strandOffset = x * CYLINDER_HEIGHT
        if x%2 != 0:
            bulb = strandOffset + y
        else:
            bulb = strandOffset + (CYLINDER_HEIGHT - 1  - y)
        strip.setPixelColor(bulb, color)

#  Test setColorAt by trickling a color down from top to bottom
def trickleDown (strip, color):
    for row in range(CYLINDER_HEIGHT):
        for col in range(CYLINDER_WIDTH):
            setColorAt(strip, color, col, row)
        if row%2 == 0:
            strip.show()
    strip.show()

#  Set whole cylinder to one color
def setChristmasTreerColor (strip, color):
    for i in range (20,LED_COUNT,1):
        strip.setPixelColor(i,color)
    strip.show()

#  Set whole cylinder to one color
def setCylinderColor (strip, color):
    for i in range (LED_COUNT):
        strip.setPixelColor(i,color)
    strip.show()

# Set one strand to one COLOR  !!!!! DOES NOT SHOW you do it when you want it
def setStrandColor(strip, strand, color):
    if strand >= 0 and strand < CYLINDER_WIDTH:
        for bulb in range(CYLINDER_HEIGHT):
            setColorAt(strip, color, strand, bulb)

# Two color Stripes on cylinder, given two colors
def stripes (strip, color1, color2):
    for strand in range (CYLINDER_WIDTH):
        if strand%2 == 0:
            setStrandColor(strip, strand, color1)
        else:
            setStrandColor(strip, strand, color2)
    strip.show()

# Three color Stripes on cylinder, given three colors
def stripes3 (strip, color1, color2, color3):
    for strand in range (CYLINDER_WIDTH):
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

def wrapChristmasColor(stip, color):
    for x in range(CYLINDER_WIDTH):
        for y in range(14,CYLINDER_HEIGHT,1):
            setColorAt(strip, color, x, y);
        strip.show();


# Random Sparkle sets cylinder to COLOR then places random colors at random places
def randomChristmasSparkle (strip):
    setCylinderColor(strip,colorBlack)
    wrapChristmasColor(strip, colorDarkGreen) 
    count = 0
    while True:
        y = random.randint(0,CYLINDER_HEIGHT-14)+14
        x = random.randint(0,CYLINDER_WIDTH)
        if random.randint(0,10)<3:
           setColorAt(strip, Color(random.randint(0,255),random.randint(0,255),random.randint(0,255)),x,y)
        else:
           setColorAt(strip, colorDarkGreen,x,y)
        count = count + 1
        if count%10 == 0:
            strip.show()

# Random Sparkle sets cylinder to COLOR then places random colors at random places
def randomSparkle (strip, color):
    setCylinderColor(strip, color)
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
            print('random dots ')
            #setCylinderColor(strip, colorWhite)
            #time.sleep(5)
            #print ('Theater chase animations.')
            #theaterChase(strip, Color(127, 127, 127))  # White theater chase
            #theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            #theaterChaseRainbow(strip)
            #theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            #print('white cylinder')
            #time.sleep(5)
            #print('green cylinder')
            #setCylinderColor(strip, Color(222,0,00))
            #time.sleep(5)
            #print('blue cylinder')
            #setCylinderColor(strip, Color(0,0,222))
            #time.sleep(5)
            #print('snow')
            #snow(strip,Color(100,100,100),Color(255,0,0))
            #print('white-- cylinder')
            #setCylinderColor(strip, Color(100,100,100))
            #setCylinderColor(strip, Color(100,100,100))
            #setCylinderColor(strip, Color(100,100,100))
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

        setCylinderColor(strip, colorBlack)


    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)

