#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import sys
import os
import smtplib
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
    cmd_start = '/Users/liming/Library/Android/sdk/platform-tools/adb -s B2NGAC6850506946'
    cmds = [
        '{0} shell am instrument -w -r   -e debug false -e class \'com.hnrmb.Cases.FIPCase\' com.hnrmb.test/androidx.test.runner.AndroidJUnitRunner'.format(cmd_start)]
    all = []
    version =0
    device = ''

    def makeSure(self):
        pathPro = os.path.dirname(os.path.abspath(__file__))
        pathCMD = os.getcwd()
        if not pathCMD == pathPro:
            os.chdir(pathPro)

    def RunCase(self):

        self.version = os.popen('{0} shell dumpsys package com.hnrmb.salary |grep versionName|cut -d"=" -f2'.format(self.cmd_start)).read()
        self.saveToFile(self.version)
        self.rt = time.strftime("%Y-%m-%d %X", time.localtime())
        for cmd in self.cmds:
            self.ProcessCMD = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
            Check_Name = True
            Check_Result = False
            Check_Last = False
            Check_desc = False
            Check_device = True
            item = {}
            while self.ProcessCMD.poll() is None:
                Results = self.ProcessCMD.stdout.readline().decode("utf-8").strip().replace('\\n', '')
                self.saveToFile(Results)
                if Check_device:
                    if 'INSTRUMENTATION_STATUS: device=' in Results:
                        self.device = Results.split('=')[1].strip()
                        Check_device = False
                        self.saveToFile(self.device)
                if Check_Name:
                    if 'INSTRUMENTATION_STATUS: test=' in Results:
                        item = {}
                        model_case = Results.split('=')[1].strip()
                        item['case'] = (model_case.split('_'))[1]
                        item['model'] = (model_case.split('_'))[0]
                        item['caseName'] = ""
                        item['result'] = -3
                        item['comment'] = ''
                        item['pic'] = ''
                        Check_Name = False
                        Check_desc = True
                        vn = self.startscreenrecord()
                        self.saveToFile(vn)
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
                        item['comment'] = Results.replace('INSTRUMENTATION_STATUS: stack=', '') + ',录屏文件:{0}.mp4'.format(vn)
                        continue
                    if 'INSTRUMENTATION_STATUS: test=' in Results:
                        Check_Result = False
                        Check_Last = True
                        continue
                if Check_Last:
                    if 'INSTRUMENTATION_STATUS_CODE:' in Results:
                        item['result'] = int(Results.split(':')[1].strip())
                        self.closescreenrecord()
                        if item['result'] == 0:
                            os.system('{0} shell rm -rf sdcard/vedio/{1}.mp4'.format(self.cmd_start,vn))
                        # print(item)
                        self.all.append(item)
                        Check_Last = False
                        Check_Name = True

                        continue

        jd = self.createDict(self.all)
        self.saveToFile(str(jd))

        try:
            self.copy(jd)
            res = requests.post('http://superqa.com.cn:9091/server/result/v3/push', json=jd).json()
            self.saveToFile(str(res))
            if jd['data']['sum']['fail'] > 0:
                self.sms(jd['data']['sum']['Jenkinsid'])
                # self.SendEmail(jd['data']['sum']['Jenkinsid'])
        except ConnectionError as e:
            self.saveResult(jd)
        except MaxRetryError as e:
            self.saveResult(jd)

    def saveResult(self, jsonRes):
        f = open('/Users/liming/Desktop/log/Android/result.log', 'a+')
        f.write(jsonRes)
        f.close()

    def sms(self,jenkinsId):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=753a96b4-b476-48cf-a648-354f97616957'

        header = {'Content-Type': 'application/json'}

        body = {
            "msgtype": "news",
            "news": {
                "articles": [
                    {
                        "title": "UI 自动化（理财）结果反馈（线下）",
                        "description": "发现异常，点击查看明细！",
                        "url": "http://superqa.com.cn:9091/web/result/uiauto/detail?jenkinsId={0}&platform=Android&user=visitor".format(jenkinsId),
                        "picurl": "http://superqa.com.cn:9091/media/img/new.png"
                    }
                ]
            }
        }

        requests.post(url=url, headers=header, json=body)

    def createDict(self, item):
        back = {}
        result = {}
        sum = {}

        sum['platform'] = 'Android'
        sum['app'] = '华能成长宝'
        sum['model'] = self.device
        sum['module'] = self.getModelList(item)
        sum['uset'] = time.strftime('%H:%M:%S', time.gmtime(self.getAlltime(item)))
        sum['runt'] = self.rt
        sum['all'] = len(item)
        sum['env'] = 'test'
        sum['version'] = self.version
        sum['fail'] = self.getFailed(item)
        sum['Jenkinsid'] = time.strftime("%Y%m%d%H%M", time.localtime())+"0"
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

    def copy(self, jd):
        os.system(
            '{0} pull /sdcard/hnrmb/ /Users/liming/Desktop/iOSAutoTest/'.format(self.cmd_start))
        os.system('{0} shell rm -rf /sdcard/hnrmb/'.format(self.cmd_start))
        for line in jd['data']['detail']:
            if line['pic'] != '':
                self.sendImg('/Users/liming/Desktop/iOSAutoTest/hnrmb/', line['pic'].split('/')[-1])
        # os.system('rm -rf /Users/liming/Desktop/iOSAutoTest/')
        # os.mkdir('/Users/liming/Desktop/iOSAutoTest')
        os.system(
            '{0} pull /sdcard/vedio/ /Users/liming/Desktop/iOSAutoTest/'.format(self.cmd_start))
        os.system(
            '{0} shell rm -rf /sdcard/vedio/*.*'.format(self.cmd_start))

    def saveToFile(self, word):
        '''
        保存日志到本地
        :param log_file:
        :param word:
        :return:
        '''
        file = open('{0}log_{1}'.format('/Users/liming/Desktop/Auto/Android/', Support.getTimeDay()), 'a+')
        file.write(str(word)+'\n')
        file.flush()
        file.close()
        pass

    def startscreenrecord(self):
        vn = time.time()
        self.ProcessVedio = Popen('{0} shell screenrecord sdcard/vedio/{1}.mp4'.format(self.cmd_start,vn), stdout=PIPE, stderr=STDOUT, shell=True)
        return vn
    def closescreenrecord(self):
        self.ProcessVedio.kill()


if __name__ == '__main__':
    Auto = AutoCase()
    Auto.makeSure()
    Auto.RunCase()