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


from Utils import Operate, Support, LogSys
from Utils.Dec import elementGPS

'''
工资宝产品详情页面
命名规则：
定位元素：object 开头
操作：action 开头
获取：get 开头
验证：assert 开头
'''

class ProductPage(object):

    title_xpath = '//XCUIElementTypeNavigationBar[@name="工资宝"]'
    buy_xpath = '//XCUIElementTypeButton[@name="购买"]'
    redeem_xpath = '//XCUIElementTypeStaticText[@name="赎回"]'
    loading_xpath = '//XCUIElementTypeStaticText[@name="加载中..."]'
    transaction_records_xpath = '//XCUIElementTypeStaticText[@name="交易记录"]'
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


    @elementGPS(type=By.XPATH, value=title_xpath)
    def objectTitle(self):
        pass

    @elementGPS(type=By.XPATH, value=buy_xpath)
    def objectBuy(self):
        pass

    @elementGPS(type=By.XPATH, value=redeem_xpath)
    def objectRedeem(self):
        pass

    @elementGPS(type=By.XPATH, value=transaction_records_xpath)
    def objectRecords(self):
        pass

    @elementGPS(type=By.XPATH, value=loading_xpath, timeout=2, isAssert=False)
    def objectLoading(self):
        pass


    def actionBuy(self):
        from Page.Ryb.BuyPage import BuyPage
        Operate.clickElement(self.objectBuy())
        return BuyPage(self.driver)

    def actionRedeem(self):
        from Page.Ryb.RedeemPage import RedeemPage
        Operate.clickElement(self.objectRedeem())
        return RedeemPage(self.driver)

    def actionRecords(self):
        Operate.clickElement(self.objectRecords())