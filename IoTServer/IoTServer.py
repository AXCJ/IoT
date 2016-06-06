#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread
from flask import Flask, jsonify
from flask import abort



__author__ = 'Nathaniel'

import os
import json
import copy
import sys
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


app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/nit/iotsv/api/nodes', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': _globalNodeList})

def updateIoTNodeList(nodeObj):
    _globalNodeList.append(nodeObj)

def main():
    class_IoTSV_MQTTManager.SubscriberThreading("IOTSV/REG", updateIoTNodeList).start()
    app.run(debug=True)

    # sm = class_MQTTManager.SubscriberManager()
    # sm.subscribe("GW1")


if __name__ == '__main__':
    main()
