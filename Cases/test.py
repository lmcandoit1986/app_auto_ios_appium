#!/usr/bin/python3
# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By

from Base.BaseCase import BaseCase
from Config import Config
from Page.LockPage import LockPage
from Page.MainPage import MainPage
from Utils import UiObject, LogSys
from Utils.Dec import CaseRun, CaseDesc


# python3 -m unittest Cases/test.py

class testss(BaseCase):

    @CaseDesc('这是一个测试用例')
    @CaseRun
    def test_model_CaseName1(self):
        LockPage(self.driver).actionClose().actionUnlock().actionBack()
        LogSys.logInfo('this is case')
