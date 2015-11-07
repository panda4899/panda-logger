#!/usr/bin/python

# This lets you choose between boards

# A B
# 0 0 main board
# 1 0 C board
# 0 1 3 board
# 1 1 4 board

# Run like
# sudo python boardselect.py 3

import RPi.GPIO as GPIO            # import RPi.GPIO module
from time import sleep             # lets us have a delay
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD
GPIO.setup(4, GPIO.OUT)           # set GPIO4 as an output (A)
GPIO.setup(17, GPIO.OUT)           # set GPIO4 as an output (B)


import argparse
parser = argparse.ArgumentParser(description='Team PANDa Board Select Program')
parser.add_argument('board', help='choose a board', choices=['m', 'c', '3', '4'])
args = parser.parse_args()

#print args.board

if args.board == "m":
        GPIO.output(4, 0)   # A 0
        GPIO.output(17, 0)  # B 0
        print "Board M Active"


if args.board == "c":
        GPIO.output(4, 1)   # A 1 
        GPIO.output(17, 0)  # B 0
        print "Board C Active"

if args.board == "3":
        GPIO.output(4, 0)   # A 0 
        GPIO.output(17, 1)  # B 1
        print "Board 3 Active"

if args.board == "4":
        GPIO.output(4, 1)   # A 1 
        GPIO.output(17, 1)  # B 1
        print "Board 4 Active"

