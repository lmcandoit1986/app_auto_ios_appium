#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time

from appium.webdriver import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from Config import Config
from Utils import LogSys, Support, Operate, Alert, Asserts

HAS_FIND_ELEMENT_ENABLED = 1
HAS_SURE_ELEMENT_UNABLED = 2
CONTINUE_WAIT_ELEMENT = 3


def find(driver, type=None, value=None, isAssert=True, timeout=0):
    LogSys.logInfo("--开始定位元素--")
    LogSys.logInfo("set type : {}".format(type))
    LogSys.logInfo("set value : {}".format(value))
    LogSys.logInfo("set isAssert : {}".format(isAssert))
    LogSys.logInfo("set timeout : {}".format(timeout))
    time_end = time.time() + timeout
    LogSys.logInfo("set begin time:{}".format(time_end - timeout))
    LogSys.logInfo("set end time:{}".format(time_end))
    # Value 不允许为空
    Asserts.assertTrueNoPic(value is not None, "传参为空")
    while True:
        # 通过 type 是否存在决定定位方法
        if type is None:
            try:
                return driver.find_element_by_ios_predicate(value)
            except NoSuchElementException:
                LogSys.logError('NoSuchElementException,value:{}'.format(value))
                if isAssert: Asserts.assertTrueNoPic(False, 'NoSuchElementException,value:{}'.format(value))
        else:
            try:
                return driver.find_element(type, value)
            except NoSuchElementException:
                LogSys.logError('NoSuchElementException,type:{},value:{}'.format(type, value))
                if isAssert: Asserts.assertTrueNoPic(False,
                                                     'NoSuchElementException,type:{},value:{}'.format(type, value))

        if time.time() >= time_end:
            LogSys.logWarning('在限制时间{0}秒内,未成功获取元素'.format(timeout))
            return None

        Support.sleep(0.1)


def finds(driver, type=None, value=None, isAssert=True, timeout=0):
    LogSys.logInfo("--开始定位元素--")
    LogSys.logInfo("set type : {}".format(type))
    LogSys.logInfo("set value : {}".format(value))
    LogSys.logInfo("set isAssert : {}".format(isAssert))
    LogSys.logInfo("set timeout : {}".format(timeout))
    time_end = time.time() + timeout
    LogSys.logInfo("set begin time:{}".format(time_end - timeout))
    LogSys.logInfo("set end time:{}".format(time_end))
    # Value 不允许为空
    Asserts.assertTrueNoPic(value is not None, "传参为空")
    while True:
        # 通过 type 是否存在决定定位方法
        if type is None:
            try:
                return driver.find_elements_by_ios_predicate(value)
            except NoSuchElementException:
                LogSys.logError('NoSuchElementException,value:{}'.format(value))
                if isAssert: Asserts.assertTrueNoPic(False, 'NoSuchElementException,value:{}'.format(value))
        else:
            try:
                return driver.find_elements(type, value)
            except NoSuchElementException:
                LogSys.logError('NoSuchElementException,type:{},value:{}'.format(type, value))
                if isAssert: Asserts.assertTrueNoPic(False,
                                                     'NoSuchElementException,type:{},value:{}'.format(type, value))

        if time.time() >= time_end:
            LogSys.logWarning('在限制时间{0}秒内,未成功获取元素'.format(timeout))
            return None

        Support.sleep(0.1)


def findElementMakeSureEnabled(driver, type=None, value=None, instance=0, timeout=10, isAssert=True):
    LogSys.logInfo("--开始尝试定位并等待元素准备完成--".format(timeout))
    time_end = time.time() + timeout
    LogSys.logInfo("set timeout:{}".format(timeout))
    LogSys.logInfo("set begin time:{}".format(time_end - timeout))
    LogSys.logInfo("set end time:{}".format(time_end))
    while True:
        if instance == 0:
            element = find(driver=driver, type=type, value=value, isAssert=False)
            res = assertEnabled(element=element, timeout=timeout, time_end=time_end, isAssert=isAssert)
            if res == HAS_FIND_ELEMENT_ENABLED:
                return element
            elif res == CONTINUE_WAIT_ELEMENT:
                return None
            checkAlert(driver=driver)
            Support.sleep(0.1)
        else:
            element = finds(driver=driver, type=type, value=value, isAssert=False)
            if len(element) < instance:
                if isAssert: Asserts.assertTrueNoPic(False, '定位元素集长度：{},传参 {} ,不符合预期'.format(len(element), instance))
                return None
            res = assertEnabled(element=element[instance], timeout=timeout, time_end=time_end, isAssert=isAssert)
            if res == HAS_FIND_ELEMENT_ENABLED:
                return element[instance]
            elif res == CONTINUE_WAIT_ELEMENT:
                return None
            checkAlert(driver=driver)
            Support.sleep(0.1)


def assertEnabled(element, timeout, time_end, isAssert):
    if isinstance(element, WebElement):
        LogSys.logInfo('assert is_enabled&is_displayed')
        if element.is_enabled() and element.is_displayed():
            return HAS_FIND_ELEMENT_ENABLED
    LogSys.logInfo("元素不可点击状态/未在当前页面展示,继续等待")
    if time.time() >= time_end:
        LogSys.logWarning('在限制时间{}秒内,未成功获取元素或元素不可点击状态/未在当前页面展示'.format(timeout))
        if isAssert: Asserts.assertTrueNoPic(False, '在限制时间{0}秒内,未成功获取元素或元素不可点击状态/未在当前页面展示'.format(timeout))
        return CONTINUE_WAIT_ELEMENT
    return HAS_SURE_ELEMENT_UNABLED


def checkAlert(driver):
    for item in Config.permission:
        Target = find(driver=driver, type=item['Type'], value=item['Value'], isAssert=False, timeout=0)
        # 处理掉弹框
        if isinstance(Target, WebElement):
            LogSys.logInfo("命中弹框，处理掉弹框后，再执行一遍findUiObject方法")
            Alert.alertAccept()
            Config.permission.remove(item)
            LogSys.logWarning(Config.permission)

    for item in Config.app:
        Target = find(driver=driver, type=item['Type'], value=item['Value'], isAssert=False, timeout=0)
        # 处理掉弹框
        if isinstance(Target, WebElement):
            LogSys.logInfo("命中弹框，处理掉弹框后，再执行一遍findUiObject方法")
            Operate.clickElementNoBreak(
                find(driver=driver, type=item['ClickType'], value=item['ClickValue'], isAssert=False))


def scrollSearchElement(driver, type, value, pageMax=15):
    '''
    滑动定位元素
    :param driver:
    :param type:
    :param value:
    :param pageMax:
    :return:
    '''
    i = 0
    while True:
        target = findElementMakeSureEnabled(driver=driver, type=type, value=value, isAssert=False, timeout=3)
        if target is not None:
            return target
        else:
            Operate.scroll(Config.DRAG_DOWN, 1)
            i += 1
            if i > pageMax:
                return None
