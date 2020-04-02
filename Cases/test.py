#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Base.BaseCase import BaseCase
from Config import Config
from Page.MainPage import MainPage
from Utils.Dec import CaseInfo

# python3 -m unittest Cases/test.py

class testss(BaseCase):

    @CaseInfo
    def test_model_CaseName1(self):
        Config.title = '这是一个测试用例'
        MainPage(self.driver).actionBack().actionTabMen().actionTabChild()

    @CaseInfo
    def test_model_CaseName2(self):
        Config.title = '这是一个测试用例'
        MainPage(self.driver).actionBack().actionTabMen().actionTabChild()
