#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from selenium.webdriver.common.by import By

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from Utils import Operate
from Utils.Dec import elementDecorator

class BeforePage(object):

    def __init__(self, driver):
        self.driver = driver

    @elementDecorator(By.NAME, "成人")
    def objectMen(self):
        pass

    @elementDecorator(By.NAME, "儿童")
    def objectChild(self):
        pass

    def actionTabMen(self):
        Operate.click(self.objectMen())
        return self

    def actionTabChild(self):
        Operate.click(self.objectChild())
        return self