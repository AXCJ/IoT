#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Nathaniel'

import IoTServer
import class_IoTSV_Obj
import class_IoTSV_MQTTManager
import json
from terminalColor import bcolors


class FunctionServerMappingRules():
    def replyFSTopicToNode(self, topicName, NodeObj):

        IsHaveFSToMapping = False

        for FS in IoTServer._globalFSList:
            for NodeFunction in NodeObj.NodeFunctions:

                if NodeFunction in FS.MappingNodes:

                    if not IsHaveFSToMapping:
                        #### ASSIGN TO M2M FS ####
                        self.FSIP = class_IoTSV_Obj.FSIPObj \
                            (NodeObj.NodeName, IoTServer._g_cst_IoTServerUUID)


                    ### else append FSPairs ###
                    self.FSIP.FSPairs.append([FS.FSName, FS.FSFunction, FS.IP, NodeFunction])

                    IsHaveFSToMapping = True

        if IsHaveFSToMapping == False:
            self.FSIP = class_IoTSV_Obj.FSIPObj \
                (NodeObj.NodeName, IoTServer._g_cst_IoTServerUUID)
            self.FSIP.FSPairs = [['x']]

        jsonstring = self.FSIP.to_JSON()

        print(bcolors.OKBLUE + "[Rules] ADDFSIP Send to topic:%s" % (topicName) + bcolors.ENDC)

        pm = class_IoTSV_MQTTManager.PublisherManager()

        pm.MQTT_PublishMessage(topicName, jsonstring)

    def replyFSTopicToMD(self, topicName):

        self.FSIP = class_IoTSV_Obj.FSIPObj \
            ("x", IoTServer._g_cst_IoTServerUUID)

        for FS in IoTServer._globalFSList:
            #### ASSIGN TO M2M FS ####
            self.FSIP.FSPairs.append([FS.FSName, FS.FSFunction, FS.IP, "x"])

        self.FSIP.Control = "MD_REPFS";
        jsonstring = self.FSIP.to_JSON()

        print(bcolors.OKBLUE + "[Rules] ADDFSIP Send to topic:%s" % (topicName) + bcolors.ENDC)

        pm = class_IoTSV_MQTTManager.PublisherManager()
        pm.MQTT_PublishMessage(topicName, jsonstring)
