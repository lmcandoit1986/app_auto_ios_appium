#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from Utils import Operate, Asserts, Support
from Utils.Dec import elementDecorator
from Page.BeforPage import BeforePage

'''
主页面
命名规则：
定位元素：object 开头
操作：action 开头
获取：get 开头
验证：assert 开头
'''

class MainPage:

    tap_1 = '//XCUIElementTypeApplication[@name="华能成长宝"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]'
    tap_2 = '//XCUIElementTypeApplication[@name="华能成长宝"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]'
    tap_3 = '//XCUIElementTypeApplication[@name="华能成长宝"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[4]'

    def __init__(self, driver):
        self.driver = driver

    @elementDecorator(By.NAME, "保险")
    def _objectBack(self):
        pass

    @elementDecorator(By.XPATH, tap_1)
    def _object1(self):
        pass

    @elementDecorator(By.XPATH, tap_2)
    def _object2(self):
        pass

    @elementDecorator(By.XPATH, tap_3)
    def _object3(self):
        pass

    @elementDecorator(By.ID, "id_tile")
    def _objectTitle(self):
        pass

    def actionBack(self):
        Operate.click(self._objectBack())
        return BeforePage(self.driver)

    def getTitle(self):
        return Operate.getText(self._objectTitle())

    def assertTitle(self):
        Asserts.assertTrueNoPic(False, "reason")

    def actionUnlock(self):
        tap1_rect = self._object1().rect
        tap2_rect = self._object2().rect
        tap3_rect = self._object3().rect
        x = tap1_rect.get('x')+tap1_rect.get('width')/2
        y = tap1_rect.get('y')+tap1_rect.get('height')/2
        tox = tap2_rect.get('x')-tap1_rect.get('x')
        toy = tap3_rect.get('y')-tap1_rect.get('y')
        TouchAction(driver=self.driver).press(None, x, y).wait(300)\
            .move_to(None, x+tox, y).wait(300)\
            .move_to(None, x+tox+tox, y).wait(300)\
            .move_to(None, x+tox+tox, y+toy).wait(300)\
            .move_to(None, x+tox+tox, y+toy+toy)\
            .release().perform()
        Support.sleep(10)
        return self

