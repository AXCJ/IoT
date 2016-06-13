__author__ = 'Nathaniel'
import class_M2MFS_MQTTManager
import time


def dummy_reg():
    publisherManager = class_M2MFS_MQTTManager.PublisherManager()
    time.sleep(.5)
    publisherManager.MQTT_PublishMessage("IOTSV/REG", '{"Device": "MD-01","Control":"MD_REQFS", "Source":"MD-01"}')

    time.sleep(.5)
    publisherManager.MQTT_PublishMessage("FS1", '{"Device": "P1","Control":"M2M_GETRULE", "Source":"MD-01"}')
    time.sleep(.5)
    publisherManager.MQTT_PublishMessage("FS1", '{"Control": "M2M_ADDRULE","Rules": '
                                                '[{"RuleID": "4","InputNode": "N1",'
                                                '"InputIO": "SW1","OutputNode": "N2",'
                                                '"OutputIO": "LED3","TargetValueOverride": "1"}], "Source":"MD-01"}')
    time.sleep(.5)
    publisherManager.MQTT_PublishMessage("FS1", '{"Device": "P1","Control":"M2M_GETRULE", "Source":"MD-01"}')

    time.sleep(.5)
    publisherManager.MQTT_PublishMessage("FS1", '{"Control": "M2M_UPDATERULE","Rules": [{"RuleID": "1", '
                                                '"InputNode": "N1", "InputIO": "SW1",'
                                                '"OutputNode": "N2","OutputIO": "LED3",'
                                                '"TargetValueOverride": "1"}], "Source":"MD-01"}')

    time.sleep(.5)
    publisherManager.MQTT_PublishMessage("FS1",
                                         '{"Control": "M2M_DELRULE","Rules": [{"RuleID": "2"}], "Source":"MD-01"}')

    time.sleep(.5)
    publisherManager.MQTT_PublishMessage("FS1", '{"Device": "P1","Control":"M2M_GETRULE", "Source":"MD-01"}')


def main():
    dummy_reg()


if __name__ == '__main__':
    main()
