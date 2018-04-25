import RPi.GPIO as GPIO
import time
import urllib

CHANNEL = 18
DELAYTIME = 50000

GPIO.setmode(GPIO.BCM)
GPIO.setup(CHANNEL,GPIO.IN)

before = 3
delay = 0

while True:
    input = GPIO.input(CHANNEL)
    if delay == 0:
        if input != before:
            delay = 1
    if delay != 0:
        if input == before:
            delay = delay + 1
    if delay == DELAYTIME:
        if input == 0:
            print "on!"
            delay = 0
        else:
            print "off!"
            delay = 0
    before = input
GPIO.cleanup()
