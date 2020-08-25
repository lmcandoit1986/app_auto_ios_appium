#!/usr/bin/python3
# -*- coding: utf-8 -*-
from selenium.common.exceptions import NoAlertPresentException

from Config import Config
from Utils import LogSys


def alertAccept():
    try:
        Config.driver.switch_to.alert.accept()
    except NoAlertPresentException as E:
        LogSys.logError('Error:{0}'.format(E))


def alertDismiss():
    try:
        Config.driver.switch_to.alert.dismiss()
    except NoAlertPresentException as E:
        LogSys.logError('Error:{0}'.format(E))
