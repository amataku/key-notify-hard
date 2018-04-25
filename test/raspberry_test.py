import RPi.GPIO as GPIO
import time
import urllib

CHANNEL = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(CHANNEL,GPIO.IN)

before = 3

while True:
    input = GPIO.input(CHANNEL)
    if input != before:
        if input == 0:
            print "on!"
            before = input
        else:
            print "off!"
            before = input

GPIO.cleanup()
