#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time

from Utils import LogSys

def getTime():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())

def getTimeForLog():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def getTimeDay():
    return time.strftime("%Y%m%d", time.localtime())

def getNextDay(skip_day):
    monthBack = time.strftime("%Y%m", time.localtime())
    dayBack = time.localtime().tm_mday+skip_day
    return '{0}{1}'.format(monthBack,dayBack)

def sleep(secs):
    LogSys.logInfo('sleep {0} s'.format(secs))
    time.sleep(secs)

if __name__ == '__main__':
    sleep(4)