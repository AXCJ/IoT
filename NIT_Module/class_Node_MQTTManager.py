#!/usr/bin/python
# -*- coding: utf-8 -*-

# 該篇程式主要用途在於註冊動作的模組化

__author__ = 'Nathaniel'
from threading import Thread
import paho.mqtt.client as mqtt
import sys
import json
import time
from terminalColor import bcolors

# 上層目錄
sys.path.append("..")
import config_ServerIPList

_g_cst_ToMQTTTopicServerIP = config_ServerIPList._g_cst_ToMQTTTopicServerIP
_g_cst_ToMQTTTopicServerPort = config_ServerIPList._g_cst_ToMQTTTopicServerPort


class SubscriberThreading(Thread):  # 宣告一Class，並在每次呼叫到時創建一個Thread，讓註冊後的通道能夠不間斷的接收在上面的信息
    global topicName

    def __init__(self, topicName, nodeUUID):  # 本位寫法，請注意Python中Address的部分，有些指定位置會在同一個地方
        Thread.__init__(self)
        self.topicName = topicName
        self.nodeUUID = nodeUUID
        self.callbackST

    def run(self):  # Use run to create Thread. Run是預設的Function
        subscriberManager = SubscriberManager(self.nodeUUID)

        # callback
        subscriberManager.callb = self.callbackST
        subscriberManager.subscribe(self.topicName)


class SubscriberManager():
    def __init__(self, nodeUUID, ):
        self.nodeUUID = nodeUUID
        self.callb = None

    def subscribe(self, topicName):
        self.topicName = topicName

        ########## MQTT Subscriber ##############
        # The callback for when the client receives a CONNACK response from the server.
        def on_connect(client, userdata, flags, rc):
            print(bcolors.WARNING + "[INFO] Connected MQTT Topic Server:" + self.topicName + " with result code " + str(
                rc) + bcolors.ENDC)
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            # print(type(self.topicName))
            client.subscribe(topicName)

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            print(bcolors.WARNING + "[INFO] MQTT message receive from Topic %s at %s :%s" % (
                msg.topic, time.asctime(time.localtime(time.time())), str(msg.payload)) + bcolors.ENDC)
            try:
                if (msg.payload != ""):
                    _obj_json_msg = json.loads(str(msg.payload, encoding="UTF-8"))

                    # from Simulator_Node import RxRouting
                    # RxRouting(_obj_json_msg)

                    # callback
                    self.callb(_obj_json_msg)


            except (NameError, TypeError, RuntimeError) as e:
                print(bcolors.FAIL + "[ERROR] Couldn't converte json to Objet! " + str(e) + bcolors.ENDC)

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        WILLMSG = {"Node": "%s" % self.nodeUUID, "Control": "LASTWILL",
                   "Source": "%s" % self.nodeUUID}
        WILLMSG_json = json.dumps(WILLMSG)
        client.will_set(topicName, WILLMSG_json, 2, False)
        client.connect(_g_cst_ToMQTTTopicServerIP, int(_g_cst_ToMQTTTopicServerPort), 60)
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        print(bcolors.WARNING + "[INFO] Subscribe TopicName:" + topicName + bcolors.ENDC)
        client.loop_forever()


class PublisherManager():
    def MQTT_PublishMessage(self, topicName, message):  # 傳送到指定的Topic上
        print(bcolors.WARNING + "[INFO] MQTT Publishing message to topic: %s, Message:%s" % (
            topicName, message) + bcolors.ENDC)
        mqttc = mqtt.Client("python_pub")
        mqttc.connect(config_ServerIPList._g_cst_ToMQTTTopicServerIP, int(
            config_ServerIPList._g_cst_ToMQTTTopicServerPort))
        mqttc.publish(topicName, message)
        mqttc.loop(2)
        mqttc.disconnect()
