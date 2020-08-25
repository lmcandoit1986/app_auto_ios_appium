#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import time

from appium.webdriver import WebElement
from selenium.webdriver.common.by import By

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from Utils import Operate, Asserts, Support, LogSys, UiObject
from Utils.Dec import elementGPS

'''
交易密码验证页面（H5）
命名规则：
定位元素：object 开头
操作：action 开头
获取：get 开头
验证：assert 开头
'''


class TradePasswordPage(object):

    title_xpath = '//XCUIElementTypeNavigationBar[@name="结果详情"]'

    def __init__(self, driver):
        self.driver = driver

    @elementGPS(type=By.XPATH, value=title_xpath, timeout=30)
    def objectTitle(self):
        pass

    def actionPassword(self, password):
        for item in password:
            Operate.clickElement(UiObject.finds(driver=self.driver, type=By.ID, value=item, isAssert=True, timeout=1)[-1])
        return self

    def assertTitle(self):
        self.objectTitle()
        return self
