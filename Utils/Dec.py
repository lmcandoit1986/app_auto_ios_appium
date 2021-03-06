import os
import sys
from functools import wraps, update_wrapper

from Config import Config

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from Utils import UiObject, LogSys

def elementGPS(type=None, value=None, timeout=10, isAssert=True):
    '''
    后续统一使用该方法定位
    :param type:
    :param value:
    :param timeout:
    :param isAssert:
    :return:
    '''
    def deco(func):
        def wrapper(*arg, **kw):
            return UiObject.findElementMakeSureEnabled(driver=Config.driver, type=type, value=value, timeout=timeout, isAssert=isAssert)
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

def CaseRun(function):
    @wraps(function)
    def get_fun_name(self, *args, **kwargs):
        LogSys.logInfo('INSTRUMENTATION_STATUS: test=' + function.__name__)
        function(self, *args, **kwargs)
        LogSys.logInfo('INSTRUMENTATION_STATUS: end')
    return get_fun_name


def CaseDesc(desc):
    def check_returns(f):
        def new_f(*args, **kwds):
            LogSys.logInfo('INSTRUMENTATION_STATUS: title=' + desc)
            result = f(*args, **kwds)
            return result
        update_wrapper(new_f, f)
        return new_f
    return check_returns