#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import threading
import time
import json
import uuid
import paho.mqtt.client as mqtt


import NIT_Node_Module
from terminalColor import bcolors

sys.path.append("..")
import config_ServerIPList


#NodeUUID = "NODE-01"
NodeUUID ="NODE-" +str(uuid.uuid1())

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





# Connect to MQTT Server for communication
def NodeToServerMQTTThread(nodeType):

    def RxRouting(self, _obj_json_msg):
        nit.M2M_RxRouting(_obj_json_msg)

    # print("thread name：　" + threading.current_thread().getName())

    # callback
    nit = NIT_Node_Module.NIT_Node(NodeUUID, Functions, NodeFunctions,nodeLBT=nodeType)
    nit.CallBackRxRouting = RxRouting
    print(bcolors.HEADER + '===============================================\n' + bcolors.ENDC)
    print(bcolors.HEADER + '---------------Node(%s)--->>>Server in MQTT-\n' % NodeUUID + bcolors.ENDC)
    print(bcolors.HEADER + '>>>Start connect Server %s<<<' % (
        time.asctime(time.localtime(time.time()))) + bcolors.ENDC)
    print(bcolors.HEADER + '===============================================\n' + bcolors.ENDC)
    print(bcolors.HEADER + 'Register to IoT Server successful! \n' + bcolors.ENDC)

    try:

        nit.RegisterNoode();

    except (RuntimeError, TypeError, NameError) as e:
        print(bcolors.FAIL + "[INFO]Register error." + str(e) + bcolors.ENDC)
        raise
        sys.exit(1)

    f = open("Testdata512B1.txt", mode='rb')
    # f = open("Testdata2.jpg", mode='rb')

    readData = bytearray(f.read())
    print("Test data size:" + str(sys.getsizeof(readData)) + "Bytes")


    sleeptime = 1.5

    if nodeType == "CType":
        sleeptime = 0.5

    if nodeType == "TEST":
        sleeptime = 3

    # mqttc = mqtt.Client("threading.current_thread().getName()")
    #
    # print(bcolors.WARNING + "[INFO] MQTT Publishing message to topic: %s" % (
    #     "BENCHMARKTOPIC") + bcolors.ENDC)
    #
    # mqttc.connect(config_ServerIPList._g_cst_ToMQTTTopicServerIP, int(
    #         config_ServerIPList._g_cst_ToMQTTTopicServerPort))


    while True:
        time.sleep(sleeptime)
        # mqttc.publish("BENCHMARKTOPIC", readData)
        # mqttc.loop_forever()
        nit.DirectMSG("BENCHMARKTOPIC", readData)





#
# global flip
# def loop():
#     global flip
#     decide = "g"
#     decide = input("enter 't' to trigger")
#     print(decide)
#
#     initMSGObj = {'TopicName': "NODE-01/SW1", 'Control': 'M2M_SET', 'Source': "NODE-01", 'M2M_Value': flip}
#     initMSGSTR = json.dumps(initMSGObj)
#
#     if (decide == "t"):
#         nit.DirectMSG("NODE-01/SW1", initMSGSTR)
#         print("SW01 SENT.")
#         flip = (~flip)


if __name__ == "__main__":

    for x in range(5):
        MQTT_Thread = threading.Thread(target=NodeToServerMQTTThread, name="main_thread_D_"+str(1), kwargs={'nodeType':"TEST"})
        MQTT_Thread.start()
        NodeUUID ="NODE-" +str(uuid.uuid1())
        time.sleep(0.05)



    # for x in range(5):
    #     MQTT_Thread = threading.Thread(target=NodeToServerMQTTThread, name="main_thread_D_"+str(x), kwargs={'nodeType':"DType"})
    #     MQTT_Thread.start()
    #     NodeUUID ="NODE-" +str(uuid.uuid1())
    #
    #     time.sleep(0.05)
    #
    # for x in range(5):
    #     MQTT_Thread = threading.Thread(target=NodeToServerMQTTThread, name="main_thread_C_"+str(x), kwargs={'nodeType':"CType"})
    #     MQTT_Thread.start()
    #     NodeUUID ="NODE-" +str(uuid.uuid1())
    #
    #     time.sleep(0.05)
    # global flip
    # flip = 0
    # while True:
    #     loop()
