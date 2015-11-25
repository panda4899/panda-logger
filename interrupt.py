#!/usr/bin/python

from Adafruit_MCP230xx import Adafruit_MCP230XX
import time
import filecmp
import smtplib
import os
from time import strftime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import socket

# setup mcp
mcp = Adafruit_MCP230XX(address = 0x20, num_gpios = 8) # MCP23008

# Set pin 1 to input with the pullup resistor enabled
mcp.config(1, mcp.INPUT)
mcp.pullup(1, 1)

while True:
    # Read input pin and display the results
    status = (mcp.input(1) >>1)
    print "Pin 1 = %d" % status

    if status == 0:
        # this is called hysteresis
        status2 = (mcp.input(1) >>1)
        time.sleep(1)
        if status2 ==0: 
            print "water!"
            ### Send email
            fromaddr = "spacedog@paulschow.com"
            toaddr = "name@example.com"
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "Water detected!"
            host = socket.gethostname()
            body = "Water detected by %s" % host
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("spacedog@paulschow.com", "passowrd")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            print "email sent"
            # we don't want to send 500 emails
            time.sleep(120)

    time.sleep(1)
