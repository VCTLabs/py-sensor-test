Python test code and modules for SensorStick
============================================

This can get tricky, depending on which python install tools or deb
packages are used.  Avoid easy_install-foo* and pip, use the setup.py
install metyhod below, and everything *should* end up in the dist dir:
/usr/local/lib/python2.7/dist-packages/.  The setup scripts will install
required dependencies; everything should work, with the caveat below that
the rpiSHT1x library conflicts with the BMP Adafruit interface.  Since the
latter is much newer than the former, well, ...

For a fresh respbian image, you should set your locale/keyboard/timezone
(using raspi-config) since everything defaults to GB/UK english, etc.  I
also expanded the fs, set overclock to "high" and forced hdmi audio.  In 
the advanced raspi-config, enable SPI and I2C, then add "i2c-dev" to 
/etc/modules (this will remove the blacklist) and reboot.  Make sure you
have an i2c-N device in /dev and you should be good to go.

BMP085 Sensor Support
=====================

Install BMP library::

 # atp-get update
 # apt-get install git build-essential python-dev python-smbus libi2c-dev
 # git clone https://github.com/adafruit/Adafruit_Python_BMP.git
 # cd Adafruit_Python_BMP
 # python setup.py install

Test BMP library and sensor::

 # cd ~/Adafruit_Python_BMP
 # python examples/simpletest.py

Expected output, should be "reasonable"::

 Temp = 18.70 *C
 Pressure = 100011.00 Pa
 Altitude = 109.81 m
 Sealevel Pressure = 100011.00 Pa

SHT10 Sensor Support
====================

Install SHT10 library::

 # wget https://pypi.python.org/packages/source/r/rpiSht1x/rpiSht1x-1.2.tar.gz
 # tar xvzf rpiSht1x-1.2.tar.gz
 # cd rpiSht1x-1.2/
 # python setup.py install

Test SHT10 library and sensor; install python test code for SHT and MPU sensors::

 # git clone git@github.com:VCTLabs/pi-sensor-test.git
 # cp pi-sensor-test/Sht1x-test.py /usr/local/bin/
 # Sht1x-test.py

Expected output should be reasonable, although there may be some warnings::

 Temperature: 18.17 Humidity: 71.220730568 Dew Point: 12.8707463473

Test MPU smbus interface and sensor::

 # cp pi-sensor-test/mpu-6050.py /usr/local/bin/
 # mpu-6050.py

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

Python tools (mostly libraries) and test code used for the individual sensors
on the sensor stick:

 * BMP085 Pressure/Temperature/Altimeter sensor

  - https://github.com/adafruit/Adafruit_Python_BMP sensor module depends on 
  - https://github.com/adafruit/Adafruit_Python_GPIO (wrapper for RPi.GPIO)

Insall manually with setup.py, will pull Adafruit_Python_GPIO if needed.

 * SHT10 Humidity/Temperature sensor

  - https://pypi.python.org/pypi/rpiSht1x/1.2  SHT10 sensor module depends on
  - https://pypi.python.org/pypi/RPi.GPIO/0.4.1a RPi GPIO module, python-spidev

Test code for invoking rpiSht1x needs to set the DATA/CLOCK pins using the
physical pin positions (required by RPi.GPIO) so 3 and 5 are SDA1 and SCL1.

Altitude/elevation are calculated (at least by default) and seems to vary
quite a bit for a fixed height.  Need to see if we can set the value instead.

BIG FAT WARNING: The 1.2 version dorks up the GPIO interface so the BMP test
code stops working.  Perform a reboot to fix it.  The installed "eggs" aren't
like previously installed packages for BMP, not sure yet what got b0rked.  The
sht1x lib should probably be ported to the AdaFruit wrapper interface.


 * MPU-6050 Gyroscope and Accelerometer (plus Temp)

  - http://blog.bitify.co.uk/2013/11/reading-data-from-mpu-6050-on-raspberry.html

This is not technically an i2c device, but uses the smbus subset and the
python-smbus module.  The smbus number in the test code is actually the i2c
bus number (I only see i2c-1 on my RPi Model B).
