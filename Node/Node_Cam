#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import threading
import time
import json
# import base64
import os

import NIT_Node_Module
from terminalColor import bcolors

NodeUUID = "NODE-picture"
# NodeUUID ="NODE-" +uuid.uuid1()

Functions = ["LED1", "LED2", "SW1"]
NodeFunctions = ['IOs', 'IPCams']

print("::::::::::::::::::::::::::::::::::::::::::")
print("::::::::::::::::::::::::::::::::::::::::::")
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
    print("thread name：　" + threading.current_thread().getName())

    # callback
    nit.CallBackRxRouting = RxRouting
    print(bcolors.HEADER + '===============================================\n' + bcolors.ENDC)
    print(bcolors.HEADER + '---------------Node(%s)--->>>Server in MQTT-\n' % NodeUUID + bcolors.ENDC)
    print(bcolors.HEADER + '>>>Start connect Server %s<<<' % (
        time.asctime(time.localtime(time.time()))) + bcolors.ENDC)
    print(bcolors.HEADER + '===============================================\n' + bcolors.ENDC)
    print(bcolors.HEADER + 'Register to IoT Server successful! \n' + bcolors.ENDC)

    try:

        nit.RegisterNoode()  # 向IoT_Server註冊 TopicName = "IOTSV/REG"

    except (RuntimeError, TypeError, NameError) as e:
        print(bcolors.FAIL + "[INFO]Register error." + str(e) + bcolors.ENDC)
        raise
        sys.exit(1)


########### Keyboard interactive ##############
def RxRouting(self, _obj_json_msg):
    nit.M2M_RxRouting(_obj_json_msg)


global flip
def loop():
    global flip
    decide = "g"
    decide = input("enter 't' or 'img' to trigger message or image, respectively.: \n")

    initMSGObj = {'TopicName': "NODE-picture", 'Control': 'picture_SET', 'Source': "NODE-picture", 'M2M_Value': flip}
    initMSGSTR = json.dumps(initMSGObj)

    if decide == "t":
        nit.DirectMSG("NODE-picture", initMSGSTR)
        flip = (~flip)

    if decide == "img":
        imageByteArray = convertImageToByteArray()
        nit.DirectMSG("image/jpg", imageByteArray)

def convertImageToByteArray():
    with open("image_test.jpg", "rb") as image_file:
        imgByteArray = bytearray(image_file.read())
        print(bcolors.WARNING + "[image] done" + bcolors.ENDC)
    return imgByteArray


if __name__ == "__main__":
    print(bcolors.WARNING + "[main]" + bcolors.ENDC)
    MQTT_Thread = threading.Thread(target=NodeToServerMQTTThread, name="main_thread")
    MQTT_Thread.start()

    global flip
    flip = 0

    while True:
        loop()
