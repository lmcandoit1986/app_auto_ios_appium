#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from tkinter import Image

from Config import Config
from Utils import LogSys, Support


def screenShot(Path):
    if not os.path.exists('{0}{1}/'.format(Config.img_path, Support.getTimeDay())):
        os.mkdir('{0}{1}/'.format(Config.img_path, Support.getTimeDay()))
    Config.driver.get_screenshot_as_file(Path)


def screenShotByElement(Pic_Name, Element):
    if Element.is_displayed():
        Element.screenshot('{0}{3}/{1}.{2}'.format(Config.img_path, Pic_Name, 'png', Support.getTimeDay()))
    else:
        ErrorMsg = 'Element is not displayed,take screenshot failed!'
        LogSys.logError(ErrorMsg)


def cutPicWithoutNavigationBar(Pic_name, Del_Pic_Ori=True):
    '''
     裁剪调顶部系统通知栏的部分
    :param Pic_name: 截图后的名称
    :param Del_Pic_Ori: 是否删除原图
    :return:
    '''
    Ori = '{0}{1}.{2}'.format(Config.img_path, 'test', 'png')
    screenShot(Ori)
    img = Image.open(Ori)
    img_size = img.size
    h = img_size[1]  # 图片高度
    w = img_size[0]  # 图片宽度
    x = 0
    y = 70
    w = w
    h = h - 70
    region = img.crop((x, y, x + w, y + h))
    region.save('{0}{2}/{1}.png'.format(Config.img_path, Pic_name, Support.getTimeDay()))
    if Del_Pic_Ori:
        os.remove(Ori)
