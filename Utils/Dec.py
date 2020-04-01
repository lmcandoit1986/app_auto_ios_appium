import os
import sys
from functools import wraps

from Config import Config

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from Utils import UiObject, LogSys


def elementDecorator(type, value, WAIT_TIME=3):
    '''
    定位元素装饰器
    :param driver:
    :param type:
    :param value:
    :param WAIT_TIME:
    :return: 如果未匹配到元素，返回None
    '''
    def deco(func):
        def wrapper(*arg, **kw):
            ob = UiObject.findUiObject(Config.driver, type, value)
            if UiObject.assertUiobjectEnabledInExpectTime(ob, WAIT_TIME):
                return ob
            else:
                return None
        return wrapper
    return deco

def scrollSearchElementDecorator(type,value ,PageMax =10):
    '''
    列表定位元素，默认最大滑动10次，如果未找到元素，返回None
    :param driver:
    :param type:
    :param value:
    :param PageMax:
    :return:
    '''
    def deco(func):
        def wrapper(*arg, **kw):
            ob = UiObject.scrollSearchElement(Config.driver, type, value, PageMax)
            return ob
        return wrapper
    return deco

def CaseInfo(function):
    @wraps(function)
    def get_fun_name(self, *args, **kwargs):
        LogSys.logInfo('INSTRUMENTATION_STATUS: test=' + function.__name__)
        function(self, *args, **kwargs)
        LogSys.logInfo('INSTRUMENTATION_STATUS: end')
    return get_fun_name
