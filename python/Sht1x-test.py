#!/usr/bin/python

from sht1x.Sht1x import Sht1x as SHT1x

## Note: pin numbers in RPi.GPIO module are physical pin positions, and
## not GPIO pin numbers.
dataPin = 3
clkPin = 5

sht1x = SHT1x(dataPin, clkPin, SHT1x.GPIO_BOARD)

temperature = sht1x.read_temperature_C()
humidity = sht1x.read_humidity()
dewPoint = sht1x.calculate_dew_point(temperature, humidity)

print("Temperature: {} Humidity: {} Dew Point: {}".format(temperature, humidity, dewPoint))
