import RPi.GPIO as GPIO
import time
import requests

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
            url = "https://key-notify-server.herokuapp.com/api/hard/on"
            requests.post(url,data={})
            print "on!"
            delay = 0
        else:
            url = "https://key-notify-server.herokuapp.com/api/hard/off"
            requests.post(url,data={})
            print "off!"
            delay = 0
    before = input
GPIO.cleanup()
