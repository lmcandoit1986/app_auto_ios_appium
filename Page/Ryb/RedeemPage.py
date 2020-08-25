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

from Utils import Operate, UiObject, LogSys, Support
from Utils.Dec import elementGPS
from Page.TraderPasswordPage import TradePasswordPage

'''
工资宝产品赎回页面
命名规则：
定位元素：object 开头
操作：action 开头
获取：get 开头
验证：assert 开头
'''


class RedeemPage(object):

    loading_xpath = '//XCUIElementTypeStaticText[@name="加载中..."]'
    input = "name BEGINSWITH  '可赎回'"
    sure_id = '确认赎回'
    close_keybord_id = '确定'
    timeOut = 30

    def __init__(self, driver):
        self.driver = driver
        '''
        判断是否loading完成
        '''
        time_end = time.time() + self.timeOut
        while True:
            if not isinstance(self.objectLoading(), WebElement):
                Support.sleep(0.5)
                return
            if time.time() >= time_end:
                LogSys.logWarning('预期时间 {} 秒内，未加载完成'.format(self.timeOut))
                return
            Support.sleep(0.5)


    @elementGPS(type=By.XPATH, value=loading_xpath, timeout=2, isAssert=False)
    def objectLoading(self):
        pass

    @elementGPS(value=input, timeout=10)
    def objectInput(self):
        pass

    @elementGPS(type=By.ID, value=close_keybord_id)
    def objectCloseKeybord(self):
        pass

    @elementGPS(type=By.ID, value=sure_id)
    def objectSure(self):
        pass


    def actionSetMoney(self, money):
        Operate.clickElement(self.objectInput())
        for item in money:
            Operate.clickElement(UiObject.find(driver=self.driver, type=By.ID, value=item))
        return self

    def actionSure(self):
        Operate.clickElement(self.objectCloseKeybord())
        Operate.clickElement(self.objectSure())
        return TradePasswordPage(self.driver)