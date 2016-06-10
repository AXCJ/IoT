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
_g_cst_IoTServerUUID = "IOTSV-123"

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

_gg = 0

@app.route('/nit/iotsv/api/nodes', methods=['GET'])
def get_tasks():
    return jsonify({'nodes': _globalNodeList})

def updateIoTNodeList(nodeObj):
    _globalNodeList.append(nodeObj)

def removeIoTNodeList(nodeObj):
    for p in _globalNodeList:
        if (p["NodeName"] == nodeObj.NodeName):
            _globalNodeList.remove(p)

def main():

    class_IoTSV_MQTTManager.SubscriberThreading("IOTSV/REG", updateIoTNodeList, removeIoTNodeList).start()
    app.run(debug=False,host="0.0.0.0")

    # sm = class_MQTTManager.SubscriberManager()
    # sm.subscribe("GW1")


if __name__ == '__main__':
    #_gg=1
    main()
