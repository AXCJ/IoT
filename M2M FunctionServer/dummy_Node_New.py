__author__ = 'Nathaniel'
import class_M2MFS_MQTTManager
import threading
import json
import time
import uuid

_g_NodeUUID = uuid.uuid1()


def initREG():
    publisherManager = class_M2MFS_MQTTManager.PublisherManager()
    initMSGObj = {'TopicName': "NODE-02/SW2", 'Control': 'M2M_SET', 'Source': "NODE-02"}
    initMSGSTR = json.dumps(initMSGObj)
    now = time.strftime("%c")
    print(now)
    print("[INFO] SendREGMSG:%s" % initMSGSTR)
    publisherManager.MQTT_PublishMessage("NODE-02/SW2", initMSGSTR)


def main():
    initREG()


if __name__ == '__main__':
    main()
