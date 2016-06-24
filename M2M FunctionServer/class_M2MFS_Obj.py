#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Nathaniel'
import json
# import M2MFunctionServer

###############################################################

class JSON_REPTOPICLIST():
    ###因為是自訂類別，所以要用這種方式轉出
    ## http://stackoverflow.com/questions/3768895/python-how-to-make-a-class-json-serializable
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)  # , indent=4) 要indent在uncommit

    def __init__(self, _obj_g_cst_FSUUID = "FS1"):
        self.Source = _obj_g_cst_FSUUID
        self.Gateway = ""
        self.Control = "M2M_REPTOPICLIST"
        self.SubscribeTopics = []  # SubscribeTopicsObj


class SubscribeTopicsObj:
    def __init__(self):
        self.TopicName = ""
        self.Node = ""
        self.Target = ""
        self.TargetValueOverride = ""


###############################################################

class JSON_M2MRULE():
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)  # , indent=4) 要indent在uncommit

    def __init__(self):
        self.Source = M2MFunctionServer._g_cst_FSUUID
        self.Control = "M2M_REPRULE"
        self.Rules = []


class RuleObj:
    def __init__(self):
        self.RuleID = ""
        self.InputNode = ""
        self.InputIO = ""
        self.OutputNode = ""
        self.OutputIO = ""
        self.TargetValueOverride = ""


class IDObj:
    def __init__(self):
        self.Altitude = ""
        self.Longitude = ""
