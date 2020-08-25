#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time

from Utils import LogSys


def getTime():
    '''
    :return:%Y%m%d%H%M%S
    '''
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


def getTimeForLog():
    '''
    :return:%Y-%m-%d %H:%M:%S
    '''
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def getTimeDay():
    '''
    :return:%Y%m%d
    '''
    return time.strftime("%Y%m%d", time.localtime())


def getNextDay(skipDay):
    '''
    :param skip_day:
    :return:
    '''
    month = time.strftime("%Y%m", time.localtime())
    day = time.localtime().tm_mday + skipDay
    return '{0}{1}'.format(month, day)


def sleep(secs):
    '''
    单位秒
    :param secs:
    :return:
    '''
    LogSys.logInfo('sleep {0} s'.format(secs))
    time.sleep(secs)


if __name__ == '__main__':
    sleep(4)
