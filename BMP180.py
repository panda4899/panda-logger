#!/usr/bin/env python

import MySQLdb
import time
import argparse
import sys
import json
import Adafruit_BMP.BMP085 as BMP085

from subprocess import call

db = MySQLdb.connect("localhost", "root", "panda", "1906630_ece4899")
curs=db.cursor()
 
CurrTime = time.strftime("%m/%d/%y %H:%M:%S") 


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
                temp = "%0.2f" % sensor.read_temperature()
				#myTemp = "%0.2f" % (temp)
                pres = "%0.2f" % sensor.read_pressure()
                alt = sensor.read_altitude()
                slpres = sensor.read_sealevel_pressure()			
                if senml:
                    print json.dumps({"bn": basename, "bt": ts, "e": [
                        {"n": "temperature", "v": temp, "u": "degC"},
                        {"n": "pressure", "v": pres, "u": "Pa"},
                        {"n": "altitude", "v": alt, "u": "m"},
                        {"n": "sealevel_pressure", "v": slpres, "u": "Pa"},
                        ]})
                else:
				    
					#print CurrTime + temp
                    #print "%0.2f %0.2f %0.2f %0.2f" % (temp, pres, alt, slpres) 
					#call(["sudo", "cp", "test2.txt", "/var/www/html/test2.txt"])										
					#print (time.strftime("%m/%d/%y %H:%M:%S")) + "," + "%0.2f" % (temp)									
					#with open("/var/www/html/python/test2.txt", "a") as myfile:
					#	myfile.write((time.strftime("%m/%d/%y %H:%M:%S")) + "," + "%0.2f" % (temp) + "\n")
					try:						
						curs.execute ("""INSERT INTO bmp180 ( category,D1 ) VALUES(%s, %s)""",(time.strftime("%m/%d/%y %H:%M:%S"), temp) )
						curs.execute ("""INSERT INTO pressure ( category,D1 ) VALUES(%s, %s)""",(time.strftime("%m/%d/%y %H:%M:%S"), pres) )
						db.commit()
						print "Data committed"		
					except:
						print "Error: the database is being rolled back"
						db.rollback()
						
            sys.stdout.flush()
        except:
            pass
        time.sleep(freq)

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
    freq = args.freq / 8.3  #print every 2 minutes

    if args.json and args.basename is None:
        print "basename must be provided if JSON is enabled"
        sys.exit(1)

    sensor = setup()
    read(args.basename, sensor, freq, args.sensor, args.json)