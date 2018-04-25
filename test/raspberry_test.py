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
        print "cahnge"
        before = input

GPIO.cleanup()
