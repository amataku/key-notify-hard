import RPi.GPIO as GPIO
import time
import requests
import json
import os
from setproctitle import  setproctitle
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# change process name
setproctitle("key_notify")

# set constant var
CHANNEL_1 = 18
CHANNEL_2 = 17
DELAYTIME = 3
SLEEPTIME = 2.0
URL='https://key-notify-server.herokuapp.com/api/hard'
RETRY_CODE = [ 400, 404 ]
RETRY_NUMBER = 3
FACTOR = 1
TIMEOUT = 5

# connect retry seeting
session = requests.Session()
retries = Retry(total = RETRY_NUMBER,backoff_factor = FACTOR,status_forcelist = RETRY_CODE)
session.mount('https://',HTTPAdapter(max_retries=retries))
session.mount('http://',HTTPAdapter(max_retries=retries))


# set pin input
GPIO.setmode(GPIO.BCM)
GPIO.setup(CHANNEL_1,GPIO.IN)
GPIO.setup(CHANNEL_2,GPIO.IN)

# get enviroment var
APP_ID = os.environ["KEY_NOTIFY"]

# set url parameter
payload = {'app_id': APP_ID}
headers = {'content-type': 'application/json'}

# set init
before_1 = 3
before_2 = 3
send = 3
delay = 0

while True:
    # wait time
    time.sleep(SLEEPTIME)

    # set input state
    input_1 = GPIO.input(CHANNEL_1)
    input_2 = GPIO.input(CHANNEL_2)

    # sensing input state change and sensing input state keep
    if delay == 0:
        if input_2 != before_2 or input_1 != before_1:
            delay = 1
    else:
        if input_2 == before_2 and input_1 == before_1:
            delay = delay + 1
        else:
            delay = 0

    if delay >= DELAYTIME:
        # send on request
        if input_2 == 0 or input_1 == 0:
            nowsend = 0
            if send != nowsend:
                url = URL+'/on'
                try:
                    session.post(url,data = json.dumps(payload),timeout = TIMEOUT,headers = headers)
                except:
                    print("connect error")
                finally:
                    delay = 0
                    send = 0
        # send off request
        else:
            nowsend = 1
            if send != nowsend:
                url = URL+'/off'
                try:
                    session.post(url,data = json.dumps(payload),timeout = TIMEOUT,headers = headers)
                except:
                    print("connect error")
                finally:
                    delay = 0
                    send = 1
    # set next before value
    before_1 = input_1
    before_2 = input_2

# pin input clean
GPIO.cleanup()
