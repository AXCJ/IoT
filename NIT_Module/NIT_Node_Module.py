import copy
import json

import class_Node_MQTTManager
import class_Node_Obj
from terminalColor import bcolors
from uuid import getnode as get_mac

publisher = class_Node_MQTTManager.PublisherManager()


class NIT_Node:
    def __init__(self, nodeUUID, functions, nodeFunctions, nodePosition=None, mqttRegTopicName="IOTSV/REG", nodeLBT="DType", nodeMAC="AA-BB-CC-DD-EE-FF"):
        self.nodeUUID = nodeUUID
        self.functions = functions
        self.mqttRegTopicName = mqttRegTopicName
        self.nodeFunctions = nodeFunctions
        self.Rules = []
        self.CallBackRxRouting = None
        self.nodeLBT = nodeLBT
        self.nodeMAC = nodeMAC
        self.pos = nodePosition



    def RegisterNoode(self):
        _cst_MQTTRegTopicName = "IOTSV/REG"  # GW一開始要和IoT_Server註冊，故需要傳送信息至指定的MQTT Channel
        initMSGObj = {'Node': self.nodeUUID, 'Control': 'NODE_REG', 'NodeFunctions': self.nodeFunctions,
                      'Functions': self.functions, 'Source': self.nodeUUID, 'NodeLBType':self.nodeLBT, 'NodeMAC':self.nodeMAC}
        initMSGSTR = json.dumps(initMSGObj)
        class_Node_MQTTManager.SubscriberThreading.callbackST = self.CallBackRxRouting
        class_Node_MQTTManager.SubscriberThreading(_cst_MQTTRegTopicName, self.nodeUUID).start()
        # 訂閱自身名稱的topic
        class_Node_MQTTManager.SubscriberThreading(self.nodeUUID, self.nodeUUID).start()

        publisher.MQTT_PublishMessage(self.mqttRegTopicName, initMSGSTR)

    def M2M_RxRouting(self, objJsonMsg):
        class_Node_MQTTManager.SubscriberThreading.callbackST = self.CallBackRxRouting
        separation_obj_json_msg = copy.copy(objJsonMsg)
        if separation_obj_json_msg["Control"] == "ADDFS":  # Recive control from IoT Server for Function Server Topic
            for fp in separation_obj_json_msg["FSPairs"]:

                if fp[0]!="x":
                    # ["FS1", "M2M", "10.0.0.1", "IOs"]
                    fspair = class_Node_Obj.FSPair(fp[0], fp[1], fp[2], fp[3])

                if (fp[1] == "M2M"):
                    try:
                        ReqToFS = {"Node": "%s" % self.nodeUUID, "Control": "M2M_REQTOPICLIST",
                                   "Source": "%s" % self.nodeUUID}
                        Send_json = json.dumps(ReqToFS)
                        publisher.MQTT_PublishMessage(fp[0], Send_json)
                        class_Node_MQTTManager.SubscriberThreading(fp[0], self.nodeUUID).start()
                    except (RuntimeError, TypeError, NameError) as e:
                        print(bcolors.FAIL + "[ERROR] Send Request for topic list error!" + str(e) + bcolors.ENDC)
                        return
                if (fp[1] == "M2F"):
                    try:
                        ReqToFS = {"Node": "%s" % self.nodeUUID, "Control": "M2M_REQTOPICLIST",
                                   "Source": "%s" % self.nodeUUID}

                        ReqToFS["Position"] = self.pos
                        Send_json = json.dumps(ReqToFS)
                        publisher.MQTT_PublishMessage(fp[0], Send_json)
                        class_Node_MQTTManager.SubscriberThreading(fp[0], self.nodeUUID).start()
                        return fspair.FSName
                    except (RuntimeError, TypeError, NameError) as e:
                        print(bcolors.FAIL + "[ERROR] Send Request for topic list error!" + str(e) + bcolors.ENDC)
                        return fspair.FSName
        elif separation_obj_json_msg["Control"] == "M2M_REPTOPICLIST":
            for subTopic in separation_obj_json_msg["SubscribeTopics"]:
                RuleObj = class_Node_Obj.M2M_RuleObj(subTopic["TopicName"], subTopic["Target"],
                                                     subTopic["TargetValueOverride"])

                self.Rules.append(RuleObj)
                class_Node_MQTTManager.SubscriberThreading(subTopic["TopicName"], self.nodeUUID).start()

        elif separation_obj_json_msg["Control"] == "M2M_SET":
            for rule in self.Rules:
                if rule.TopicName == separation_obj_json_msg["TopicName"]:
                    ####### You need custom something here #######
                    print(
                        bcolors.OKGREEN + ">>Trigger<< Rx SET Msg " + rule.Target + " " + rule.TargetValueOverride + bcolors.ENDC)

    def DirectMSG(self, topicName, msg):
        publisher.MQTT_PublishMessage(topicName, msg)


class CustomError(Exception):
    """Base class for other exceptions"""
    def __init__(self, msg):
        self.msg = msg
