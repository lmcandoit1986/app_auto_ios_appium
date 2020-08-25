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

from Utils import Operate, UiObject, Support, LogSys
from Utils.Dec import elementGPS
from Page.TraderPasswordPage import TradePasswordPage

'''
工资宝产品购买页面
命名规则：
定位元素：object 开头
操作：action 开头
获取：get 开头
验证：assert 开头
'''


class BuyPage(object):
    sure_id = '确认购买'
    continue_id = '继续购买'
    loading_xpath = '//XCUIElementTypeStaticText[@name="加载中..."]'
    timeOut = 15

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

    @elementGPS(type=By.ID, value=sure_id)
    def objectSure(self):
        pass

    @elementGPS(type=By.ID, value=continue_id, isAssert=False)
    def objectContinue(self):
        pass

    def actionSetMoney(self, money):
        for item in money:
            Operate.clickElement(
                UiObject.findElementMakeSureEnabled(driver=self.driver, type=By.ID, value=item, timeout=5, instance=0))
        return self

    def actionSure(self):
        Operate.clickElement(self.objectSure())
        Operate.clickElementNoBreak(self.objectContinue())
        return TradePasswordPage(self.driver)
