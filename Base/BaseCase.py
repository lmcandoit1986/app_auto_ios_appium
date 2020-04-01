#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import unittest
import yaml
from appium import webdriver

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from Config import Config
from Utils import LogSys, Support


class BaseCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.Device = cls.readConfig(cls)
        cls.driver = webdriver.Remote(cls.Device['Appium_server'], cls.Device['appium'][Config.devices])
        Config.driver = cls.driver
        '''
        隐式等待
        '''
        cls.driver.implicitly_wait(Config.IMPLICITLY_WAIT)
        cls._allstart = time.time()

    @classmethod
    def tearDownClass(cls):
        LogSys.logInfo('INSTRUMENTATION_STATUS: alltime={0}'.format(int(time.time() - cls._allstart)))
        cls.driver.quit()

    def setUp(self):
        if not Config.isinit == 0:
            self.driver.launch_app()
        # Support.sleep(5)
        Config.isinit += 1
        self._start = time.time()
        Config.title = None


    def tearDown(self):
        LogSys.logInfo('INSTRUMENTATION_STATUS: title={0}'.format(Config.title))
        LogSys.logInfo('INSTRUMENTATION_STATUS: time={0}'.format(int(time.time() - self._start)))
        self.driver.close_app()

    def readConfig(self):
        filePath = os.path.dirname(__file__)
        yamlPath = os.path.join(filePath, 'DevicesInfo')
        f = open(yamlPath, 'r', encoding='utf-8')
        cont = f.read()
        x = yaml.load(cont, Loader=yaml.FullLoader)
        f.close()
        return x