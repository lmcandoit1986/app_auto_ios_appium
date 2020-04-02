#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os
import sys
import requests

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from Utils import LogSys

def setHeader():
    header = {}
    header['User-Agent'] = "HN-Salary iOS/5.7.10.3799 (12.1.1; iPhone10,2) 2208x1242 [App Store]"
    header['cookie'] ='''XDevice=cbea71d8638e0cf4eb1352e34828093e; XToken=669a133d-1f6e-4b3b-9cfc-89c6c461b6a9; SESSION=669a133d-1f6e-4b3b-9cfc-89c6c461b6a9; gaOpenId=GA201909261721261038397092; _UNAME=%E4%B8%80%E9%9B%B6%E4%BA%8C'''
    return header

def request_get(Url):
    res = requests.get(url=Url, headers=setHeader())
    LogSys.logInfo(res.content)
    return json.loads(res.content)

def request_post(Url, Body):
    res = requests.post(url=Url, headers=setHeader(), json=Body)
    LogSys.logInfo(res.content)
    return json.loads(res.content)

