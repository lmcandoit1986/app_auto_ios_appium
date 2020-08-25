#!/usr/bin/python3
# -*- coding: utf-8 -*-

from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import ElementNotVisibleException

from Config import Config
from Utils import Support, LogSys, Asserts


def swipes(direction, num):
    LogSys.logInfo('drag to {0} loop:{1}'.format(direction, num))
    if direction == 'up':
        for i in range(num):
            Config.driver.swipe(Config.width / 2, Config.Height / 5 * 3, Config.width / 2,
                                Config.Height / 5 * 2, 400)
            Support.sleep(1.5)
    elif direction == 'down':
        for i in range(num):
            Config.driver.swipe(Config.width / 2, Config.Height / 5 * 2, Config.width / 2,
                                Config.Height / 5 * 3, 400)
            Support.sleep(1.5)
    elif direction == 'left':
        for i in range(num):
            Config.driver.swipe(Config.width / 5 * 3 * 2, Config.Height / 2, Config.width / 5 * 2,
                                Config.Height / 2, 400)
            Support.sleep(1.5)
    elif direction == 'right':
        for i in range(num):
            Config.driver.swipe(Config.width / 5 * 2, Config.Height / 2, Config.width / 5 * 3,
                                Config.Height / 2, 400)
            Support.sleep(1.5)
    else:
        LogSys.logWarning('Key Error with {0}'.format(direction))


def scroll(direction, num):
    '''
    down,up,left,right
    :param TO:
    :return:
    '''
    LogSys.logInfo('scroll from {0} loop {1}'.format(direction, num))
    for i in range(num):
        Config.driver.execute_script('mobile: scroll', {'direction': direction})


def clickPointFromElement(driver, element):
    Asserts.assertTrue(element is not None, '对象定位异常，未定位到信息', Support.getTime())
    mid_x = element.rect.get('x') + element.rect.get('width') / 2
    mid_y = element.rect.get('y') + element.rect.get('height') / 2
    LogSys.logInfo('click element use point {0},{1}'.format(mid_x, mid_y))
    driver.tap([(mid_x, mid_y), (mid_x, mid_y)], 500)


def clickPoint(driver, point_x, point_y):
    LogSys.logInfo('click element use point {0},{1}'.format(point_x, point_y))
    driver.tap([(point_x, point_y), (point_x, point_y)], 500)


def clickElement(element):
    LogSys.logInfo(type(element))
    Asserts.assertTrue(element is not None, '对象定位异常，未定位到信息', Support.getTime())
    LogSys.logInfo('click element')
    try:
        element.click()
    except ElementNotVisibleException:
        Asserts.assertTrueNoPic(False,
                                'ElementNotVisibleException: Message: The element is not visible on the screen and thus is not interactable')


def clickElementNoBreak(element):
    '''
    失败不中断用例执行
    :param element:
    :return:
    '''
    if element is not None:
        LogSys.logInfo('click element')
        element.click()
    else:
        LogSys.logInfo('对象定位异常，未定位到信息')


def clickPointFromElementNoBreak(driver, element):
    '''
    失败不中断用例执行
    :param element:
    :return:
    '''
    if element is not None:
        Mid_x = element.rect.get('x') + element.rect.get('width') / 2
        Mix_y = element.rect.get('y') + element.rect.get('height') / 2
        LogSys.logInfo('click element use point {0},{1}'.format(Mid_x, Mix_y))
        driver.tap([(Mid_x, Mix_y), (Mid_x, Mix_y)], 500)
    else:
        LogSys.logInfo('对象定位异常，未定位到信息')


def getTextFromElement(element):
    if element is None:
        return None
    return element.text()


def input(editElement, inputWords):
    Asserts.assertTrue(editElement is not None, '对象定位异常，未定位到信息', Support.getTime())
    editElement.clear()
    editElement.send_keys(inputWords)


def draw(points, driver):
    '''
    绘制图案
    :param points:绘制图案用到的坐标点集合，格式[{'x':1,'y':2},{'x':1,'y':2}]
    :param driver:
    :return:
    '''
    touchAction = TouchAction(driver=driver)
    if len(points) > 0:
        touchAction.pressItem(None, points[0]['x'], points[0]['y']).sleep()
        for point in points[1:]:
            touchAction.move_to(None, point['x'], point['y'])
        touchAction.release().perform()


def clickUseTouch(driver, element):
    x_pos = element.rect.get('x') + element.rect.get('width') / 2
    y_pos = element.rect.get('y') + element.rect.get('height') / 2
    TouchAction(driver).tap(x=x_pos, y=y_pos).perform()
