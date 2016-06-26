#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread

__author__ = 'Nathaniel'

import os
import json
import copy
import sys
sys.path.append(os.path.split(os.getcwd())[0])
from terminalColor import  bcolors
import class_IoTSV_MQTTManager

# 上層目錄
sys.path.append("..")
import config_ServerIPList

_g_cst_ToMQTTTopicServerIP = config_ServerIPList._g_cst_ToMQTTTopicServerIP
_g_cst_ToMQTTTopicServerPort = config_ServerIPList._g_cst_ToMQTTTopicServerPort
_g_cst_IoTServerUUID = "IOTSV"

_globalNodeList = []
_globalFSList = []
_globalMDList = []

print(bcolors.HEADER + "::::::::::::::::::::::::::::::::::::::::::::::::" + bcolors.ENDC)
print(bcolors.HEADER + "::::::::::::::::::::::::::::::::::::::::::::::::" + bcolors.ENDC)
print(bcolors.HEADER + "'####::'#######::'########::'######::'##::::'##:" + bcolors.ENDC)
print(bcolors.HEADER + ". ##::'##.... ##:... ##..::'##... ##: ##:::: ##:" + bcolors.ENDC)
print(bcolors.HEADER + ": ##:: ##:::: ##:::: ##:::: ##:::..:: ##:::: ##:" + bcolors.ENDC)
print(bcolors.HEADER + ": ##:: ##:::: ##:::: ##::::. ######:: ##:::: ##:" + bcolors.ENDC)
print(bcolors.HEADER + ": ##:: ##:::: ##:::: ##:::::..... ##:. ##:: ##::" + bcolors.ENDC)
print(bcolors.HEADER + ": ##:: ##:::: ##:::: ##::::'##::: ##::. ## ##:::" + bcolors.ENDC)
print(bcolors.HEADER + "'####:. #######::::: ##::::. ######::::. ###::::" + bcolors.ENDC)
print(bcolors.HEADER + "....:::.......::::::..::::::......::::::...:::::" + bcolors.ENDC)
print(bcolors.HEADER + "::::::::::::::::::::::::::::::::::::::::::::::::\n" + bcolors.ENDC)


def main():
    class_IoTSV_MQTTManager.SubscriberThreading("IOTSV/REG").start()

    # sm = class_MQTTManager.SubscriberManager()
    # sm.subscribe("GW1")


if __name__ == '__main__':
    main()
