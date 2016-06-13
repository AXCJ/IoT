import paho.mqtt.client as mqtt
import time
import config_ServerIPList
from terminalColor import bcolors

_g_cst_ToMQTTTopicServerIP = config_ServerIPList._g_cst_ToMQTTTopicServerIP
_g_cst_ToMQTTTopicServerPort = config_ServerIPList._g_cst_ToMQTTTopicServerPort


# Define event callbacks
def on_connect(mosq, obj, rc):
    print("on_connect: " + str(rc))

def on_message(mosq, obj, msg):
    print(bcolors.WARNING + "[INFO] MQTT message receive from Topic %s at %s :%s" % (
        msg.topic, time.asctime(time.localtime(time.time())), str(msg.payload)) + bcolors.ENDC)
    # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    # print(isinstance(msg.payload, bytearray))
    # print(isinstance(msg.payload, bytes))
    # print(isinstance(msg.payload, str))

    if msg.topic == "image/jpg":  # check if it is bytearray
        with open('testing_pic_receiving.jpg', 'wb') as fw:
            fw.write(msg.payload)

    bytes(msg.payload)

def on_publish(mosq, obj, mid):
    print("on_publish: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)


client = mqtt.Client()
# Assign event callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe

# Connect
client.connect(_g_cst_ToMQTTTopicServerIP, int(_g_cst_ToMQTTTopicServerPort), 60)

# Start subscribe
print(client.subscribe("image/jpg"))
print(client.subscribe("msg/hello"))

# Publish a message
client.publish("msg/hello", 'testing message')

# Continue the network loop, exit when an error occurs
rc = 0
while rc == 0:
    rc = client.loop()
print("rc: " + str(rc))