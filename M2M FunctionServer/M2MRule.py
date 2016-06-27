#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Nathaniel'

import class_M2MFS_Obj
import class_M2MFS_MQTTManager
import json
import copy
from terminalColor import bcolors
import base64
import os
# import M2MFunctionServer

# RuleID, InputNode, InputNode, InputIO, OutputNode, OutputNode, OutputIO, TargetValueOverride
# _g_M2MRulesMappingList = [["1", "Node1", "N1", "SW1", "Node2", "N2", "LED3", "DEF"],
#                         ["2", "Node1", "N1", "SW1", "Node2", "N2", "LED4", "0"],
#                         ["3", "Node2", "N2", "SW2", "Node1", "N1", "LED2", "1"]]

_g_M2MRulesMappingList = [{"RuleID": "1", "InputNode": "NODE-01", "InputIO": "SW1",
                           "OutputNode": "NODE-02", "OutputIO": "LED3", "TargetValueOverride": "EQU"},

                          {"RuleID": "2", "InputNode": "NODE-01", "InputIO": "SW1",
                           "OutputNode": "NODE-02", "OutputIO": "LED4", "TargetValueOverride": "0"},

                          {"RuleID": "3", "InputNode": "NODE-02", "InputIO": "SW2",
                           "OutputNode": "NODE-01", "OutputIO": "LED2", "TargetValueOverride": "1"},

                          {"RuleID": "4", "InputNode": "NODE-01", "InputIO": "SW1",
                           "OutputNode": "NODE-03", "OutputIO": "LED1", "TargetValueOverride": "EQU"},

                          {"RuleID": "5", "InputNode": "NODE-03", "InputIO": "SW1",
                           "OutputNode": "NODE-01", "OutputIO": "LED1", "TargetValueOverride": "EQU"},

                          # CustomRuleFormat
                          {"RuleID": "6", "InputNode": "NODE", "InputIO": "",
                           "OutputNode": "NODE", "OutputIO": "IMG", "TargetValueOverride": ""},
                          ]
nodePosList = []

class FunctionServerMappingRules():
    def __init__(self, _obj_topic, _obj_msg):
        self.jsonObj = class_M2MFS_Obj.JSON_REPTOPICLIST(_obj_topic)
        self.msg = _obj_msg

        if self.msg.get("Position") is not None:
            NodePos = class_M2MFS_Obj.NodePosObj(self.msg["Node"], self.msg["Position"])  # () means initialization
            # self.NodePos.Node = self.msg["Node"]
            # self.NodePos.Position = self.msg["Node"]
            nodePosList.append(NodePos)  # save positions which can access
        # print(nodePosList)
        # print(self.NodePos.to_JSON())

    def replyM2MTopicToNode(self, topicName, NodeName):
        self.jsonObj.Gateway = NodeName
        IsNodeHaveM2MMappingRules = False
        readyToReplyTopics = []

        for SingleM2MMappingRule in _g_M2MRulesMappingList:

            if (SingleM2MMappingRule["OutputNode"] == NodeName):
                readyToReplyTopics.append(SingleM2MMappingRule)

        if (len(readyToReplyTopics) > 0):
            IsNodeHaveM2MMappingRules = True
            for SingleM2MMappingRule in readyToReplyTopics:
                #### ASSIGN TO M2M FS ####
                self.SubscribeTopics = class_M2MFS_Obj.SubscribeTopicsObj()
                self.SubscribeTopics.TopicName = SingleM2MMappingRule["InputNode"] + \
                                                 "/" + SingleM2MMappingRule["InputIO"]  # FS1
                self.SubscribeTopics.Node = SingleM2MMappingRule["OutputNode"]  # M2M
                self.SubscribeTopics.Target = SingleM2MMappingRule["OutputIO"]
                self.SubscribeTopics.TargetValueOverride = SingleM2MMappingRule["TargetValueOverride"]

                self.jsonObj.SubscribeTopics.append(self.SubscribeTopics)

        else:
            IsNodeHaveM2MMappingRules = False

        jsonstring = self.jsonObj.to_JSON()

        print(bcolors.OKBLUE + "[Rules] REPTOPICLIST Send to topic:%s" % (topicName) + bcolors.ENDC)

        pm = class_M2MFS_MQTTManager.PublisherManager()
        pm.MQTT_PublishMessage(topicName, jsonstring)

    def replyM2MRulesAll(self, topicName):
        self.jsonObj = class_M2MFS_Obj.JSON_M2MRULE()

        for SingleM2MMappingRule in _g_M2MRulesMappingList:
            self.Rule = class_M2MFS_Obj.RuleObj()
            self.Rule.RuleID = SingleM2MMappingRule["RuleID"]
            self.Rule.InputNode = SingleM2MMappingRule["InputNode"]
            self.Rule.InputIO = SingleM2MMappingRule["InputIO"]
            self.Rule.OutputNode = SingleM2MMappingRule["OutputNode"]
            self.Rule.OutputIO = SingleM2MMappingRule["OutputIO"]
            self.Rule.TargetValueOverride = SingleM2MMappingRule["TargetValueOverride"]
            self.jsonObj.Rules.append(self.Rule)

        jsonstring = self.jsonObj.to_JSON()

        print(bcolors.OKBLUE + "[Rules] REPRULE Send to topic:%s" % (topicName) + bcolors.ENDC)

        pm = class_M2MFS_MQTTManager.PublisherManager()
        pm.MQTT_PublishMessage(topicName, jsonstring)

    def AddM2MRule(self, RuleObjs):
        print(bcolors.OKBLUE + "[Rules] ADDRULE start %s" % (RuleObjs) + bcolors.ENDC)

        NotifyNodes = []

        for SingleM2MMappingRule in RuleObjs:
            NotifyNodes.append(SingleM2MMappingRule["OutputNode"])
            _g_M2MRulesMappingList.append(SingleM2MMappingRule)

        self.ModifyRePublishToNode(NotifyNodes)
        print(bcolors.OKGREEN + "[Rules] ADDRULE end!" + bcolors.ENDC)

    def UpdateM2MRule(self, RuleObjs):
        print(bcolors.OKBLUE + "[Rules] UPDATERULE start %s" % (RuleObjs) + bcolors.ENDC)

        NotifyNodes = []

        for SingleM2MMappingRule in RuleObjs:
            for updateRule in _g_M2MRulesMappingList:
                if (updateRule["RuleID"] == SingleM2MMappingRule["RuleID"]):
                    # 蠻怪的，陣列內dict變動，list內卻沒有跟著變??，只好砍掉重新加入
                    NotifyNodes.append(updateRule["OutputNode"])
                    _g_M2MRulesMappingList.remove(updateRule)
                    _g_M2MRulesMappingList.append(SingleM2MMappingRule.copy())
                    NotifyNodes.append(SingleM2MMappingRule["OutputNode"])

        self.ModifyRePublishToNode(NotifyNodes)
        print(bcolors.OKBLUE + "[Rules] UPDATERULE end!" + bcolors.ENDC)

    def DelM2MRule(self, RuleObjs):
        print(bcolors.OKBLUE + "[Rules] DELRULE start %s" % (RuleObjs) + bcolors.ENDC)

        NotifyNodes = []

        for SingleM2MMappingRule in RuleObjs:
            for delRule in _g_M2MRulesMappingList:
                if (delRule["RuleID"] == SingleM2MMappingRule["RuleID"]):
                    NotifyNodes.append(delRule["OutputNode"])
                    _g_M2MRulesMappingList.remove(delRule)

        self.ModifyRePublishToNode(NotifyNodes)
        print(bcolors.OKGREEN + "[Rules] DELRULE end!" + bcolors.ENDC)

    def ModifyRePublishToNode(self, NotifyNodes):
        print(bcolors.OKBLUE + "[Rules] Republish New M2M Rules for relate Node." + bcolors.ENDC)
        NotifyNodes = list(set(NotifyNodes))
        for Nodes in NotifyNodes:
            self.replyM2MRulesAll(Nodes)


class FunctionServerIDRules():
    def __init__(self):
        self.IDObj = class_M2MFS_Obj.IDObj()

    def SaveGpsImage(self, MsgObj):
        if Obj_Msg['GPS'] != "":
            self.IDObj.Latitude = MsgObj['GPS'][0]
            self.IDObj.Longitude = MsgObj['GPS'][1]
            print('GPS_Latitude: ', self.IDObj.Latitude, 'GPS_Longitude: ' + str(self.IDObj.Longitude))

        if MsgObj['IMG'] != "":
            fileName = str(self.IDObj.Latitude) + '_' + str(self.IDObj.Longitude) + '.jpg'  # file name = Lat_Lon
            dirPath = os.path.join(os.path.abspath(os.curdir), 'Image')  # save image into directory 'Image'
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
            filePath = os.path.join(dirPath, fileName)
            with open(filePath, 'wb') as fw:
                imgStr = MsgObj['IMG'].encode('utf-8')  # str to bytes
                img = base64.decodebytes(imgStr)  # base64 to binary
                fw.write(img)
                print(bcolors.WARNING + "[IMG] Save image success!" + bcolors.ENDC)

    def aaabbb(self, _obj_FSUUID, _ReqObj):
        self.FSUUID = _obj_FSUUID

        if nodePosList is not None:
            readyToRequestTopics = []
            for singlenodePos in nodePosList:
                if (singlenodePos.NodePosition == _ReqObj):
                    readyToRequestTopics.append(singlenodePos.NodeName)
        print(readyToRequestTopics)
        if (len(readyToRequestTopics) > 0):
            for singleTopicName in readyToRequestTopics:
                self.RequestTopics = class_M2MFS_Obj.JSON_IMGREQUEST(self.FSUUID)
                jsonstring = self.RequestTopics.to_JSON()
                pm = class_M2MFS_MQTTManager.PublisherManager()
                pm.MQTT_PublishMessage(singleTopicName, jsonstring)
                print(bcolors.OKBLUE + "[Rules] IMG_REQUEST Send to topic:%s" % (self.FSUUID) + bcolors.ENDC)
