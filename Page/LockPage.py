#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import time

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from Page.MainPage import MainPage

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from Utils import Operate, Asserts, Support, LogSys
from Utils.Dec import elementDecorator
from Page.BeforPage import BeforePage

'''
图案解锁页面
命名规则：
定位元素：object 开头
操作：action 开头
获取：get 开头
验证：assert 开头
'''

class LockPage(object):

    up_shutdown_id ='icon close update' # 升级关闭按

    forget_psw_Name = '忘记手势密码' # 忘记密码

    tap_1 = '//XCUIElementTypeApplication[@name="华能成长宝"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]'

    tap_2 = '//XCUIElementTypeApplication[@name="华能成长宝"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]'

    tap_3 = '//XCUIElementTypeApplication[@name="华能成长宝"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[4]'


    def __init__(self, driver):
        self.driver = driver

    @elementDecorator(By.XPATH, tap_1)
    def _object1(self):
        pass

    @elementDecorator(By.XPATH, tap_2)
    def _object2(self):
        pass

    @elementDecorator(By.XPATH, tap_3)
    def _object3(self):
        pass

    @elementDecorator(By.ID, up_shutdown_id)
    def _objcetclose(self):
        pass

    @elementDecorator(By.NAME, forget_psw_Name)
    def _objcetforgetPSW(self):
        pass

    def actionClose(self):
        Operate.clickV2(self._objcetclose())
        return self

    def actionUnlock(self):

        end_time = time.time() + 10
        while(True):
            if self._objcetforgetPSW():
                break
            if time.time() >= end_time:
                break
            Support.sleep(0.5)

        tap1_rect = self._object1().rect
        tap2_rect = self._object2().rect
        tap3_rect = self._object3().rect
        # 106.5 293.5 100 100
        x = tap1_rect.get('x') + tap1_rect.get('width') / 2
        y = tap1_rect.get('y') + tap1_rect.get('height') / 2
        x_x = tap2_rect.get('x') - tap1_rect.get('x')
        y_y = tap3_rect.get('y') - tap1_rect.get('y')

        points =[]
        points.append({'x': x, 'y': y})
        for i in range(2):
            # 向右滑动
            points.append({'x': points[-1]['x']+x_x, 'y': points[-1]['y']})

        for i in range(2):
            # 向下滑动
            points.append({'x': points[-1]['x'], 'y': points[-1]['y']+y_y})

        for i in range(0):
            # 向左滑动
            points.append({'x': points[-1]['x']-x_x, 'y': points[-1]['y']})

        for i in range(0):
            # 向上滑动
            points.append({'x': points[-1]['x'], 'y': points[-1]['y']-y_y})

        '''
        暂不支持斜向滑动
        '''
        LogSys.logInfo(points)
        touchAction = TouchAction(self.driver)
        touchAction.press(None, points[0]['x'], points[0]['y']).wait(300)\
            .move_to(None, points[1]['x'], points[1]['y']).wait(300)\
            .move_to(None, points[2]['x'], points[2]['y']).wait(300)\
            .move_to(None, points[3]['x'], points[3]['y']).wait(300)\
            .move_to(None, points[4]['x'], points[4]['y']).wait(300)\
            .release().perform()
        return MainPage(self.driver)