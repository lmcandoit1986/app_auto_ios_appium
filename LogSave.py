#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

import sys
import os
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText
from subprocess import Popen, PIPE, STDOUT
import requests
from urllib3.exceptions import MaxRetryError

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from Utils import Support

class logSys(object):
    def startscreenrecord(self):
        self.ProcessVedio = Popen('/Users/liming/Library/Android/sdk/platform-tools/adb -s B2NGAC6850506946 logcat -s qatest > /Users/liming/Desktop/Auto/Android/log_B2NGAC6850506946_{}.log'.format(Support.getNextDay(0)), stdout=PIPE, stderr=STDOUT, shell=True)
    def closescreenrecord(self):
        self.ProcessVedio.kill()

if __name__ == '__main__':
    logSysObject = logSys()
    logSysObject.startscreenrecord()
    print(int(time.strftime("%H%M%S", time.localtime())))
    if int(time.strftime("%H%M%S", time.localtime())) > 215000:
        print('pass')
        logSysObject.closescreenrecord()
        Support.sleep(60)
