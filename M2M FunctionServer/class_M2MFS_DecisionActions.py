#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Nathaniel'

import time
import json
import copy
import sys
import class_M2MFS_MQTTManager
import class_M2MFS_Obj
# import M2MFunctionServer
from M2MRule import *
from terminalColor import bcolors
import M2MRule

class DecisionAction():
    def Judge(self, _obj_topic, _obj_json_msg):
        spreate_obj_json_msg = copy.copy(_obj_json_msg)

        ########## Control REQTOPICLIST ##########

        if (spreate_obj_json_msg["Control"] == "M2M_REQTOPICLIST"):
            print(bcolors.OKBLUE + "[DecisionActions] REQTOPICLIST TopicName: %s" % spreate_obj_json_msg[
                "Source"] + bcolors.ENDC)

            m2mfsmrules = FunctionServerMappingRules(_obj_topic, _obj_json_msg)
            time.sleep(1)
            m2mfsmrules.replyM2MTopicToNode(_obj_topic, spreate_obj_json_msg["Node"])


        elif (spreate_obj_json_msg["Control"] == "M2M_GETRULE"):
            m2mfsmrules = FunctionServerMappingRules()
            m2mfsmrules.replyM2MRulesAll("FS1")

        elif (spreate_obj_json_msg["Control"] == "M2M_ADDRULE"):
            m2mfsmrules = FunctionServerMappingRules()
            m2mfsmrules.AddM2MRule(spreate_obj_json_msg["Rules"])

        elif (spreate_obj_json_msg["Control"] == "M2M_UPDATERULE"):
            m2mfsmrules = FunctionServerMappingRules()
            m2mfsmrules.UpdateM2MRule(spreate_obj_json_msg["Rules"])

        elif (spreate_obj_json_msg["Control"] == "M2M_DELRULE"):
            m2mfsmrules = FunctionServerMappingRules()
            m2mfsmrules.DelM2MRule(spreate_obj_json_msg["Rules"])

        ########## 收到NodeLastWell異常斷線時，移除該Node在FS內的相關資料 ##########
        elif (spreate_obj_json_msg["Control"] == "LASTWILL"):
            print(bcolors.OKBLUE + "[DecisionActions] Remove exception disconnect Node: %s" %
                  spreate_obj_json_msg["Node"] + bcolors.ENDC)

            IsAlreadyREMOVE = False

            for p in M2MRule.nodePosList:
                if p.NodeName == spreate_obj_json_msg["Node"]:
                    M2MRule.nodePosList.remove(p)
                    IsAlreadyREMOVE = True
                    print(bcolors.OKGREEN + "[DecisionActions] Remove Node Success" + bcolors.ENDC)

            if ~IsAlreadyREMOVE:
                tempprint = "[DecisionActions] Remove Node NOT FOUND! nodePosList:"
                for p in nodePosList:
                    tempprint += p.NodeName + ", "
                print(bcolors.FAIL + tempprint + bcolors.ENDC)

        elif spreate_obj_json_msg["Control"] == "ID":
            m2fsidrules = FunctionServerIDRules()
            m2fsidrules.SaveGpsImage(spreate_obj_json_msg["GI"])

        elif spreate_obj_json_msg["Control"] == "IMG_REQUEST":
            m2fsidrules = FunctionServerIDRules()
            m2fsidrules.imgRequest(_obj_topic, spreate_obj_json_msg["Position"])

        else:
            print(bcolors.FAIL + "[DecisionActions] Receive message in wrong Control Signal! json:%s" % (
                spreate_obj_json_msg) + bcolors.ENDC)
