#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import smtplib
import sys
import time
from email.header import Header
from email.mime.text import MIMEText
from subprocess import Popen, PIPE, STDOUT
import requests
from urllib3.exceptions import MaxRetryError

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from Utils import Support


class AutoCase(object):
    cmds = ['/Users/liming/Library/Android/sdk/platform-tools/adb -s 1dcb290a shell am instrument -w -r   -e debug false -e class \'com.hnrmb.Cases.SumCase\' com.hnrmb.test/androidx.test.runner.AndroidJUnitRunner']
    all = []

    def RunCase(self):
        self.rt = time.strftime("%Y-%m-%d %X", time.localtime())
        for cmd in self.cmds:
            self.ProcessCMD = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
            Check_Name = True
            Check_Result = False
            Check_Last = False
            Check_desc = False
            item = {}
            while self.ProcessCMD.poll() is None:
                Results = self.ProcessCMD.stdout.readline().decode("utf-8").strip().replace('\\n', '')
                # print(Results)
                if Check_Name:
                    if 'INSTRUMENTATION_STATUS: test=' in Results:
                        item = {}
                        model_case = Results.split('=')[1].strip()
                        # print(model_case)
                        item['case'] = (model_case.split('_'))[1]
                        item['model'] = (model_case.split('_'))[0]
                        item['caseName'] = ""
                        item['result'] = -3
                        item['comment'] = ''
                        item['pic'] = ''
                        Check_Name = False
                        Check_desc = True
                        continue

                if Check_desc:
                    if 'INSTRUMENTATION_STATUS: desc=' in Results:
                        item['caseName'] = Results.split('=')[1].strip()
                        Check_desc = False
                        Check_Result = True
                        continue

                if Check_Result:
                    if 'INSTRUMENTATION_STATUS: img' in Results:
                        item['pic'] = '/{2}/{0}/{1}.png'.format('img', Results.split('=')[1].strip(), 'media')
                        continue
                    if 'INSTRUMENTATION_STATUS: time=' in Results:
                        item['useTime'] = int(Results.split('=')[1])
                        continue
                    if 'INSTRUMENTATION_STATUS: stack' in Results:
                        item['comment'] = Results.replace('INSTRUMENTATION_STATUS: stack=', '')
                        continue
                    if 'INSTRUMENTATION_STATUS: test=' in Results:
                        Check_Result = False
                        Check_Last = True
                        continue
                if Check_Last:
                    if 'INSTRUMENTATION_STATUS_CODE:' in Results:
                        item['result'] = int(Results.split(':')[1].strip())
                        # print(item)
                        self.all.append(item)
                        Check_Last = False
                        Check_Name = True
                        continue

        jd = self.createDict(self.all)
        # print(jd)
        try:
            self.copy(jd)
            requests.post('http://superqa.com.cn:9091/server/result/v3/push', json=jd)
            if jd['data']['sum']['fail'] > 0:
                self.SendEmail(jd['data']['sum']['Jenkinsid'])
        except ConnectionError as e:
            self.saveResult(jd)
        except MaxRetryError as e:
            self.saveResult(jd)

    def saveResult(self, jsonRes):
        f = open('/Users/liming/Desktop/result.log', 'a')
        f.write(jsonRes)
        f.close()

    def createDict(self, item):
        back = {}
        result = {}
        sum = {}

        sum['platform'] = 'Android'
        sum['app'] = '华能成长宝'
        sum['model'] = '小米8'
        sum['module'] = self.getModelList(item)
        sum['uset'] = time.strftime('%H:%M:%S', time.gmtime(self.getAlltime(item)))
        sum['runt'] = self.rt
        sum['all'] = len(item)
        sum['version'] = '5.9.0'
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

    def SendEmail(self, JenkinsID):
        # 第三方 SMTP 服务
        mail_host = "smtp.exmail.qq.com"  # 设置服务器
        mail_user = "liming@ycfin.com.cn"  # 用户名
        mail_pass = "Lm9182731"  # 口令
        sender = 'liming@ycfin.com.cn'
        receivers = ['liming@ycfin.com.cn']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        message = MIMEText(
            'App 自动化监控发现异常。。。\n请处理\nhttp://superqa.com.cn:9091/web/result/uiauto/detail?jenkinsId={0}&platform=Android&user=visitor'.format(
                JenkinsID),
            'plain', 'utf-8')
        message['From'] = Header("云成测试监控", 'utf-8')
        message['To'] = Header("云成", 'utf-8')
        subject = 'App 自动化监控发现异常'
        message['Subject'] = Header(subject, 'utf-8')

        try:
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)
            smtpObj.ehlo()
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            smtpObj.close()
        except smtplib.SMTPException as e:
            i = 1

    def sendImg(self, img_path, img_name, img_type='image/jpeg'):
        files = {'img': (img_name, open(img_path + img_name, 'rb'), img_type)}
        url = 'http://superqa.com.cn:9091/api/img/upload'
        # 上传图片的时候，不使用data和json，用files
        response = requests.post(url=url, files=files).json()
        return response

    def getAlltime(self, lists):
        back = 0
        for line in lists:
            back += line['useTime']
        return back

    def getModelList(self, lists):
        listback = []
        for line in lists:
            listback.append(line['model'])
        setback = set(listback)
        listresult = list(setback)
        return listresult

    def copy(self,jd):
        # Today = Support.getNextDay(0)
        # if not os.path.exists('/Library/WebServer/Documents/IMG/{0}'.format(Today)):
        #     os.mkdir('/Library/WebServer/Documents/IMG/{0}'.format(Today))
        os.system('/Users/liming/Library/Android/sdk/platform-tools/adb -s 1dcb290a pull /sdcard/hnrmb/ /Users/liming/Desktop/iOSAutoTest/')
        os.system('/Users/liming/Library/Android/sdk/platform-tools/adb -s 1dcb290a shell rm -rf /sdcard/hnrmb/')
        for line in jd['data']['detail']:
            if line['pic'] != '':
                self.sendImg('/Users/liming/Desktop/iOSAutoTest/hnrmb/', line['pic'].split('/')[-1])
        # os.system('cp /Users/liming/Desktop/iOSAutoTest/* /Library/WebServer/Documents/IMG/{0}/'.format(Today))
        os.system('rm -rf /Users/liming/Desktop/iOSAutoTest/')
        os.mkdir('/Users/liming/Desktop/iOSAutoTest')


Auto = AutoCase()
Auto.RunCase()
