#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Nathaniel'
import json
import IoTServer


###############################################################

class NodeObj():
    def __init__(self, NodeName, NodeFunctions, Functions):
        self.NodeName = NodeName
        self.NodeFunctions = NodeFunctions
        self.Functions = Functions


class FunctionServerObj():
    global Function

    def __init__(self, FSName, FSFunction, IP, MappingNodes):
        self.FSName = FSName
        self.FSFunction = FSFunction
        self.IP = IP
        self.MappingNodes = MappingNodes


###############################################################

class ManageObj():
    def __init__(self, MANAGEName):
        self.Name = MANAGEName


###############################################################

class JSON_ADDFSIP():
    ###因為是自訂類別，所以要用這種方式轉出
    ## http://stackoverflow.com/questions/3768895/python-how-to-make-a-class-json-serializable
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)  # , indent=4) 要indent在uncommit

    def __init__(self):
        self.Source = IoTServer._g_cst_IoTServerUUID
        self.Control = "ADDFSIP"
        self.FSIPs = []  # 放FSIPObj


class FSIPObj:
    def __init__(self, REPNodeName, SOURCE):
        self.Node = REPNodeName
        self.Control = "ADDFS"

        # FS.FSName, FS.FSFunction, FS.IP, NodeFunctions
        self.FSPairs = []
        self.Source = SOURCE

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)  # , indent=4) 要indent在uncommit

###############################################################
