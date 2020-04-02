#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time

from appium.webdriver import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from Config import Config
from Utils import LogSys, Support, Operate, Alert


def findUiObject(driver, Type, Value):
    '''
    定位元素的基础方法，当元素不可见时，去匹配异常处理
    :param driver:
    :param Type:
    :param Value:
    :return:
    '''
    LogSys.logInfo("定位,type:{0},value:{1}".format(Type, Value))
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
        for uiobject in Config.permission:
            LogSys.logWarning('尝试开始定位，Type:{0},Value:{1}'.format(uiobject['Type'], uiobject['Value']))
            Target = findUiObjectResetImplicitlyWait(driver, uiobject['Type'], uiobject['Value'])
            # 处理掉弹框
            if isinstance(Target, WebElement):
                LogSys.logInfo("命中弹框，处理掉弹框后，再执行一遍findUiObject方法")
                Alert.alertAccept()
                Config.permission.remove(uiobject)
                LogSys.logWarning(Config.permission)
                findUiObject(driver, Type, Value)
        for uiobject in Config.app:
            LogSys.logWarning('尝试开始定位，Type:{0},Value:{1}'.format(uiobject['Type'],uiobject['Value']))
            Target = findUiObjectResetImplicitlyWait(driver, uiobject['Type'], uiobject['Value'])
            # 处理掉弹框
            if isinstance(Target, WebElement):
                LogSys.logInfo("命中弹框，处理掉弹框后，再执行一遍findUiObject方法")
                Operate.clickV2(Target)
                findUiObject(driver, Type, Value)


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
    '''
    验证元素是否可见及点击
    :param uiobject:
    :param timeOut:
    :return:
    '''
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
    '''
    滑动定位元素
    :param driver:
    :param Type:
    :param Value:
    :param PageMax:
    :return:
    '''
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

def findUiobjects(driver, Type, Value):
    return driver.find_elements(Type, Value)

def findUiobjectsWithExpection(driver, Type, Value):
    uiobjects =  driver.find_elements(Type, Value)
    if len(uiobjects) == 0:
        '''
        可以区分弹框类型
        1、授权类弹框，当匹配弹框后，将列表中的对象删除，减少后续匹配时间
        2、App测试弹框，匹配成功后，不对列表做处理
        '''
        for uiobject in Config.permission:
            LogSys.logWarning('尝试开始定位，Type:{0},Value:{1}'.format(uiobject['Type'], uiobject['Value']))
            Target = findUiObjectResetImplicitlyWait(driver, uiobject['Type'], uiobject['Value'])
            # 处理掉弹框
            if isinstance(Target, WebElement):
                LogSys.logInfo("命中弹框，处理掉弹框后，再执行一遍findUiObject方法")
                Alert.alertAccept()
                Config.permission.remove(uiobject)
                LogSys.logWarning(Config.permission)
                findUiobjectsWithExpection(driver, Type, Value)
        for uiobject in Config.app:
            LogSys.logWarning('尝试开始定位，Type:{0},Value:{1}'.format(uiobject['Type'], uiobject['Value']))
            Target = findUiObjectResetImplicitlyWait(driver, uiobject['Type'], uiobject['Value'])
            # 处理掉弹框
            if isinstance(Target, WebElement):
                LogSys.logInfo("命中弹框，处理掉弹框后，再执行一遍findUiObject方法")
                Operate.clickV2(Target)
                findUiobjectsWithExpection(driver, Type, Value)
    return uiobjects

def findUiobjectWithInstance(driver, Type, Value, Instance):
    '''
    元素有重复时使用
    :param driver:
    :param Type:
    :param Value:
    :param Instance:
    :return:
    '''
    uiobjects = findUiobjectsWithExpection(driver, Type, Value)
    LogSys.logInfo("uiobjects list len:{0}".format(len(uiobjects)))
    if len(uiobjects) >Instance:
        return uiobjects[Instance]
    LogSys.logError('instance:{0},but only {1}'.format(Instance,len(uiobjects)))
    return None




