#!/bin/sh
git -C /home/pi/key-notify-hard pull origin master

# search process 'key_notify'
_pcnt=`pgrep -fo key_notify | wc -l`

# if first process => start system
if [ ${_pcnt} -eq 0 ]; then
    python /home/pi/key-notify-hard/notify.py &
    exit 1
fi
