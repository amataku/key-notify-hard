import RPi.GPIO as GPIO
import time
import requests
import json
import os
from setproctitle import  setproctitle
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from logging import Formatter, handlers, getLogger, DEBUG

# change process name
setproctitle("key_notify")

# set constant var
CHANNEL_1 = 18
CHANNEL_2 = 17
OUTPUT_CHANNEL = 24
DELAYTIME = 3
SLEEPTIME = 2.0
URL='https://key-notify-server.herokuapp.com/api/hard'
RETRY_CODE = [ 400, 404 ]
RETRY_NUMBER = 1
FACTOR = 1
TIMEOUT = 60
STATE = {
    "ON": 0,
    "OFF": 1
}

class Logger:
    def __init__(self, name = __name__):
        self.logger = getLogger(name)
        self.logger.setLevel(DEBUG)
        formatter = Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")

        #file output
        handler = handlers.RotatingFileHandler(filename = 'log.log', maxBytes = 1048576, backupCount = 3)
        handler.setLevel(DEBUG)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        def debug(self, msg):
            self.logger.debug(msg)

        def info(self, msg):
            self.logger.info(msg)

        def warn(self, msg):
            self.logger.warning(msg)

        def error(self, msg):
            self.logger.eeror(msg)

        def critical(self, msg):
            self.logger.critical(msg)

#set logger
log  = Logger('key_notify hard')

# connect retry seeting
session = requests.Session()
retries = Retry(total = RETRY_NUMBER,backoff_factor = FACTOR,status_forcelist = RETRY_CODE)
session.mount('https://',HTTPAdapter(max_retries=retries))
session.mount('http://',HTTPAdapter(max_retries=retries))


# set pin input,output
GPIO.setmode(GPIO.BCM)
GPIO.setup(CHANNEL_1,GPIO.IN)
GPIO.setup(CHANNEL_2,GPIO.IN)
GPIO.setup(OUTPUT_CHANNEL, GPIO.OUT)

# get enviroment var
APP_ID = os.environ["KEY_NOTIFY"]

# set url parameter
payload = {'app_id': APP_ID}
headers = {'content-type': 'application/json'}

# set init
before_plate_state = 3
send = 3
delay = 0

while True:
    # wait time
    time.sleep(SLEEPTIME)

    # set input state
    input_1 = GPIO.input(CHANNEL_1)
    input_2 = GPIO.input(CHANNEL_2)
    # if input_1 or input_2 is 0(ON) then state is 0(ON)
    # if input_1 and input_2 is 1(OFF) then state is 1(OFF)
    plate_state = int(bool(input_1) and bool(input_2))

    # sensing input state change and sensing input state keep
    if delay == 0:
        if plate_state != before_plate_state:
            delay = 1
    else:
        if plate_state == before_plate_state:
            delay = delay + 1
        else:
            delay = 0

    if delay >= DELAYTIME:
        # send on request
        if plate_state == STATE["ON"]:
            nowsend = STATE["ON"]
            if send != nowsend:
                url = URL+'/on'
                try:
                    req = session.post(url,data = json.dumps(payload),timeout = TIMEOUT,headers = headers)
                except:
                    log.error("connection error")
                else:
                    log.debug(req.status_code)
                finally:
                    GPIO.output(OUTPUT_CHANNEL, True)
                    delay = 0
                    send = STATE["ON"]
        # send off request
        else:
            nowsend = STATE["OFF"]
            if send != nowsend:
                url = URL+'/off'
                try:
                    req =　session.post(url,data = json.dumps(payload),timeout = TIMEOUT,headers = headers)
                except:
                    log.error("connection error")
                else:
                    log.debug(req.status_code)
                finally:
                    GPIO.output(OUTPUT_CHANNEL, False)
                    delay = 0
                    send = STATE["OFF"]
    # set next before value
    before_plate_state = plate_state

# pin input clean
GPIO.cleanup()
