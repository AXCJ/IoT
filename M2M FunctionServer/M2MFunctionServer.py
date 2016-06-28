#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread

__author__ = 'Nathaniel'

import json
import copy
import sys
from terminalColor import bcolors
import class_M2MFS_MQTTManager


# 上層目錄
sys.path.append("..")
import config_ServerIPList

_g_cst_MQTTRegTopicName = "IOTSV/REG"  # 一開始要和IoT_Server註冊，故需要傳送信息至指定的MQTT Channel
_g_cst_FSUUID = "FS1"


# _globalGWList = []

print(bcolors.HEADER + ":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + bcolors.ENDC)
print(bcolors.HEADER + ":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + bcolors.ENDC)
print(bcolors.HEADER + "'##::::'##::'#######::'##::::'##::::'########::'######::'##::::'##:" + bcolors.ENDC)
print(bcolors.HEADER + " ###::'###:'##.... ##: ###::'###:::: ##.....::'##... ##: ##:::: ##:" + bcolors.ENDC)
print(bcolors.HEADER + " ####'####:..::::: ##: ####'####:::: ##::::::: ##:::..:: ##:::: ##:" + bcolors.ENDC)
print(bcolors.HEADER + " ## ### ##::'#######:: ## ### ##:::: ######:::. ######:: ##:::: ##:" + bcolors.ENDC)
print(bcolors.HEADER + " ##. #: ##:'##:::::::: ##. #: ##:::: ##...:::::..... ##:. ##:: ##::" + bcolors.ENDC)
print(bcolors.HEADER + " ##:.:: ##: ##:::::::: ##:.:: ##:::: ##:::::::'##::: ##::. ## ##:::" + bcolors.ENDC)
print(bcolors.HEADER + " ##:::: ##: #########: ##:::: ##:::: ##:::::::. ######::::. ###::::" + bcolors.ENDC)
print(bcolors.HEADER + ":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::" + bcolors.ENDC)
print(bcolors.HEADER + ":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n" + bcolors.ENDC)


def main():
    REGMSG = '{"FunctionServer":"%s", "Control":"FS_REG",' \
             '"Function":"M2M","FSIP":"10.0.0.1" ,"MappingNodes":"[IOs]", "Source":"%s"}' % \
             (_g_cst_FSUUID, _g_cst_FSUUID)

    publisherManger = class_M2MFS_MQTTManager.PublisherManager()
    publisherManger.MQTT_PublishMessage(_g_cst_MQTTRegTopicName, REGMSG)

    # 訂閱自身名稱topic
    class_M2MFS_MQTTManager.SubscriberThreading(_g_cst_FSUUID).run()


if __name__ == '__main__':
    main()
