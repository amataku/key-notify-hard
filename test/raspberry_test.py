import RPi.GPIO as GPIO
import time
import requests

CHANNEL_1 = 18
CHANNEL_2 = 17
DELAYTIME = 50

GPIO.setmode(GPIO.BCM)
GPIO.setup(CHANNEL_1,GPIO.IN)
GPIO.setup(CHANNEL_2,GPIO.IN)

before_1 = 3
before_2 = 3
delay = 0

while True:
    input_1 = GPIO.input(CHANNEL_1)
    input_2 = GPIO.input(CHANNEL_2)
    print str(input_2)
    print str(input_1)
    if delay == 0:
        if input_2 != before_2 or input_1 != before_1:
            delay = 1
    if delay != 0:
        if input_2 == before_2 or input_1 == before_1:
            delay = delay + 1
    else:
        delay = 0
    if delay == DELAYTIME:
        if input_2 == 0 or input_1 == 0:
            url = "https://key-notify-server.herokuapp.com/api/hard/on"
            requests.post(url,data={})
            print "on!"
            delay = 0
        else:
            url = "https://key-notify-server.herokuapp.com/api/hard/off"
            requests.post(url,data={})
            print "off!"
            delay = 0
    before_1 = input_1
    before_2 = input_2
GPIO.cleanup()
