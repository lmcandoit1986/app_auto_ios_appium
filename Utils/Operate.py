#!/usr/bin/python3
# -*- coding: utf-8 -*-
from appium.webdriver.common.touch_action import TouchAction

from Config import Config
from Utils import Support, LogSys, Asserts


def swipes(TO, Cycle):
    LogSys.logInfo('drag to {0} loop:{1}'.format(TO, Cycle))
    if TO == 'up':
        for i in range(Cycle):
            Config.driver.swipe(Config.width / 2, Config.Height / 5 * 3, Config.width / 2,
                            Config.Height / 5 * 2, 400)
            Support.sleep(1.5)
    elif TO == 'down':
        for i in range(Cycle):
            Config.driver.swipe(Config.width / 2, Config.Height / 5 * 2, Config.width / 2,
                                Config.Height / 5 * 3, 400)
            Support.sleep(1.5)
    elif TO == 'left':
        for i in range( Cycle):
            Config.driver.swipe(Config.width / 5*3*2, Config.Height / 2, Config.width / 5*2,
                                Config.Height / 2, 400)
            Support.sleep(1.5)
    elif TO == 'right':
        for i in range( Cycle):
            Config.driver.swipe(Config.width / 5*2, Config.Height / 2, Config.width / 5*3,
                                Config.Height / 2, 400)
            Support.sleep(1.5)
    else:
        LogSys.logWarning('Key Error with {0}'.format(TO))

def scroll(FROM, Cycle):
    '''
    down,up,left,right
    :param TO:
    :return:
    '''
    LogSys.logInfo('scroll from {0} loop {1}'.format(FROM, Cycle))
    for i in range(Cycle):
        Config.driver.execute_script('mobile: scroll', {'direction': FROM})

def clickByPoint(driver,uiobject):
    Asserts.assertTrue(uiobject is not None, '对象定位异常，未定位到信息', Support.getTime())
    Mid_x = uiobject.rect.get('x') + uiobject.rect.get('width') / 2
    Mix_y = uiobject.rect.get('y') + uiobject.rect.get('height') / 2
    LogSys.logInfo('click element use point {0},{1}'.format(Mid_x, Mix_y))
    driver.tap([(Mid_x, Mix_y), (Mid_x, Mix_y)], 500)

def clickByPoint(driver,x,y):
    LogSys.logInfo('click element use point {0},{1}'.format(x, y))
    driver.tap([(x, y), (x, y)], 500)

def click(uiobject):
    LogSys.logInfo(type(uiobject))
    Asserts.assertTrue(uiobject is not None, '对象定位异常，未定位到信息',Support.getTime())
    LogSys .logInfo('click element')
    uiobject.click()

def clickV2(uiobject):
    '''
    失败不中断用例执行
    :param uiobject:
    :return:
    '''
    if uiobject is not None:
        LogSys .logInfo('click element')
        uiobject.click()
    else:
        LogSys.logInfo('对象定位异常，未定位到信息')

def clickByPointV2(driver,uiobject):
    '''
    失败不中断用例执行
    :param uiobject:
    :return:
    '''
    if uiobject is not None:
        Mid_x = uiobject.rect.get('x') + uiobject.rect.get('width') / 2
        Mix_y = uiobject.rect.get('y') + uiobject.rect.get('height') / 2
        LogSys.logInfo('click element use point {0},{1}'.format(Mid_x, Mix_y))
        driver.tap([(Mid_x, Mix_y), (Mid_x, Mix_y)], 500)
    else:
        LogSys.logInfo('对象定位异常，未定位到信息')

def getText(uiobject):
    if uiobject is None:
        return None
    return uiobject.text()

def input(uiobject, Value):
    Asserts.assertTrue(uiobject is not None, '对象定位异常，未定位到信息', Support.getTime())
    uiobject.clear()
    uiobject.send_keys(Value)

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

