import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.IN)

while True:
    now = GPIO.input(18)
    if now == 0: 
        state = 1
    else:
        state = 0
    print "now input value is " + str(state)
GPIO.cleanup()
