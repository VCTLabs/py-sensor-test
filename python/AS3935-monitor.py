# -*- coding: utf-8 -*-
#! /usr/bin/env python
"""
AS3935-monitor.py: A monitoring script for the AS3935 lightning
    sensor on the MOD-1016 v6 breakout board.  Requires both the
    RaspberryPi-AS3935 and RPi.GPIO Python modules.  Note that
    the reset function requires VCT fork of RaspberryPi-AS3935.

simple invocation:
    $ sudo python AS3935-monitor.py

error logging invocation:
    $ sudo python -u AS3935-monitor.py > >(tee -a output.log) 2> >(tee error.log >&2)

Licensed under the GNU General Public License (GPL) version 2 or greater.
Copyright 2014 Vanguard Computer Technology Labs, Inc.
"""

from RPi_AS3935 import RPi_AS3935
import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)

## Rev 1 Raspberry Pi: bus=0
## Rev 2 and later Raspberry Pi: bus=1
## All: address=<i2c add>

sensor = RPi_AS3935(address=0x03, bus=1)

## Uncomment to reset all registers to factory default values.
sensor.reset()

sensor.calibrate(tun_cap=0x03)
time.sleep(0.002)
sensor.set_indoors(True)
sensor.set_noise_floor(0)

## uncomment/set to filter out false positives
sensor.set_min_strikes(5)

def handle_interrupt(channel):
    time.sleep(0.003)
    global sensor
    reason = sensor.get_interrupt()
    if reason == 0x01:
        print("Noise level too high - adjusting")
        sensor.raise_noise_floor()
    elif reason == 0x04:
        print("Disturber detected - masking")
        sensor.set_mask_disturber(True)
    elif reason == 0x08:
        now = datetime.now()
        distance = sensor.get_distance()
        if distance < 2:
            print("Overhead lightning detected - distance = " + str(distance) + " km at %s ") % now.strftime("%H:%M:%S.%f")[:-3],now.strftime("%Y-%m-%d")
        elif distance > 40:
            print("Distant lightning detected - distance = " + str(distance) + " kms at %s") % now.strftime("%H:%M:%S.%f")[:-3],now.strftime("%Y-%m-%d")
        else:
            print("Lightning detected - distance = " + str(distance) + " kms at %s") % now.strftime("%H:%M:%S.%f")[:-3],now.strftime("%Y-%m-%d")

irq_pin = 17
cs_pin = 24

GPIO.setup(irq_pin, GPIO.IN)
GPIO.add_event_detect(irq_pin, GPIO.RISING, callback=handle_interrupt)

running = True

try:
    print("AS3935 Lightning Detection Monitor Script - v0.1")
    print("  Monitor Status: ONLINE")
    print("")

    while running:
        time.sleep(1.0)

except KeyboardInterrupt:
    print("  Monitor Status: OFFLINE")
    print("")

finally:
    GPIO.cleanup() # clean up GPIO on CTRL+C exit
