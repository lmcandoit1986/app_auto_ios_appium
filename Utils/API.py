#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from Utils import Net

def getGoodsList(PageNum):
    Url = "https://www.bjycjf.com/api2/goods/business?page={0}&size=10".format(PageNum)
    return Net.request_get(Url)

def getGoodsDetail(id):
    Url = "https://www.bjycjf.com/api2/goods/detail/" + id
    return Net.request_get(Url)

def getBanner():
    Url = "https://www.bjycjf.com/api2/goods/operation"
    return Net.request_get(Url)



