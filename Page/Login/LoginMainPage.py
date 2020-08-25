#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from selenium.webdriver.common.by import By

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from Utils import Operate, SqlObj
from Utils.Dec import elementGPS
from Page.Login.LoginLockPage import LoginLockPage
from Config import Config

'''
登录-输入账号密码页面
命名规则：
定位元素：object 开头
操作：action 开头
获取：get 开头
验证：assert 开头
'''

class LoginMainPage(object):

    phone_class = 'XCUIElementTypeTextField'
    password_class = 'XCUIElementTypeSecureTextField'
    login_id = '登录'
    unable_login_id = '无法登录'

    def __init__(self, driver):
        self.driver = driver

    @elementGPS(type=By.CLASS_NAME, value=phone_class)
    def objectPhoneEdit(self):
        pass

    @elementGPS(type=By.CLASS_NAME, value=password_class)
    def objectPasswordEdit(self):
        pass

    @elementGPS(type=By.ID, value=login_id)
    def objectLogin(self):
        pass

    @elementGPS(type=By.ID, value=unable_login_id)
    def objectUnableLogin(self):
        pass

    def actionInputPhone(self, phone):
        if Config.NEV == 'test':
            SqlObj.delLoginLog(phone)
        Operate.input(self.objectPhoneEdit(), phone)
        return self

    def actionInputPassword(self, password):
        Operate.input(self.objectPasswordEdit(), password)
        return self

    def actionLogin(self):
        Operate.clickElement(self.objectLogin())
        return LoginLockPage(self.driver)

    def actionUnableLogin(self):
        Operate.clickElement(self.objectUnableLogin())