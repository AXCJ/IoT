#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread

__author__ = 'Nathaniel'
import os
import json
import copy
import sys
sys.path.append(os.path.split(os.getcwd())[0])
from terminalColor import bcolors
import class_M2MFS_MQTTManager


# 上層目錄
sys.path.append("..")
import config_ServerIPList

_g_cst_MQTTRegTopicName = "IOTSV/REG"  # 一開始要和IoT_Server註冊，故需要傳送信息至指定的MQTT Channel
_g_cst_FSUUID = "CG_NCKUMVLAB92823@FS-41d0b11e-3d3a-11e6-a655-3c07544f6d45"
# _g_cst_FSUUID = "FS_CG@FS-" + str(uuid.uuid1())


# _globalGWList = []

# (Font: 'nancyj-underlined')
print(bcolors.HEADER + ":::::::::::::::::::::::::::::" + bcolors.ENDC)
print(bcolors.HEADER + ":::::::::::::::::::::::::::::" + bcolors.ENDC)
print(bcolors.HEADER + "      a88888b.  .88888.  " + bcolors.ENDC)
print(bcolors.HEADER + "     d8'   `88 d8'   `88 " + bcolors.ENDC)
print(bcolors.HEADER + "     88        88        " + bcolors.ENDC)
print(bcolors.HEADER + "     88        88   YP88 " + bcolors.ENDC)
print(bcolors.HEADER + "     Y8.   .88 Y8.   .88 " + bcolors.ENDC)
print(bcolors.HEADER + "      Y88888P'  `88888'  " + bcolors.ENDC)
print(bcolors.HEADER + "     oooooooooooooooooooo" + bcolors.ENDC)
print(bcolors.HEADER + ":::::::::::::::::::::::::::::" + bcolors.ENDC)
print(bcolors.HEADER + ":::::::::::::::::::::::::::::\n" + bcolors.ENDC)

# print(bcolors.HEADER + ":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + bcolors.ENDC)
# print(bcolors.HEADER + ":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + bcolors.ENDC)
# print(bcolors.HEADER + "         ########::'######:::::'########::'####::'######::" + bcolors.ENDC)
# print(bcolors.HEADER + "         ##.....::'##... ##:::: ##.... ##:. ##::'##... ##:" + bcolors.ENDC)
# print(bcolors.HEADER + "         ##::::::: ##:::..::::: ##:::: ##:: ##:: ##:::..::" + bcolors.ENDC)
# print(bcolors.HEADER + "         ######:::. ######::::: ########::: ##:: ##:::::::" + bcolors.ENDC)
# print(bcolors.HEADER + "         ##...:::::..... ##:::: ##.....:::: ##:: ##:::::::" + bcolors.ENDC)
# print(bcolors.HEADER + "         ##:::::::'##::: ##:::: ##::::::::: ##:: ##::: ##:" + bcolors.ENDC)
# print(bcolors.HEADER + "         ##:::::::. ######::::: ##::::::::'####:. ######::" + bcolors.ENDC)
# print(bcolors.HEADER + ":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + bcolors.ENDC)
# print(bcolors.HEADER + ":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n" + bcolors.ENDC)


def main():
    REGMSG = '{"FunctionServer":"%s", "Control":"FS_REG",' \
             '"Function":"M2F","FSIP":"92.8.23.1", "MappingNodes":"[CG, Cam, GPS]", "Source":"%s"}' % \
             (_g_cst_FSUUID, _g_cst_FSUUID)

    publisherManger = class_M2MFS_MQTTManager.PublisherManager()
    publisherManger.MQTT_PublishMessage(_g_cst_MQTTRegTopicName, REGMSG)

    # 訂閱自身名稱topic
    class_M2MFS_MQTTManager.SubscriberThreading(_g_cst_FSUUID).start()


if __name__ == '__main__':
    main()
