#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Nathaniel'

import time
import json
import copy
import sys
import class_IoTSV_MQTTManager
import class_IoTSV_Obj
import IoTServer
import Rules
from terminalColor import bcolors


class DecisionAction():
    def __init__(self, callbackNodeAppend, callbackNodeRemove):
        self.callbackNodeAppend = callbackNodeAppend
        self.callbackNodeRemove = callbackNodeRemove

    def Judge(self, _obj_json_msg):
        spreate_obj_json_msg = copy.copy(_obj_json_msg)


        ########## Control NODE_REG ##########

        if (spreate_obj_json_msg["Control"] == "NODE_REG"):
            if (spreate_obj_json_msg["Node"].find("NODE") != -1):
                print(bcolors.OKBLUE + "[DecisionActions] Start subscriber TopicName: %s" %
                      spreate_obj_json_msg["Node"] + bcolors.ENDC)

                ## 防止重複註冊
                IsAlreadyREG = False

                for p in IoTServer._globalNodeList:
                    if (p.NodeName == spreate_obj_json_msg["Node"]): IsAlreadyREG = True

                if (not IsAlreadyREG):

                    nodeObj = class_IoTSV_Obj.NodeObj(
                        spreate_obj_json_msg["Node"],
                        spreate_obj_json_msg["NodeFunctions"],
                        spreate_obj_json_msg["Functions"],
                        spreate_obj_json_msg["NodeLBType"],
                        spreate_obj_json_msg["NodeMAC"])

                    IoTServer._globalNodeList.append(nodeObj)
                    self.callbackNodeAppend(dict(nodeObj))

                    tempprint = "[DecisionActions] REG GW From %s ,_globalNodeList:" % (nodeObj.NodeName)
                    for p in IoTServer._globalNodeList: tempprint += p.NodeName + ", "

                    print(bcolors.OKGREEN + tempprint + bcolors.ENDC)

                    class_IoTSV_MQTTManager.SubscriberThreading(spreate_obj_json_msg["Node"], self.callbackNodeAppend, self.callbackNodeRemove).start()

                    time.sleep(1)
                    fsmapping = Rules.FunctionServerMappingRules()
                    fsmapping.replyFSTopicToNode(spreate_obj_json_msg["Node"], nodeObj)
                else:
                    print(
                        bcolors.FAIL + "[DecisionActions] REG Node Fail!, due to this Node already REG!" + bcolors.ENDC)


        ########## Control FS_REG ##########
        elif (spreate_obj_json_msg["Control"] == "FS_REG"):
            # print(bcolors.OKBLUE + "[DecisionActions] Start subscriber TopicName: %s" %
            #       spreate_obj_json_msg["FunctionServer"] + bcolors.ENDC)

            ## 防止重複註冊
            FSIsAlreadyREG = False

            for p in IoTServer._globalFSList:
                if (p.FSName == spreate_obj_json_msg["FunctionServer"]): FSIsAlreadyREG = True

            if (not FSIsAlreadyREG):

                fsobj = class_IoTSV_Obj.FunctionServerObj(
                    spreate_obj_json_msg["FunctionServer"],
                    spreate_obj_json_msg["Function"],
                    spreate_obj_json_msg["FSIP"],
                    spreate_obj_json_msg["MappingNodes"]
                )

                IoTServer._globalFSList.append(fsobj)

                tempprint = "[DecisionActions] REG fs From %s ,_globalFSList:" % (fsobj.FSName)
                for p in IoTServer._globalFSList: tempprint += p.FSName + ", "

                print(bcolors.OKGREEN + tempprint + bcolors.ENDC)

                # class_MQTTManager.SubscriberThreading(spreate_obj_json_msg["FunctionServer"]).start()

            else:
                print(bcolors.FAIL + "[DecisionActions] REG FS Fail!, due to this FS already REG!" + bcolors.ENDC)

        #
        # ########## Control ADDNODE ##########
        #
        # elif (spreate_obj_json_msg["Control"] == "NODE_ADD"):
        #     print(bcolors.OKBLUE + "[DecisionActions] Start AddNode" + bcolors.ENDC)
        #     IsAddNode = False
        #     for nodeObj in IoTServer._globalNodeList:
        #         # print("Current nodeObj: "+ str(nodeObj) + " name:"+ str(nodeObj.Name))
        #         if (nodeObj.Name == spreate_obj_json_msg["Gateway"]):
        #             # print("in Current nodeObj: "+ str(nodeObj) + " name:"+ str(nodeObj.Name))
        #
        #             for node in spreate_obj_json_msg["Nodes"]:
        #                 nodeobj = class_IoTSV_Obj.NodeObj(node["Node"], node["NodeFunction"], node["Functions"])
        #                 # print("in nodeobj "+str(nodeobj))
        #                 nodeObj.Nodes.append(nodeobj)
        #                 print(
        #                     bcolors.OKGREEN + "[DecisionActions] ADDNODE From %s, NodeName is %s, NodeFunction is %s, Functions is %s" %
        #                     (nodeObj.Name, node["Node"], node["NodeFunction"], node["Functions"]) + bcolors.ENDC)
        #
        #                 # for g in nodeObj.Nodes:
        #                 #    print(g.Functions)
        #
        #             IsAddNode = True
        #
        #             fsmapping = Rules.FunctionServerMappingRules()
        #             fsmapping.replyFSTopicToGW(spreate_obj_json_msg["Gateway"], nodeObj.Nodes)
        #
        #     if (not IsAddNode):
        #         print(bcolors.FAIL + "[DecisionActions] ADDNODE Not found specific GW." + bcolors.ENDC)

        ########## Control DELNODE ##########

        elif (spreate_obj_json_msg["Control"] == "NODE_DEL"):
            IsDelNode = False
            for nodeObj in IoTServer._globalNodeList:
                if (nodeObj.NodeName == spreate_obj_json_msg["Node"]):
                    try:
                        print(bcolors.OKGREEN + "[DecisionActions] NODE remove %s" % (
                            nodeObj.NodeName) + bcolors.ENDC)
                        IoTServer._globalNodeList.remove(nodeObj)
                        self.callbackNodeRemove(dict(nodeObj))

                        IsDelNode = True
                    except:
                        pass

            if (not IsDelNode):
                print(bcolors.FAIL + "[DecisionActions] DEL NODE Not found." + bcolors.ENDC)

        ########## 收到NodeLastWell異常斷線時，移除該Node在IOTSV內的相關資料 ##########
        elif (spreate_obj_json_msg["Control"] == "LASTWILL"):
            print(bcolors.OKBLUE + "[DecisionActions] Remove exception disconnect GW: %s" %
                  spreate_obj_json_msg["Node"] + bcolors.ENDC)

            IsAlreadyREMOVE = False

            for p in IoTServer._globalNodeList:
                if (p.NodeName == spreate_obj_json_msg["Node"]):
                    IoTServer._globalNodeList.remove(p)
                    self.callbackNodeRemove(p)

                    #class_IoTSV_MQTTManager.SubscriberManager
                    IsAlreadyREMOVE = True
                    print(bcolors.OKGREEN + "[DecisionActions] Remove Node Success" + bcolors.ENDC)

            if (~IsAlreadyREMOVE):
                print(bcolors.FAIL + "[DecisionActions] Remove Node NOT FOUND!" + bcolors.ENDC)


        ############### Manage Device ###############
        #############################################
        ########## Control MANAGEDEVICEREG ##########
        #############################################

        elif (spreate_obj_json_msg["Control"] == "MD_REG"):
            print(bcolors.OKBLUE + "[DecisionActions] Start subscriber TopicName: %s" %
                  spreate_obj_json_msg["Device"] + bcolors.ENDC)

            ## 防止重複註冊
            IsAlreadyREG = False

            for p in IoTServer._globalMDList:
                if (p.Name == spreate_obj_json_msg["Device"]): IsAlreadyREG = True

            if (not IsAlreadyREG):

                manObj = class_IoTSV_Obj.ManageObj(spreate_obj_json_msg["Device"])
                IoTServer._globalMDList.append(manObj)

                tempprint = "[DecisionActions] REG MANAGEDEVICE From %s ,_globalMDList:" % (manObj.Name)
                for p in IoTServer._globalMDList: tempprint += p.Name + ", "

                print(bcolors.OKGREEN + tempprint + bcolors.ENDC)

                class_IoTSV_MQTTManager.SubscriberThreading(spreate_obj_json_msg["Device"]).start()

            else:
                print(
                    bcolors.FAIL + "[DecisionActions] REG MANAGEDEVICE Fail!, due to this MANAGEDEVICE already REG!" + bcolors.FAIL)

        ########## Control DEVICEREQFS ##########
        elif (spreate_obj_json_msg["Control"] == "MD_REQFS"):
            fsmapping = Rules.FunctionServerMappingRules()
            fsmapping.replyFSTopicToMD(spreate_obj_json_msg["Device"])


        else:
            print(bcolors.FAIL + "[DecisionActions] Receive message in wrong Control Signal! json:%s" % (
                spreate_obj_json_msg) + bcolors.ENDC)
