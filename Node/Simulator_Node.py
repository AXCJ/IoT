#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import threading
import time
import json

import NIT_Node_Module
from terminalColor import bcolors

NodeUUID = "NODE-01"
# NodeUUID ="NODE-" +uuid.uuid1()

Functions = ["LED1", "LED2", "SW1"]
NodeFunctions = ['IOs', 'IPCams']

print("::::::::::::::::::::::::::::::::::::::::::\n")
print("::::::::::::::::::::::::::::::::::::::::::\n")
print("'##::: ##::'#######::'########::'########:")
print(" ###:: ##:'##.... ##: ##.... ##: ##.....::")
print(" ####: ##: ##:::: ##: ##:::: ##: ##:::::::")
print(" ## ## ##: ##:::: ##: ##:::: ##: ######:::")
print(" ##. ####: ##:::: ##: ##:::: ##: ##...::::")
print(" ##:. ###: ##:::: ##: ##:::: ##: ##:::::::")
print(" ##::. ##:. #######:: ########:: ########:")
print("..::::..:::.......:::........:::........::")
print("::::::::::::::::::::::::::::::::::::::::::\n")

nit = NIT_Node_Module.NIT_Node(NodeUUID, Functions, NodeFunctions)


# Connect to MQTT Server for communication
def NodeToServerMQTTThread():
    # print("thread name：　" + threading.current_thread().getName())

    # callback
    nit.CallBackRxRouting = RxRouting
    print(bcolors.HEADER + '===============================================\n' + bcolors.ENDC)
    print(bcolors.HEADER + '---------------Node(%s)--->>>Server in MQTT-\n' % NodeUUID + bcolors.ENDC)
    print(bcolors.HEADER + '>>>Start connect Server %s<<<' % (
        time.asctime(time.localtime(time.time()))) + bcolors.ENDC)
    print(bcolors.HEADER + '===============================================\n' + bcolors.ENDC)
    print(bcolors.HEADER + 'Register to IoT Server successful! \n' + bcolors.ENDC)

    try:

        nit.RegisterNoode();  # 'Control': 'NODE_REG'

    except (RuntimeError, TypeError, NameError) as e:
        print(bcolors.FAIL + "[INFO]Register error." + str(e) + bcolors.ENDC)
        raise
        sys.exit(1)


########### Keyboard interactive ##############
def RxRouting(self, _obj_json_msg):  # 收到訊息會執行這個，可在這邊新增功能
    nit.M2M_RxRouting(_obj_json_msg)


global flip
def loop():
    global flip
    decide = "g"
    decide = input("enter 't' to trigger")

    initMSGObj = {"TopicName": "NODE-01/SW1", "Control": "M2M_SET", "Source": "NODE-01", "M2M_Value": flip}
    initMSGSTR = json.dumps(initMSGObj)  # 將對象轉json(JavaScript Object Notation)

    if (decide == "t"):
        nit.DirectMSG("NODE-01/SW1", initMSGSTR)
        print("SW01 SENT.")
        flip = (~flip)


if __name__ == "__main__":
    MQTT_Thread = threading.Thread(target=NodeToServerMQTTThread, name="main_thread")
    MQTT_Thread.start()
    global flip
    flip = 0
    while True:
        loop()
