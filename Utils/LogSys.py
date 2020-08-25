#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from Config import Config
from Utils import Support

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


def logInfo(word):
    '''
    普通日志输出
    :param log:
    :param word:
    :return:
    '''
    log.info(word)
    log_file = 'log_{0}'.format(Support.getTimeDay())
    saveToFile(log_file, '{0} {1} {2} \n'.format(Support.getTimeForLog(),'-INFO -',word))

def logError(word):
    '''
    报错日志输出
    :param log:
    :param word:
    :return:
    '''
    log.error(word)
    log_file = 'log_{0}'.format(Support.getTimeDay())
    saveToFile(log_file, '{0} {1} {2} \n'.format(Support.getTimeForLog(),'-INFO -',word))
    # log.error(value.replace('"','\"').replace("'","\'").replace('[','').replace(']','').replace('{','').replace('{',''))

def logWarning(word):
    '''
    告警日志输出
    :param log:
    :param word:
    :return:
    '''
    log.warning(word)
    log_file = 'log_{0}'.format(Support.getTimeDay())
    saveToFile(log_file, '{0} {1} {2} \n'.format(Support.getTimeForLog(),'-INFO -',word))
    # log.warning(value.replace('"','\"').replace("'","\'").replace('[','').replace(']','').replace('{','').replace('{',''))

def saveToFile(log_file,word):
    '''
    保存日志到本地
    :param log_file:
    :param word:
    :return:
    '''
    file = open('{0}{1}'.format(Config.log_path, log_file),'a+')
    file.write(str(word)+'\n')
    file.flush()
    file.close()