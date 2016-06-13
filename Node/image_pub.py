import paho.mqtt.client as mqtt

#
# def on_publish(mosq, userdata, mid):
# mosq.disconnect()
#
# client = mqtt.Client()
# client.username_pw_set('user', 'password')
# client.> >> >
# client.connect("myvps.com", 1883, 60)
#
# f = open('1.jpg', 'rb')
# fileContent = f.read()
# byteArr = bytes(fileContent)
# client.publish("test", byteArr, 0)
#
# client.loop_forever()

import config_ServerIPList
from terminalColor import bcolors

_g_cst_ToMQTTTopicServerIP = config_ServerIPList._g_cst_ToMQTTTopicServerIP
_g_cst_ToMQTTTopicServerPort = config_ServerIPList._g_cst_ToMQTTTopicServerPort


# Define event callbacks
def on_connect(mosq, obj, rc):
    print("on_connect: " + str(rc))

def on_message(mosq, obj, msg):
    if msg.topic == 'image/jpg':
        client.disconnect()
    print("on_message: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mosq, obj, mid):
    print("on_publish: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)

def convertImageToBase():
    with open("image_test.jpg", "rb") as image_file:
        imgByte = bytearray(image_file.read())
        print(bcolors.WARNING + "[image] done" + bcolors.ENDC)
    return imgByte


client = mqtt.Client()
# Assign event callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe

# Connect
client.connect(_g_cst_ToMQTTTopicServerIP, int(_g_cst_ToMQTTTopicServerPort), 60)

# Start subscribe
client.subscribe("msg/hello")
client.subscribe("image/jpg")

# Publish a message
with open("image_test.jpg", "rb") as image_file:
    imgBytearray = bytearray(image_file.read())  # file.read() returns a bytes
    # print(bcolors.WARNING + "[image] " + str(imgBytearray) + bcolors.ENDC)

# print(isinstance(imgBytearray, bytearray))  # check if it is bytearray
# print(bcolors.WARNING + "[INFO] MQTT Publishing message to topic: %s, Message:%s" % (
#     "image/jpg", imgBytearray) + bcolors.ENDC)


print(client.publish("image/jpg", imgBytearray))
print(client.publish("msg/hello", "hello"))
# Continue the network loop, exit when an error occurs
rc = 0
# while rc == 0:
rc = client.loop_forever(20)
print("rc: " + str(rc))
