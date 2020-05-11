#!/usr/bin/python3
# -*- coding: utf-8 -*-

import base64
from email import header
import pickle
import poplib
import re


class emails():
    popHost = 'pop.exmail.qq.com'
    port = 995
    userName = 'liming@ycfin.com.cn'
    passWord = 'Lm918273'

    def login(self):
        try:
            self.mailLink = poplib.POP3_SSL(self.popHost)
            self.mailLink.set_debuglevel(0)
            self.mailLink.user(self.userName)
            self.mailLink.pass_(self.passWord)
            msgNum, Size = self.mailLink.stat()
            print(msgNum)

        except Exception as e:
            print(u'login fail! ' + str(e))
            quit()



    def receiveNewEmail(self, lastCheckNum):
        newNum,Size = self.mailLink.stat()
        for Num in range(lastCheckNum, newNum):
            resp, mail, octets = self.mailLink.retr(Num+1)
            fromer = ''
            Subject = ''
            CheckSubject = False
            for line in mail:
                lineDecode = line.decode('utf-8')
                if lineDecode.startswith('From'):
                    # print(lineDecode)
                    ss = re.search('.*<(.*)>.*', lineDecode)
                    fromer =ss.group(1)
                    continue
                if lineDecode.startswith('Subject'):
                    # print(lineDecode)
                    if '=?UTF-8?B?' in lineDecode:
                        Subject += base64.b64decode(lineDecode[len('Subject: =?UTF-8?B?'):]).decode("utf-8")
                    else:

                        # header.decode_header()
                        # print(text,encoding)
                        Subject += lineDecode[len('Subject: '):]
                    CheckSubject = True
                    continue
                if CheckSubject:
                    if ': ' not in lineDecode:
                        if '=?UTF-8?B?' in lineDecode:
                            Subject += base64.b64decode(lineDecode[len('=?UTF-8?B?'):]).decode("utf-8")
                        else:
                            Subject += lineDecode
                    else:
                        CheckSubject = False
            print('Subject:{0},from:{1}'.format(Subject,fromer))


    def PDump(self,obj):
        f = open("./email.txt", 'wb')
        pickle.dump(obj, f)
        f.close()


    def Ploads(self):
        f = open("./email.txt", 'rb')
        back =pickle.load(f)
        f.close()
        return back



mail = emails()
mail.login()
mail.receiveNewEmail(980)