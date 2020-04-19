#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from Utils import Operate, Asserts, Support, UiObject
from Utils.Dec import elementDecorator, elementV2Decorator
from Page.BeforPage import BeforePage

'''
主页面
命名规则：
定位元素：object 开头
操作：action 开头
获取：get 开头
验证：assert 开头
'''

class MainPage(object):

    def __init__(self, driver):
        self.driver = driver

    @elementV2Decorator(By.ID, "理财")
    def _objectBack(self):
        pass

    @elementDecorator(By.ID, "cmbc close")
    def _objectClose(self):
        pass

    @elementDecorator(By.ID, "id_tile")
    def _objectTitle(self):
        pass

    def actionBack(self):
        # print(self.driver.page_source)
        Operate.clickByObjectPoint(self.driver, self._objectBack())
        return BeforePage(self.driver)

    def getTitle(self):
        return Operate.getText(self._objectTitle())

    def assertTitle(self):
        Asserts.assertTrueNoPic(False, "reason")



