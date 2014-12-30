# -*- coding: utf-8 -*-
#! /usr/bin/env python
"""
SensorStick-monitor.py: A monitoring script for the SensorStick
    sensors on the SensorStick breakout board.  Requires all the
    sensor modules plus RPi.GPIO (Sht1x and the Adafruit BMP/GPIO).
    Note this requires VCT fork of RPi.GPIO to get fix for sht1x
    protocol nastiness.

simple invocation:
    $ sudo python SensorStick-monitor.py

error logging invocation:
    $ sudo python -u SensorStick-monitor.py > >(tee -a output.log) 2> >(tee error.log >&2)

Licensed under the GNU General Public License (GPL) version 2 or greater.
Copyright 2014 Vanguard Computer Technology Labs, Inc.
"""

import Adafruit_BMP.BMP085 as BMP085
from sht1x.Sht1x import Sht1x as SHT1x

import time
from datetime import datetime

## SHT1x setup; pin numbers in RPi.GPIO module are physical pin positions
dataPin = 3
clkPin = 5
sht1x = SHT1x(dataPin, clkPin, SHT1x.GPIO_BOARD)

## BMP085 setup; default mode is STANDARD
bmp085 = BMP085.BMP085(mode=BMP085.BMP085_HIGHRES)
#bmp085 = BMP085.BMP085()

global verbose
verbose = True

def readBmp085():
    temperature = bmp085.read_temperature()
    pressure = bmp085.read_pressure()
    altitude = bmp085.read_altitude()
    msl_pressure = bmp085.read_sealevel_pressure()
    data = dict([('BMP_TEMP', temperature), ('BMP_PRES', pressure), ('BMP_ALT', altitude), ('BMP_MSL', msl_pressure)])
    if verbose:
        print 'The temperature is {:.2f} deg C'.format(data['BMP_TEMP'])
        print 'The pressure is {:6g} Pa'.format(data['BMP_PRES'])
        print 'The altitude is {:.2f} meters'.format(data['BMP_ALT'])
        print 'The MSL pressure is {:6g} Pa'.format(data['BMP_MSL'])
    return data

def readSht1x():
    temperature = sht1x.read_temperature_C()
    humidity = sht1x.read_humidity()
    dewPoint = sht1x.calculate_dew_point(temperature, humidity)
    data = dict([('SHT_TEMP', temperature), ('SHT_HUM', humidity), ('SHT_DEW', dewPoint)])
    if verbose:
        print 'The temperature is {:.2f} deg C'.format(data['SHT_TEMP'])
        print 'The humidity is {:.1f} percent'.format(data['SHT_HUM'])
        print 'The dew point temperature is {:.2f} deg C'.format(data['SHT_DEW'])
    return data

def get_raw_data():
    # need to pass time as parameter and convert to UTC here
    global timestamp
    utcnow = datetime.utcnow()
    timestamp = utcnow.strftime("%Y-%m-%d %H:%M:%S.%f")
    if verbose:
        print('')
        print 'The time is {}'.format(timestamp)
    bmpdata = readBmp085()
    shtdata = readSht1x()
    data = bmpdata.copy()
    data.update(shtdata)
    return data

def log_raw_data(data):
    version = '01'
    bmpstring = str(data['BMP_PRES'])+" "+str(data['BMP_TEMP'])
    shtstring = str(data['SHT_HUM'])+" "+str(data['SHT_DEW')
    outstring = version+" "+str(timestamp)+" "+bmpstring+" "+shtstring+"\n"
    f.write(outstring)
    f.flush

running = True

try:
    print("SensorStick Data Monitor Script - v0.1")
    print("  Monitor Status: ONLINE")
    ## log raw data to file
    f=open('SensorStick-data.txt','a')

    while running:
        data = get_raw_data()
        log_raw_data(data)
        time.sleep(10.0)

except KeyboardInterrupt:
    print("  Monitor Status: OFFLINE")
    print("")

finally:
    f.close()
