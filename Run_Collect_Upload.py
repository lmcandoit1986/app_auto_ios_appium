#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
from subprocess import Popen, PIPE, STDOUT
import requests
from urllib3.exceptions import MaxRetryError

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from Config import Config
from Utils import Support

class AutoCase(object):
    cmds = []
    Cases = os.listdir('./Cases/')
    for case in Cases:
        if case.endswith('.py'):
            cmds.append('python3 -m unittest Cases/{0}'.format(case))
    all = []
    def RunCase(self):
        for cmd in self.cmds:
            print(cmd)
            self.ProcessCMD = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
            Check_Name = True
            Check_Result = False
            checkLog = False
            Log =''
            item = {}
            while self.ProcessCMD.poll() is None:
                Results = self.ProcessCMD.stdout.readline().decode("utf-8").strip().replace('\\n', '')
                print(Results)
                if 'ERROR:' in Results:
                    pattern = re.compile('ERROR: (.*) \(.*')
                    Name = pattern.findall(Results)
                    isHave = False
                    item = {}
                    if not Name[0] == 'setUpClass' and not 'tearDownClass'==Name[0]:
                        for line in all:
                            if line['case'] == Name[0]:
                                isHave = True
                                break
                        if not isHave:
                            checkLog= True
                            item['caseName'] = Name[0]
                            item['model'] = Name[0].split('_')[1]
                            item['case'] = item['caseName']
                            item['result'] = -2
                            item['comment'] = 'appium server出错'
                            item['pic'] = ''
                            item['useTime'] = 0
                            self.all.append(item)

                if Check_Name:

                    if 'INSTRUMENTATION_STATUS: test=' in Results:
                        item = {}
                        item['caseName'] = Results.split('=')[1]
                        item['model'] = item['caseName'].split('_')[1]
                        item['case'] = item['caseName']
                        item['result'] = -3
                        item['comment'] = ''
                        item['pic'] = ''
                        Check_Name = False
                        Check_Result = True
                        continue
                if Check_Result:
                    if 'INSTRUMENTATION_STATUS: pic' in Results:
                        if not Results.split('=')[1].strip() == 'None':
                            item['pic'] = 'http://127.0.0.1/IMG/{0}/{1}'.format(Support.getNextDay(0),Results.split('=')[1])
                    if 'INSTRUMENTATION_STATUS: time=' in Results:
                        item['useTime'] = int(Results.split('=')[1])
                        Check_Result = False
                        Check_Name = True
                        self.all.append(item)
                    if 'INSTRUMENTATION_STATUS: result' in Results:
                        if Results.split('=')[1] == 'Failed':
                            item['result'] = -1
                    if 'INSTRUMENTATION_STATUS: end' in Results:
                        if item['result'] == -3:
                            item['result'] = 0
                    if 'INSTRUMENTATION_STATUS: title' in Results:
                        item['caseName']= Results.split('=')[1]
                    if 'INSTRUMENTATION_STATUS: reason' in Results:
                        item['comment'] = Results.replace('INSTRUMENTATION_STATUS: reason=', '')

        jd = self.createDict(self.all)
        print(jd)

        try:
            self.copy()
            res = requests.post('http://152.136.202.79:9092/server/result/v2/push', json=jd)
            # res = requests.post('http://localhost:9092/server/result/v2/push', json=jd)
            print(res.content)
        except ConnectionError as e:
            self.saveResult(jd)
            print(e)
        except MaxRetryError as e:
            self.saveResult(jd)
            print(3)


        # print('url:http://152.136.202.79:9092/web/watcher?only={0}'.format(jd['data']['only']))

    def saveResult(self,jsonRes):
        f = open('./result.log','a')
        f.write(jsonRes)
        f.close()

    def createDict(self, item):
        back ={}
        result = {}
        sum = {}
        sum['platform']='iOS'
        sum['app']='平安健康险'
        sum['model'] = Config.devices
        sum['module'] = self.getModelList(item)
        sum['uset'] = '{0} m'.format(round(self.getAlltime(item)/60, 2))
        sum['runt'] = time.strftime("%Y-%m-%d %X", time.localtime())
        sum['all'] = len(item)
        sum['version'] = '3.13.1'
        sum['fail'] = self.getFailed(item)
        sum['Jenkinsid'] = time.strftime("%Y%m%d%H%M", time.localtime())
        result['detail'] = item
        result['sum'] = sum
        back['data'] = result
        return back

    def getFailed(self, lists):
        i = 0
        for line in lists:
            if not line['result'] == 0:
                i += 1
        return i

    def getAlltime(self,lists):
        back =0
        for line in lists:
            back += line['useTime']
        return back

    def getModelList(self,lists):
        listback =[]
        for line in lists:
            listback.append(line['model'])
        setback = set(listback)
        listresult = list(setback)
        print(listresult)
        return listresult

    def copy(self):
        Today = Support.getNextDay(0)
        if not os.path.exists('/Library/WebServer/Documents/IMG/{0}'.format(Today)):
            os.mkdir('/Library/WebServer/Documents/IMG/{0}'.format(Today))

        os.system('cp /Users/liming/Desktop/iOSAutoTest/* /Library/WebServer/Documents/IMG/{0}/'.format(Today))
        os.system('rm -rf /Users/liming/Desktop/iOSAutoTest/')
        os.mkdir('/Users/liming/Desktop/iOSAutoTest')


Auto = AutoCase()
Auto.RunCase()