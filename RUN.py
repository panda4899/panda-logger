#!/usr/bin/env python

import MySQLdb
import time, signal, sys, json, argparse

from Adafruit_ADS1x15 import ADS1x15                  # ADC
import Adafruit_BMP.BMP085 as BMP085                  # Temp/Pressure
from TSL2561 import TSL2561                           # Light
from sht21 import SHT21                               # Humidity
from Adafruit_ADS1x15 import ADS1x15                  # ADC

from subprocess import call
from decimal import Decimal
from time import strftime

from interruptingcow import timeout            # interrupt

db = MySQLdb.connect("localhost", "root", "panda", "1906630_ece4899")
curs=db.cursor()  
 
def signal_handler(signal, frame):                  # interrupt handler
        adc.stopContinuousConversion()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
# Print 'Press Ctrl+C to exit'

#ADS1015 = 0x00	# 12-bit ADC  
ADS1115 = 0x01	# 16-bit ADC

# Initialise the ADC using the default mode (use default I2C address)
# Set this to ADS1015 or ADS1115 depending on the ADC you are using!
adc = ADS1x15(ic=ADS1115)

# start comparator on channel 2 with a thresholdHigh=200mV and low=100mV
# in traditional mode, non-latching, +/-1.024V and 250sps
#adc.startSingleEndedComparator(2, 200, 100, pga=1024, sps=250, activeLow=True, traditionalMode=True, latching=False, numReadings=1)
global count

# Sound Interrupt
def ADC(basename, sensor, freq, stype, senml, temp, pres, shumid, tslight, dB, CO, count):	
	try:
		with timeout(60*.01, exception=RuntimeError): #delay = 5 Min
			while True:
				test = 0
				time.sleep(.25)               # sound must last .25 seconds
				dB = adc.readADCSingleEnded(2, 6144, 475) / 10       # Sound in volts*100
				#if 150 > dB > 50:				                     # Record loud burst                       
				if dB > 50.00:                                       # Adjust for large dB     
					if dB > 150.00:
						dB = 150.00                                  # make graph easier to read
						curs.execute ("""INSERT INTO all_graphs ( category,temp, pres, shumid, adc, tslight, CO ) VALUES(%s, %s, %s, %s, %s, %s, %s)""",(time.strftime("%m/%d/%y %H:%M:%S"), "null", "null", "null", dB, "null", "null" ) )	
						db.commit()
						print "Excessive Noise"
					else:
						curs.execute ("""INSERT INTO all_graphs ( category,temp, pres, shumid, adc, tslight, CO ) VALUES(%s, %s, %s, %s, %s, %s, %s)""",(time.strftime("%m/%d/%y %H:%M:%S"), "null", "null", "null", dB, "null", "null" ) )	
						db.commit()
						print "Noise"
				if test == .01:                # delay
					break					
				test = test - 1
	except RuntimeError:		
		pass

# temp Interrupt
def Temp(basename, sensor, freq, stype, senml, temp, pres, shumid, tslight, dB, CO, count):    
	try:
		with timeout(60*.5, exception=RuntimeError): #delay = 5 Min
			while True:
				tsl = TSL2561()
				tslight = round(tsl.readLux(), 2)
				temp = "%0.2f" % ((sensor.read_temperature()*(1.8))+32)
				test = 0
				time.sleep(.25)               # sound must last .25 seconds
				dB = adc.readADCSingleEnded(2, 6144, 475) / 10       # Sound in volts*100
				#if 150 > dB > 50:				                     # Record loud burst                       
				if dB > 50.00:                                       # Adjust for large dB     
					if dB > 150.00:
						dB = 150.00                                  # make graph easier to read
						curs.execute ("""INSERT INTO all_graphs ( category,temp, pres, shumid, adc, tslight, CO ) VALUES(%s, %s, %s, %s, %s, %s, %s)""",(time.strftime("%m/%d/%y %H:%M:%S"), "null", "null", "null", dB, "null", "null" ) )	
						db.commit()
						print "Excessive Noise"
					else:
						curs.execute ("""INSERT INTO all_graphs ( category,temp, pres, shumid, adc, tslight, CO ) VALUES(%s, %s, %s, %s, %s, %s, %s)""",(time.strftime("%m/%d/%y %H:%M:%S"), "null", "null", "null", dB, "null", "null" ) )	
						db.commit()
						print "Noise"
				if test == .5:                # delay
					break				
				test = test - 1
	except RuntimeError:
		count = count + 1
	if count < 5:
		curs.execute ("""INSERT INTO all_graphs ( category, temp, pres, shumid, adc, tslight, CO ) VALUES(%s, %s, %s, %s, %s, %s, %s)""",(time.strftime("%m/%d/%y %H:%M:%S"), "null", "null", "null", "null", tslight, "null",  ) )
		curs.execute ("""INSERT INTO all_graphs ( category, temp, pres, shumid, adc, tslight, CO ) VALUES(%s, %s, %s, %s, %s, %s, %s)""",(time.strftime("%m/%d/%y %H:%M:%S"), temp, "null", "null", "null", "null", "null",  ) )		
		db.commit()
		print "Temp/Light", count		
		Light(basename, sensor, freq, stype, senml, temp, pres, shumid, tslight, dB, CO, count)			
	ADC(basename, sensor, freq, stype, senml, temp, pres, shumid, tslight, dB, CO, count)	
	pass
		
# Light Interrupt
def Light(basename, sensor, freq, stype, senml, temp, pres, shumid, tslight, dB, CO, count):        
	try:		
		with timeout(60*.5, exception=RuntimeError): #delay = 5 Min
			while True:
				tsl = TSL2561()
				tslight = round(tsl.readLux(), 2)
				test = 0
				time.sleep(.25)               # sound must last .25 seconds
				dB = adc.readADCSingleEnded(2, 6144, 475) / 10       # Sound in volts*100
				#if 150 > dB > 50:				                     # Record loud burst                       
				if dB > 50.00:                                       # Adjust for large dB     
					if dB > 150.00:
						dB = 150.00                                  # make graph easier to read
						curs.execute ("""INSERT INTO all_graphs ( category,temp, pres, shumid, adc, tslight, CO ) VALUES(%s, %s, %s, %s, %s, %s, %s)""",(time.strftime("%m/%d/%y %H:%M:%S"), "null", "null", "null", dB, "null", "null" ) )	
						db.commit()
						print "Excessive Noise"
					else:
						curs.execute ("""INSERT INTO all_graphs ( category,temp, pres, shumid, adc, tslight, CO ) VALUES(%s, %s, %s, %s, %s, %s, %s)""",(time.strftime("%m/%d/%y %H:%M:%S"), "null", "null", "null", dB, "null", "null" ) )	
						db.commit()
						print "Noise"
				if test == .5:                # delay
					break				
				test = test - 1
	except RuntimeError:
		curs.execute ("""INSERT INTO all_graphs ( category, temp, pres, shumid, adc, tslight, CO ) VALUES(%s, %s, %s, %s, %s, %s, %s)""",(time.strftime("%m/%d/%y %H:%M:%S"), "null", "null", "null", "null", tslight, "null",  ) )		
		db.commit()
		print "Light"
		Temp(basename, sensor, freq, stype, senml, temp, pres, shumid, tslight, dB, CO, count)			
		pass

		
# Rest of sensors
def read(basename, sensor, freq, stype, senml):    
    while True:
        ts = int(time.mktime(time.gmtime()))

        try:
            if stype == "temp":
                temp = sensor.read_temperature()
                if senml:
                    print json.dumps({"bt": ts, "e": [{"n": basename + "temperature", "v": temp, "u": "degC"}]})
                else:
                    print "%0.2f" % temp
            elif stype == "pres":
                pres = sensor.read_pressure()
                if senml:
                    print json.dumps({"bt": ts, "e": [{"n": basename + "pressure", "v": pres, "u": "Pa"}]})
                else:
                    print "%0.2f" % pres
            elif stype == "alt":
                alt = sensor.read_altitude()
                if senml:
                    print json.dumps({"bt": ts, "e": [{"n": basename + "altitude", "v": alt, "u": "m"}]})
                else:
                    print "%0.2f" % alt
            elif stype == "slpres":
                slpres = sensor.read_sealevel_pressure()
                if senml:
                    print json.dumps({"bt": ts, "e": [{"n": basename + "sealevel_pressure", "v": slpres, "u": "Pa"}]})
                else:
                    print "%0.2f" % slpres
            else:			    
                temp = "%0.2f" % ((sensor.read_temperature()*(1.8))+32)				
                pres = (sensor.read_pressure()/1000.000)
                tsl = TSL2561()
                shumid = round(SHT21(1).read_humidity(), 2)	
				
                if senml:
                    print json.dumps({"bn": basename, "bt": ts, "e": [
                        {"n": "temperature", "v": temp, "u": "degC"},
                        {"n": "pressure", "v": pres, "u": "Pa"},
                        {"n": "altitude", "v": alt, "u": "m"},
                        {"n": "sealevel_pressure", "v": slpres, "u": "Pa"},
                        ]})
                else:				    
					try:
						#dB = adc.readADCSingleEnded(2, 6144, 475) / 2       # Sound converted to DB
						dB = adc.readADCSingleEnded(2, 6144, 475) / 10       # Sound in volts*100 to see on graph
						CO = adc.readADCSingleEnded(3, 6144, 475) / 1000	 # VOC						
						count = 0
						tslight = round(tsl.readLux(), 2)
						#airvolts = adc.readADCSingleEnded(0, gain, sps) / 1000
						#print "Air Quality:", CO, "ppm"						
						curs.execute ("""INSERT INTO all_graphs ( category, temp, pres, shumid, adc, tslight, CO ) VALUES(%s, %s, %s, %s, %s, %s, %s)""",(time.strftime("%m/%d/%y %H:%M:%S"), temp, pres, shumid, dB, tslight, CO, ) )
						db.commit()
						print "Data committed"						
					except:
						print "Error: the database is being rolled back"
						db.rollback()
						
            sys.stdout.flush()
        except:
            pass
        time.sleep(freq)
	Light(basename, sensor, freq, stype, senml, temp, pres, shumid, tslight, dB, CO, count)  # call the sound

def setup():
    return BMP085.BMP085()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--json", help="Output in SenML", type=bool)
    parser.add_argument("-f", "--freq", help="Pulling frequency, msec", type=int)
    parser.add_argument("-s", "--sensor", help="Sensor (all if not specified): temp|pres|alt|slpres", type=str)
    parser.add_argument("-bn", "--basename", help="Sensor BaseName (URI) for SenML output", type=str)
    parser.set_defaults(freq=1000)

    args = parser.parse_args()

    if args.freq <= 0:
        print "freq should be >= 0"
        sys.exit(1)
    freq = args.freq / 1000  # Time in between timed insert and noise pause = 1sec
	
    if args.json and args.basename is None:
        print "basename must be provided if JSON is enabled"
        sys.exit(1)

    sensor = setup()
    read(args.basename, sensor, freq, args.sensor, args.json)
	
