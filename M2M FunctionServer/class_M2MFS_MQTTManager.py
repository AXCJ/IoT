#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread

__author__ = 'Nathaniel'

import paho.mqtt.client as mqtt
import time
import json
import copy
import sys
import class_M2MFS_DecisionActions
from terminalColor import bcolors
import  M2MFunctionServer


# 上層目錄
sys.path.append("..")
import config_ServerIPList

_g_cst_ToMQTTTopicServerIP = config_ServerIPList._g_cst_ToMQTTTopicServerIP
_g_cst_ToMQTTTopicServerPort = config_ServerIPList._g_cst_ToMQTTTopicServerPort


class SubscriberThreading(Thread):
    global topicName

    def __init__(self, topicName):
        Thread.__init__(self)
        self.topicName = topicName

    def run(self):
        subscriberManager = SubscriberManager()
        subscriberManager.subscribe(self.topicName)


class SubscriberManager():
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
            client.subscribe(str(self.topicName))

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            print(bcolors.WARNING + "[INFO] MQTT message receive from Topic %s at %s :%s" % (
                msg.topic, time.asctime(time.localtime(time.time())), str(msg.payload)) + bcolors.ENDC)

            try:
                if(msg.payload!=""):
                    # print("[INFO] Receive from MQTT %s" % msg.payload)
                    _obj_json_msg = json.loads(str(msg.payload, encoding="UTF-8"))
                    if(_obj_json_msg["Source"] != M2MFunctionServer._g_cst_FSUUID):
                        class_M2MFS_DecisionActions.DecisionAction().Judge(_obj_json_msg)
            except (RuntimeError, TypeError, NameError) as e:
                print(bcolors.FAIL + "[ERROR] Couldn't converte json to Objet! Error Details:" + str(e) + bcolors.ENDC)

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(_g_cst_ToMQTTTopicServerIP, int(_g_cst_ToMQTTTopicServerPort), 60)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.

        print(bcolors.WARNING + "[INFO] Subscribe TopicName:" + self.topicName + bcolors.ENDC)
        client.loop_forever()



        ########### MQTT Publisher ##############


class PublisherManager():
    def MQTT_PublishMessage(self, topicName, message):
        print(bcolors.WARNING + "[INFO] MQTT Publishing message to topic: %s, Message:%s" % (
        topicName, message) + bcolors.ENDC)
        mqttc = mqtt.Client("python_pub")
        mqttc.connect(_g_cst_ToMQTTTopicServerIP, int(_g_cst_ToMQTTTopicServerPort))
        mqttc.publish(topicName, message)
        mqttc.loop(2)  # timeout 2sec
