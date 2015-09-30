#!/usr/bin/python

import time
import signal
import sys
from Adafruit_ADS1x15 import ADS1x15
from time import strftime


def signal_handler(signal, frame):
        #print 'You pressed Ctrl+C!'
        #print adc.getLastConversionResults()/1000.0
        adc.stopContinuousConversion()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
# Print 'Press Ctrl+C to exit'

ADS1015 = 0x00    # 12-bit ADC
ADS1115 = 0x01    # 16-bit ADC

# Select the gain
gain = 6144  # +/- 6.144V
#gain = 4096  # +/- 4.096V
#gain = 2048  # +/- 2.048V
# gain = 1024  # +/- 1.024V
# gain = 512   # +/- 0.512V
# gain = 256   # +/- 0.256V

# Select the sample rate
#sps = 8    # 8 samples per second
# sps = 16   # 16 samples per second
# sps = 32   # 32 samples per second
# sps = 64   # 64 samples per second
# sps = 128  # 128 samples per second
#sps = 250  # 250 samples per second
#sps = 475  # 475 samples per second
sps = 860  # 860 samples per second

# Initialise the ADC using the default mode (use default I2C address)
# Set this to ADS1015 or ADS1115 depending on the ADC you are using!
adc = ADS1x15(ic=ADS1115)
# ADC channel 0
#adc.startContinuousConversion(0, gain, sps)

# Initilize variables
voltavg = 0
lastvoltage = 3.3
levels = []
maxlevels = []
twominavg = 0
avgdone = 0
#maxvalue = 3.3
isloud = 0
lastmax = 3.3

while True:
    # If the average has already been recorded and the minute change
    # set avgdone back to zero
    if avgdone is 1 and int(strftime("%M")) % 2 is not 0:
        avgdone = 0

    #elif (int(strftime("%M")) % 10 is not 0):
        #voltage = round(adc.getLastConversionResults() / 1000.0, 4)
        ##print voltage, count
        #voltsum = voltsum + voltage
        #voltavg = voltsum / count
        ##print "avg", round(voltavg, 4)
        ##print int(strftime("%M")) % 10
        #count = count + 1
        #time.sleep(0.5)

    # If the current minute divided by 2 has no remainder
    # then it's 2 minutes
    # Forgive me for this
    elif (int(strftime("%M")) % 2 is 0 and avgdone is 0):
        try:
            twominavg = round(sum(maxlevels) / float(len(maxlevels)), 6)
            print "Two Minute Average:", twominavg
        except ZeroDivisionError:
            pass
#        twominavg = round(voltavg, 6)
#        print "two-Minute Average:", twominavg
#        twofile = open('sound_test2_log.csv', 'a')
#        twofile.write(strftime("%m-%d-%y %H:%M"))  # time
#        twofile.write(",")
#        twofile.write(str(twominavg))
#        twofile.write("\n")
#        twofile.close()
        levels = []
        maxlevels = []
        # avgdone is so it only records the 2 minute avgerage once
        avgdone = 1

    else:
        for x in range(0, 860):
            # Read channel 0 in single-ended mode using the settings above
            volts = adc.readADCSingleEnded(0, gain, sps) / 1000
            value = round(3.3 - volts, 6)
            levels.append(value)
        # If the sound value increases by 80% or more it is loud
            if (value > ((lastmax * 0.7) + lastmax) and isloud == 0):
                print "Loud", value
                isloud = 1
#            loudfile = open('loud_test2_log.csv', 'a')
#            loudfile.write(strftime("%m-%d-%y %H:%M"))  # time
#            loudfile.write(",")
#            loudfile.write("1")
#            loudfile.write("\n")
#            loudfile.close()
        maxvalue = max(levels)
        print maxvalue
        maxlevels.append(maxvalue)
        levels = []
        isloud = 0
        lastmax = maxvalue
        maxvalue = 0
