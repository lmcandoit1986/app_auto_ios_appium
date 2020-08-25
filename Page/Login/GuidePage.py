#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from selenium.webdriver.common.by import By

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from Utils import Operate
from Utils.Dec import elementGPS
from Page.Login.AssertLoginPage import AssertLoginPage

'''
闪屏页面
命名规则：
定位元素：object 开头
操作：action 开头
获取：get 开头
验证：assert 开头
'''

class GuidePage(object):

    skip_xpath = '//XCUIElementTypeApplication[@name="华能成长宝"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeButton'

    def __init__(self, driver):
        self.driver = driver

    @elementGPS(type=By.XPATH, value=skip_xpath)
    def objectSkip(self):
        pass

    def actionSkip(self):
        Operate.clickElementNoBreak(self.objectSkip())
        return AssertLoginPage(self.driver)