#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time

from appium.webdriver import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from Config import Config
from Utils import LogSys, Support, Operate


def findUiObject(driver, Type, Value):
    LogSys.logInfo("定位,type:{0},value:{1}".format(Type, Value))
    objects = [(By.NAME, 'alert'), (By.NAME, 'alert')]
    try:
        return driver.find_element(Type, Value)
    except NoSuchElementException as NS:
        LogSys.logError('NoSuchElementException,type:{0},value:{1}'.format(Type, Value))
        # 后续 异常弹框的处理
        '''
        可以区分弹框类型
        1、授权类弹框，当匹配弹框后，将列表中的对象删除，减少后续匹配时间
        2、App测试弹框，匹配成功后，不对列表做处理
        '''
        for uiobject in objects:
            Target = findUiObjectResetImplicitlyWait(driver, uiobject[0], uiobject[1])
            # 处理掉弹框
            if isinstance(Target, WebElement):
                LogSys.logInfo("命中弹框，处理掉弹框后，再执行一遍findUiObject方法")
                objects.remove(uiobject)
                findUiObject(Type, Value)


def findUiObjectResetImplicitlyWait(driver, Type, Value):
    driver.implicitly_wait(1)
    try:
        target = driver.find_element(Type, Value)
        driver.implicitly_wait(Config.IMPLICITLY_WAIT)
        return target
    except NoSuchElementException as NS:
        driver.implicitly_wait(Config.IMPLICITLY_WAIT)
        LogSys.logError('NoSuchElementException,type:{0},value:{1}'.format(Type, Value))


def assertUiobjectEnabled(driver, uiobject):
    '''
    框架提供的显式等待写法，目前实际运行有问题，暂不使用
    :param uiobject:
    :return:
    '''
    if isinstance(uiobject, WebElement):
        try:
            WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located(uiobject))
            WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located(uiobject))
            WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable(uiobject))
            return True
        except TimeoutException as TE:
            LogSys.logError('TimeoutException')
            # 后续 异常弹框的处理
    else:
        LogSys.logError('NoSuchElementException')
    return False


def assertUiobjectEnabledInExpectTime(uiobject, timeOut=3):
    time_end = time.time() + timeOut
    LogSys.logWarning("uiobjrct type:{0}".format(type(uiobject)))
    while True:
        if isinstance(uiobject, WebElement):
            if uiobject.is_enabled() and uiobject.is_displayed():
                return True
            if time.time() >= time_end:
                LogSys.logWarning('在限制时间{0}秒内,未成功获取元素或元素不可点击状态/未在当前页面展示'.format(timeOut))
                return False
            Support.sleep(0.5)


def scrollSearchElement(driver, Type, Value, PageMax=15):
    i = 0
    while True:
        ob = findUiObject(driver, Type, Value)
        if assertUiobjectEnabledInExpectTime(ob, 1):
            return ob
        else:
            Operate.scroll(Config.DRAG_DOWN, 1)
            i += 1
            if i > PageMax:
                return None



