#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys

from selenium.webdriver.common.by import By

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from Utils import Operate, LogSys
from Utils.Dec import elementGPS

back_xpath = '//XCUIElementTypeButton[@name="icon back black"]'
back_xpath_2 = '//XCUIElementTypeButton[@name="icon back white"]'
back_xpath_3 = '//XCUIElementTypeButton[@name="返回"]'

@elementGPS(type=By.XPATH, value=back_xpath)
def objectBack():
    pass

@elementGPS(type=By.XPATH, value=back_xpath_2)
def objectBack2():
    pass

@elementGPS(type=By.XPATH, value=back_xpath_3)
def objectBack3():
    pass

def back_black():
    '''
    通用的返回
    :return:
    '''
    Operate.clickElement(objectBack())

def back_white():
    '''
    通用的返回
    :return:
    '''
    Operate.clickElement(objectBack2())

def back_chinese():
    '''
    通用的返回
    :return:
    '''
    Operate.clickElement(objectBack3())

def actionBack():
    if not objectBack() == None:
        back_black()
        return
    elif not objectBack2() == None:
        back_white()
        return
    elif not objectBack3() == None:
        back_chinese()
        return
    else:
        LogSys.logWarning('未匹配到返回。')
        return