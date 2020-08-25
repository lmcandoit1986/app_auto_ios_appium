#!/usr/bin/python3
# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By

from Base.BaseCase import BaseCase
from Page.Login.GuidePage import GuidePage
from Utils import UiObject, LogSys, Support
from Utils.Dec import CaseRun, CaseDesc


# python3 -m unittest Cases/test.py

class testss(BaseCase):

    @CaseDesc('这是一个测试用例')
    @CaseRun
    def test_model_CaseName1(self):
        # GuidePage(self.driver).actionSkip().assertPage('15011043581','111qqq').actionRyb().actionBuy().actionSetMoney('1').actionSure().actionPassword('111111').assertTitle()
        GuidePage(self.driver).actionSkip().assertPage('15011043581', '111qqq').actionRyb().actionRedeem().actionSetMoney('2').actionSure().actionPassword('111111').assertTitle()
        Support.sleep(10)
        LogSys.logInfo('this is case')
