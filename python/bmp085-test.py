#!/usr/bin/python
# modifed version of Adafruit example simpletest.py

# enable debug output by uncommenting the following two lines:
#import logging
#logging.basicConfig(level=logging.DEBUG)

import Adafruit_BMP.BMP085 as BMP085

# Connecting to the exposed RPi GPIO should find the right bus number
# (defaults to 1 on BeagleBone).
#sensor = BMP085.BMP085()

# can override the bus number if necessary:
#sensor = BMP085.BMP085(busnum=2)

# Can also optionally change the BMP085 mode to one of BMP085_ULTRALOWPOWER, 
# BMP085_STANDARD, BMP085_HIGHRES, or BMP085_ULTRAHIGHRES.  See the BMP085
# datasheet for more details on the meanings of each mode (accuracy and power
# consumption are primarily the differences).  The default mode is STANDARD.
sensor = BMP085.BMP085(mode=BMP085.BMP085_HIGHRES)

print 'Temp = {0:0.2f} *C'.format(sensor.read_temperature())
print 'Pressure = {0:0.2f} Pa'.format(sensor.read_pressure())
print 'Altitude = {0:0.2f} m'.format(sensor.read_altitude())
print 'Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure())
