__author__ = 'Nathaniel'
import class_M2MFS_MQTTManager
import time


def dummy_reg():
    publisherManager = class_M2MFS_MQTTManager.PublisherManager()

    time.sleep(.5)
    # publisherManager.MQTT_PublishMessage("FS1", '{"Gateway": "GW1","Control":"REQTOPICLIST"}')
    time.sleep(.5)
    publisherManager.MQTT_PublishMessage("FS1", '{"Gateway": "GW2","Control":"REQTOPICLIST"}')


def main():
    dummy_reg()


if __name__ == '__main__':
    main()
