#!/usr/bin/python3
# -*- coding: utf-8 -*-
from Config import Config
from Utils import Support, LogSys

def assertTrue(Condition,reason,Pic_Name=None):
    if not Condition:
        if Pic_Name == None:
            Pic_Name = Support.getTime()
        msg = 'ErrorMessage:{0},Pic:{1}.{2}'.format(reason, Pic_Name,'png')
        Support.screenShot('{0}{3}/{1}.{2}'.format(Config.img_path, Pic_Name, 'png', Support.getTimeDay()))
        LogSys.logInfo('INSTRUMENTATION_STATUS: result={0}'.format('Failed'))
        LogSys.logInfo('INSTRUMENTATION_STATUS: reason={0}'.format(reason))
        LogSys.logInfo('INSTRUMENTATION_STATUS: pic={1}/{0}.png'.format(Pic_Name, Support.getTimeDay()))
        raise AssertionError(msg)

def assertTrueNoPic(Condition,reason):
    if not Condition:
        msg = 'ErrorMessage:{0}。'.format(reason)
        LogSys.logInfo('INSTRUMENTATION_STATUS: result={0}'.format('Failed'))
        LogSys.logInfo('INSTRUMENTATION_STATUS: reason={0}'.format(reason))
        LogSys.logInfo('INSTRUMENTATION_STATUS: pic={0}'.format(None))
        raise AssertionError(msg)