#!/bin/bash

source /etc/environment
source ~/.bashrc

touch /usr/app/logs/cron.log

/usr/local/bin/python /usr/app/src/main.py >> /usr/app/logs/cron.log 2>&1
