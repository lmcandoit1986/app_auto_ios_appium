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
from Page.Login.LoginMainPage import LoginMainPage

'''
未登录，App启动后页面
命名规则：
定位元素：object 开头
操作：action 开头
获取：get 开头
验证：assert 开头
'''

class LoginSelectorPage(object):

    login_id = '登录'
    register_id = '注册'

    def __init__(self, driver):
        self.driver = driver

    @elementGPS(type=By.ID, value=login_id)
    def objectLogin(self):
        pass

    @elementGPS(type=By.ID, value=register_id)
    def objectRegister(self):
        pass

    def actionLogin(self):
        Operate.clickElement(self.objectLogin())
        return LoginMainPage(self.driver)

    def actionRegister(self):
        Operate.clickElement(self.objectRegister())
        return self
