#!/usr/bin/python

# PaSS
# Panda Sensor System ?

# This is meant to be run in cron
# something like this runs it every 2 minutes:

# m h  dom mon dow   command
# */2 * * * * /home/pi/panda/pass_logger.py


# for sht21
# https://github.com/jaques/sht21_python
# MIT License
from sht21 import SHT21


# for bmp180
# https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_BMP085
# BSD Liscense
from Adafruit_BMP085 import BMP085
bmp = BMP085(0x77)


# For ADC
# https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_ADS1x15
# BSD license
from Adafruit_ADS1x15 import ADS1x15


# For TLS2561
# https://github.com/seanbechhofer/raspberrypi/blob/master/python/TSL2561.py
# No license
# Uses Adafruit I2C
# Modified by Paul
from TSL2561 import TSL2561
tsl = TSL2561()


# Timekeeping
import time
from time import strftime


# For ppm calculation
#import numpy as np


# ADC setup
ADS1115 = 0x01    # 16-bit ADC
gain = 6144  # +/- 6.144V
sps = 475  # 475 samples per second
adc = ADS1x15(ic=ADS1115)


# Main Loop
if __name__ == "__main__":
    # SHT21
    # Temperature and Humidity
    try:
        stemp = round(SHT21(1).read_temperature(), 2)
        shumid = round(SHT21(1).read_humidity(), 2)
        print "Temperature:   %s C" % stemp
        print "Humidity:      %s rh" % shumid
    except TypeError:
        print "Invalid Checksum"

    # BMP180
    # Pressure
    btemp = bmp.readTemperature()
    pressure = round(bmp.readPressure(), 2)
    altitude = bmp.readAltitude()
    print "BMP 180 Temp:  %.2f C" % btemp
    print "Pressure:      %.f pa" % pressure
    print "Altitude:      %.2f m" % altitude

    # TLS2561
    # Light level
    tslight = round(tsl.readLux(), 2)
    print "Light Level:   " + str(tslight) + " lux"

    # Air Quality 0
    air0volts = round(adc.readADCSingleEnded(0, gain, sps) / 1000, 3)
    print "Air Quality 0:", air0volts, "volts"

#    # Air Quality 3
#    air3volts = round(adc.readADCSingleEnded(3, gain, sps) /1000, 3)
#    print "Air Quality 3:", air3volts, "volts"

#    # Air Quality CO2 PPM Conversion
#    # Get resistance from voltage
#    ohm = (-1000*(air0volts-5))/air0volts
#    #ppm = 116.6020682*(np.power((ohm/41763), -2.769034857)

#    # Get ppm from resistance (3 step process)
#    ohmp1 = ohm/41763
#    ohmp2 = np.power(ohmp1, -2.769034857)
#    ppm = 116.6020682 * ohmp2
#    print ppm

#    # Get percent co2 from ppm
#    # and round to 3 decimal places
#    perco2 = np.around(ppm/10000, 3)
#    print perco2


    # Open a csv file in append mode and write the data
#    myfile = open('log_airqtest.csv', 'a')
#    myfile.write(strftime("%m-%d-%y %H:%M"))  # time
#    myfile.write(",")
#    myfile.write(str(stemp))
#    myfile.write(",")
#    myfile.write(str(shumid))
#    myfile.write(",")
#    myfile.write(str(btemp))
#    myfile.write(",")
#    myfile.write(str(pressure))
#    myfile.write(",")
#    myfile.write(str(tslight))
#    myfile.write(",")
#    myfile.write(str(air0volts))
#    myfile.write(",")
#    myfile.write(str(air3volts))
#    myfile.write("\n")
#    myfile.close()

