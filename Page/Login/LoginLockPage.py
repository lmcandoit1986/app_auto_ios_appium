#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from Utils import Operate, Support, LogSys
from Utils.Dec import elementGPS
from Page.Main.HomePage import HomePage

'''
图案密码页面，设置或解锁
命名规则：
定位元素：object 开头
操作：action 开头
获取：get 开头
验证：assert 开头
'''

class LoginLockPage(object):

    set_pattern_lock_id = '请绘制手势密码'
    unlock_id = '使用密码登录'
    pattern_tap_1_xpath = '//XCUIElementTypeApplication[@name="华能成长宝"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]'
    pattern_tap_2_xpath = '//XCUIElementTypeApplication[@name="华能成长宝"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]'
    pattern_tap_3_xpath = '//XCUIElementTypeApplication[@name="华能成长宝"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[4]'

    def __init__(self, driver):
        self.driver = driver

    @elementGPS(type=By.ID, value=set_pattern_lock_id)
    def objectSetPatternLockTag(self):
        pass

    @elementGPS(type=By.ID, value=unlock_id)
    def objectUnlockTag(self):
        pass

    @elementGPS(type=By.XPATH, value=pattern_tap_1_xpath)
    def objectPatternPoint_1(self):
        pass

    @elementGPS(type=By.XPATH, value=pattern_tap_2_xpath)
    def objectPatternPoint_2(self):
        pass

    @elementGPS(type=By.XPATH, value=pattern_tap_3_xpath)
    def objectPatternPoint_3(self):
        pass

    def actionUsePhoneAndPsw(self):
        from Page.Login.LoginMainPage import LoginMainPage
        Operate.clickElement(self.objectUnlockTag())
        return LoginMainPage(self.driver)

    def actionUnlock(self):
        tap1_rect = self.objectPatternPoint_1().rect
        tap2_rect = self.objectPatternPoint_2().rect
        tap3_rect = self.objectPatternPoint_3().rect
        # 106.5 293.5 100 100
        x = tap1_rect.get('x') + tap1_rect.get('width') / 2
        y = tap1_rect.get('y') + tap1_rect.get('height') / 2
        x_x = tap2_rect.get('x') - tap1_rect.get('x')
        y_y = tap3_rect.get('y') - tap1_rect.get('y')

        points = []
        points.append({'x': x, 'y': y})
        for i in range(2):
            # 向右滑动
            points.append({'x': points[-1]['x'] + x_x, 'y': points[-1]['y']})

        for i in range(2):
            # 向下滑动
            points.append({'x': points[-1]['x'], 'y': points[-1]['y'] + y_y})

        for i in range(0):
            # 向左滑动
            points.append({'x': points[-1]['x'] - x_x, 'y': points[-1]['y']})

        for i in range(0):
            # 向上滑动
            points.append({'x': points[-1]['x'], 'y': points[-1]['y'] - y_y})

        '''
        暂不支持斜向滑动
        '''
        LogSys.logInfo(points)
        touchAction = TouchAction(self.driver)
        touchAction.press(None, points[0]['x'], points[0]['y']).wait(300) \
            .move_to(None, points[1]['x'], points[1]['y']).wait(300) \
            .move_to(None, points[2]['x'], points[2]['y']).wait(300) \
            .move_to(None, points[3]['x'], points[3]['y']).wait(300) \
            .move_to(None, points[4]['x'], points[4]['y']).wait(300) \
            .release().perform()
        return HomePage(self.driver)

    def actioSetLock(self):
        tap1_rect = self.objectPatternPoint_1().rect
        tap2_rect = self.objectPatternPoint_2().rect
        tap3_rect = self.objectPatternPoint_3().rect
        # 106.5 293.5 100 100
        x = tap1_rect.get('x') + tap1_rect.get('width') / 2
        y = tap1_rect.get('y') + tap1_rect.get('height') / 2
        x_x = tap2_rect.get('x') - tap1_rect.get('x')
        y_y = tap3_rect.get('y') - tap1_rect.get('y')

        points = []
        points.append({'x': x, 'y': y})
        for i in range(2):
            # 向右滑动
            points.append({'x': points[-1]['x'] + x_x, 'y': points[-1]['y']})

        for i in range(2):
            # 向下滑动
            points.append({'x': points[-1]['x'], 'y': points[-1]['y'] + y_y})

        for i in range(0):
            # 向左滑动
            points.append({'x': points[-1]['x'] - x_x, 'y': points[-1]['y']})

        for i in range(0):
            # 向上滑动
            points.append({'x': points[-1]['x'], 'y': points[-1]['y'] - y_y})

        '''
        暂不支持斜向滑动
        '''
        LogSys.logInfo(points)
        touchAction = TouchAction(self.driver)
        touchAction.press(None, points[0]['x'], points[0]['y']).wait(300) \
            .move_to(None, points[1]['x'], points[1]['y']).wait(300) \
            .move_to(None, points[2]['x'], points[2]['y']).wait(300) \
            .move_to(None, points[3]['x'], points[3]['y']).wait(300) \
            .move_to(None, points[4]['x'], points[4]['y']).wait(300) \
            .release().perform()
        Support.sleep(2)
        touchAction.press(None, points[0]['x'], points[0]['y']).wait(300) \
            .move_to(None, points[1]['x'], points[1]['y']).wait(300) \
            .move_to(None, points[2]['x'], points[2]['y']).wait(300) \
            .move_to(None, points[3]['x'], points[3]['y']).wait(300) \
            .move_to(None, points[4]['x'], points[4]['y']).wait(300) \
            .release().perform()
        return HomePage(self.driver)
