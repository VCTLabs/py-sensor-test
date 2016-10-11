Python test code and modules for SensorStick
============================================

Things are getting worse, made debs from apt-get source this time, ported
the RPi.GPIO and sht1x patches, rolled back on AadFruit_BMP/GPIO to avoid
the pureio beta stuff and stick with python-smbus.  Tthe following *should*
work on a fresh Raspbian install without rebuilding debs from source.

For manual install of VCT forks of RPi.GPIO and rpisht1x, use:

https://github.com/VCTLabs/RPi.GPIO.git  branch: sf-062

https://github.com/VCTLabs/rpisht1x.git branch master

For manual installs of AdaFruit_Blah, use these commits:

Adafruit_Python_GPIO - 973745604bbb2f6a4094caabf3eb99098db2d3b8

Adafruit_Python_BMP - fe36075719d0f599305bf10d745fe81eb0fd52f6

These packages should still end up in:

/usr/local/lib/python2.7/dist-packages/

For a fresh raspbian image, you should set your locale/keyboard/timezone
(using raspi-config) since everything defaults to GB/UK english, etc.
I also expanded the fs, set overclock to "high" and forced hdmi audio.
In the advanced raspi-config, enable SPI and I2C, then add "i2c-dev" to
/etc/modules (this will remove the blacklist) and reboot.  Make sure
you have an i2c-N device in /dev and you should be good to go.

First install the python test code for the three sensors on the SensorStick::

 # git clone https://github.com/VCTLabs/pi-sensor-test.git
 # cp pi-sensor-test/python/*.py /usr/local/bin/

Build Dependencies
==================

Install some tools and Python dependencies::

 $ sudo -i
 # apt-get update
 # apt-get install git build-essential python-dev python-smbus libi2c-dev python-pip
 # apt-get build-dep python-rpi.gpio
 # pip install git+https://github.com/VCTLabs/RPi.GPIO#egg=RPi.GPIO
 # git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
 # git clone https://github.com/adafruit/Adafruit_Python_BMP.git
 # cd Adafruit_Python_GPIO
 # git checkout 973745604bbb2f6a4094caabf3eb99098db2d3b8
 # python2 setup.py install
 # cd ../Adafruit_Python_BMP/
 # git checkout fe36075719d0f599305bf10d745fe81eb0fd52f6
 # python2 setup.py install
 # exit

BMP085 Sensor Support
=====================

Test BMP library and sensor::

 $ sudo bmp085-test.py

Expected output, should be "reasonable"::

 Temp = 18.70 *C
 Pressure = 100011.00 Pa
 Altitude = 109.81 m
 Sealevel Pressure = 100011.00 Pa

SHT10 and MPU6050 Sensor Support
================================

Install SHT10 library::

 # git clone https://github.com/VCTLabs/rpisht1x.git
 # cd rpiSht1x/src
 # python setup.py install

Test SHT10 library and sensor::

 $ sudo Sht1x-test.py

Expected output should be reasonable, although there may be some warnings::

 Temperature: 18.17 Humidity: 71.220730568 Dew Point: 12.8707463473

.. note:: If you get an error message or no output running any script
          after running the Sht1x-test.py script, try running the
          SensorStick monitor script to clean up the pin config.

Since you already installed python-smbus, you should be ready to go;
now test the MPU smbus interface and sensor::

 $ sudo mpu6050-test.py

Expected output so far is just gyro/accel, with no temperature output::

 gyro data
 ---------
 gyro_xout:  141  scaled:  1
 gyro_yout:  294  scaled:  2
 gyro_zout:  -116  scaled:  -1

 accelerometer data
 ------------------
 accel_xout:  -476  scaled:  -0.029052734375
 accel_yout:  -16088  scaled:  -0.98193359375
 accel_zout:  -2284  scaled:  -0.139404296875
 x rotation:  -81.7485192341
 y rotation:  1.6779160025

Upstream Sources and Related Info
=================================

Python tools (mostly libraries) and test code used for the individual sensors on the sensor stick:

 * BMP085 Pressure/Temperature/Altimeter sensor

  - https://github.com/adafruit/Adafruit_Python_BMP sensor module depends on
  - https://github.com/adafruit/Adafruit_Python_GPIO (wrapper for RPi.GPIO)

Install manually with setup.py, will pull Adafruit_Python_GPIO if needed.


 * SHT10 Humidity/Temperature sensor

  - https://pypi.python.org/pypi/rpiSht1x/1.2  SHT10 sensor module depends on
  - https://pypi.python.org/pypi/RPi.GPIO/0.4.1a RPi GPIO module, python-spidev

Test code for invoking rpiSht1x needs to set the DATA/CLOCK pins using
the physical pin positions (required by RPi.GPIO) so 3 and 5 are SDA1
and SCL1.

Altitude/elevation are calculated (at least by default) and seems to
vary quite a bit without a fixed height.  Need to set a fixed elevation
value as part of setup, pass it to Sealevel Pressure function.

BIG FAT WARNING: The original version of this library dorks up the GPIO
interface and apparently does not let go properly, which causes the BMP
test code to stop working.  Perform a reboot to reset it.  The sht1x lib
now has a workaround for this problem, but still needs to be checked for
SHT10 vs SHT15 transfer coefficients.


 * MPU-6050 Gyroscope and Accelerometer (plus Temp)

  - http://blog.bitify.co.uk/2013/11/reading-data-from-mpu-6050-on-raspberry.html

This is not technically an i2c device, but uses the smbus subset and the
python-smbus module.  The smbus number in the test code is actually the
i2c bus number (I only see i2c-1 on my RPi Model B).
