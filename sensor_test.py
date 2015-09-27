#!/usr/bin/python

# PaSS
# Panda Sensor System

# This version is for debugging and testing individual sensors

import time

import argparse
parser = argparse.ArgumentParser(description='Team PANDa Sensor Testing Program')
parser.add_argument('-s','--sleep', help='Time in-between samples', required=False, default=1)
parser.add_argument('-t','--temp', help='SHT21 Temperature sensor', required=False, action="store_true")
parser.add_argument('-a','--adc', help='ADS1115 ADC. Select a channel.', required=False)
parser.add_argument('-p','--pres', help='BMP180 Pressure Sensor', required=False, action="store_true")
parser.add_argument('-l','--light', help='TLS2651 Light Sensor', required=False, action="store_true")
args = parser.parse_args()

if args.temp:
# for sht21
# https://github.com/jaques/sht21_python
# MIT License
    try:
        from sht21 import SHT21
        while True:
            try:
                stemp = round(SHT21(1).read_temperature(), 2)
                shumid = round(SHT21(1).read_humidity(), 2)
                print "Temperature:   %s C" % stemp
                print "Humidity:      %s rh" % shumid
            except TypeError:
                print "Invalid Checksum"
            time.sleep(float(args.sleep))
    except KeyboardInterrupt:
        print " \nBye"
    except Exception as e:
        print e
        print "Something went wrong. Is the sensor plugged in?"


if args.adc:
## https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_ADS1x15
## BSD license
    try:
        from Adafruit_ADS1x15 import ADS1x15
        ADS1115 = 0x01    # 16-bit ADC
        gain = 6144  # +/- 6.144V
        sps = 475  # 475 samples per second
        adc = ADS1x15(ic=ADS1115)

        while True:
            volts = round(adc.readADCSingleEnded(int(args.adc), gain, sps) /1000, 3)
            print "ADC:", volts, "volts"
            time.sleep(float(args.sleep))
    except KeyboardInterrupt:
        print " \nBye"
    except Exception as e:
        print e
        print "Something went wrong. Is the sensor plugged in?"

if args.pres:
## for bmp180
## https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_BMP085
## BSD Liscense
    try:
        from Adafruit_BMP085 import BMP085
        bmp = BMP085(0x77)

        while True:
            btemp = bmp.readTemperature()
            pressure = round(bmp.readPressure(), 2)
            altitude = bmp.readAltitude()
            print "BMP 180 Temp:  %.2f C" % btemp
            print "Pressure:      %.f pa" % pressure
            print "Altitude:      %.2f m" % altitude
            time.sleep(float(args.sleep))
    except KeyboardInterrupt:
        print " \nBye"
    except Exception as e:
        print e
        print "Something went wrong. Is the sensor plugged in?"

if args.light:
## https://github.com/seanbechhofer/raspberrypi/blob/master/python/TSL2561.py
## No liscense
## Uses Adafruit I2C
## Modified by Paul
    try:
        from TSL2561 import TSL2561
        tsl = TSL2561()

        while True:
            tslight = round(tsl.readLux(), 2)
            print "Light Level:   " + str(tslight) + " lux"
            time.sleep(float(args.sleep))
    except KeyboardInterrupt:
        print " \nBye"
    except Exception as e:
        print e
        print "Something went wrong. Is the sensor plugged in?"
