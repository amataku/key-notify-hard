import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

for x in xrange(5):
	GPIO.output(18,True)
	time.sleep(2)
	GPIO.output(18,False)
	time.sleep(2)
GPIO.cleanup()
