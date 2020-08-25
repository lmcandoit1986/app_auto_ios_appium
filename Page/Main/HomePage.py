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

'''
首页
命名规则：
定位元素：object 开头
操作：action 开头
获取：get 开头
验证：assert 开头
'''

class HomePage(object):

    banner_xpath = '//XCUIElementTypeApplication[@name="华能成长宝"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeScrollView/XCUIElementTypeImage'
    banner_class = 'XCUIElementTypeImage'
    ryb_id = '工资宝'
    fund_id = '余额盈'
    fip_id = '理财'
    bank_id = '银行+'
    goods_id = '好物'
    hotel_id = '酒店'
    public_id = '公益'

    def __init__(self, driver):
        self.driver = driver

    @elementGPS(type=By.ID, value=ryb_id, timeout=30)
    def objectRyb(self):
        pass

    @elementGPS(type=By.ID, value=fund_id)
    def objectFund(self):
        pass

    @elementGPS(type=By.ID, value=fip_id)
    def objectFip(self):
        pass

    @elementGPS(type=By.ID, value=bank_id)
    def objectBank(self):
        pass

    @elementGPS(type=By.ID, value=goods_id)
    def objectGoods(self):
        pass

    @elementGPS(type=By.ID, value=hotel_id)
    def objectHotel(self):
        pass

    @elementGPS(type=By.ID, value=public_id)
    def objectPublic(self):
        pass

    @elementGPS(type=By.ID, value=fund_id)
    def objectFund(self):
        pass

    @elementGPS(type=By.XPATH, value=banner_xpath)
    def objectBanner(self):
        pass

    def actionBanner(self):
        Operate.clickElement(self.objectBanner())
        return self

    def actionRyb(self):
        from Page.Ryb.ProductPage import ProductPage
        Operate.clickElement(self.objectRyb())
        return ProductPage(self.driver)