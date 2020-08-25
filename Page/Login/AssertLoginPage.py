#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from selenium.webdriver.common.by import By

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from Utils import LogSys, UiObject
from Page.Login.LoginLockPage import LoginLockPage
from Page.Login.LoginSelectorPage import LoginSelectorPage

'''
登录统一入口，兼判断页面是否登录，登录账号是否匹配
命名规则：
定位元素：object 开头
操作：action 开头
获取：get 开头
验证：assert 开头
'''


class AssertLoginPage(object):

    def __init__(self, driver):
        self.driver = driver

    def assertPage(self, phone, passowrd):

        if not LoginLockPage(self.driver).objectUnlockTag() == None:
            '''
            登录状态
            '''
            phoneScriet = phone[0:3] + '****' + phone[7:11]
            LogSys.logInfo(phoneScriet)
            if UiObject.findElementMakeSureEnabled(driver=self.driver, type=By.ID, value=phoneScriet, timeout=3, isAssert=False):
                '''
                账号匹配，解锁
                '''
                return LoginLockPage(self.driver).actionUnlock()
            else:
                '''
                账号不匹配，重新登录
                '''
                return LoginLockPage(self.driver).actionUsePhoneAndPsw().actionInputPhone(phone).actionInputPassword(
                    passowrd).actionLogin().actioSetLock()
        elif not LoginSelectorPage(self.driver).objectRegister() == None:
            '''
            如果是未登录状态，则走登录流程
            '''
            return LoginSelectorPage(self.driver).actionLogin().actionInputPhone(phone).actionInputPassword(
                passowrd).actionLogin().actioSetLock()
