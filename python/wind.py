# -*- coding: utf-8 -*-
#! /usr/bin/env python
"""
wind.py - Driver for wind direction sensor using GPIO pins on RPi.
Requires RPi.GPIO
See http://www.yoctopuce.com/EN/article/how-to-measure-wind-part-2

Licensed under the GNU General Public License (GPL) version 2 or greater.
Copyright 2014 Vanguard Computer Technology Labs, Inc.
"""

import RPi.GPIO as GPIO

# Constant orientation lookup table for wind direction, 0th and 31st indexes are invalid.
direction_orientation = ( -1,   0,  72, 12, 144, 132,  84, 120,
                         216, 348, 204, 24, 156, 168, 192, 180,
                         288, 300,  60, 48, 276, 312,  96, 108,
                         228, 336, 240, 36, 264, 324, 252,  -1)

# GPIO sensor bits for wind direction.
direction_pins = (11, # bit 0
                  12, # bit 1
                  13, # bit 2
                  15, # bit 3
                  16) # bit 4

def initialize():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(direction_pins, GPIO.OUT, initial=GPIO.LOW)
    GPIO.cleanup()
    GPIO.setup(direction_pins, GPIO.IN)

def get_direction():
    result = 0

    for index, pin in enumerate(direction_pins):
        result = result | GPIO.input(pin) << index

    try:
        return direction_orientation[result]
    except IndexError:
        return -1

def finalize():
    GPIO.cleanup()

if __name__ == '__main__':
    initialize()
    print "Wind direction:", get_direction(), "degrees"
    finalize()
