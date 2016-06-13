#!/usr/bin/python
# -*- coding: utf-8 -*-

from websocket_server import WebsocketServer
from threading import Thread
import socket
#from gevent import Timeout
import time
import json
import copy
import sys
import paho.mqtt.client as mqtt

_g_cst_serverName = "SV1"

_g_cst_SVSocketServerIP = ''  # 不用特別指定的話就是接受所有INTERFACE的IP進入
_g_cst_SVSocketServerPort = 50005
_g_cst_MaxGatewayConnectionCount = 10
_g_cst_GatewayConnectionTimeOut = 1000  #non-blocking寫法，目前無用，不要un-commit這個數值所使用的程式碼段落

_g_cst_socketClientTimeout = 120 # 如果在指定的秒數之內，gw都沒有訊息，視為time out 120 second

_g_cst_webSocketServerIP = ''  # 不用特別指定的話就是接受所有INTERFACE的IP進入
_g_cst_webSocketServerPORT = 8009

_g_cst_ToMQTTTopicServerIP = "thkaw.no-ip.biz"
_g_cst_ToMQTTTopicServerPort = "1883"

_g_cst_MQTTTopicName = "NCKU/NEAT/TOPIC/01"


_g_cst_ToGWProtocalHaveMQTT = True
_g_cst_ToGWProtocalHaveSocket = False


_g_cst_GWRoute = [['GW1','GW2'],['GW2','GW1']] #GW1->GW2, GW2->GW1 可支援串接例如['GW1','GW2','GW3']代表GW1->GW2,3
_g_cst_DEVICERoute = [['D1','D2'],['D2','D1']]
_g_cst_WhichTypeToTransport ='REP'

print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
print(":'######::'########:'########::'##::::'##:'########:'########::")
print("'##... ##: ##.....:: ##.... ##: ##:::: ##: ##.....:: ##.... ##:")
print(" ##:::..:: ##::::::: ##:::: ##: ##:::: ##: ##::::::: ##:::: ##:")
print(". ######:: ######::: ########:: ##:::: ##: ######::: ########::")
print(":..... ##: ##...:::: ##.. ##:::. ##:: ##:: ##...:::: ##.. ##:::")
print("'##::: ##: ##::::::: ##::. ##:::. ## ##::: ##::::::: ##::. ##::")
print(". ######:: ########: ##:::. ##:::. ###:::: ########: ##:::. ##:")
print(":......:::........::..:::::..:::::...:::::........::..:::::..::")
print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n")

########### Normal Socket to Nodes ##############

_g_gatewayList = []

# listen to device socket connection
def serverSocketThread():
    devicePollingInterval = 1

    def clientServiceThread(client):

        gatewayInfo = []
        gatewayInfo.append(client)

        ClientRegisted = False

        while (True):
            time.sleep(devicePollingInterval)

            _str_recvMsg = None

            with Timeout(_g_cst_socketClientTimeout, False):
                try:
                    _str_recvMsg = client.recv(256)

                except socket.error as,message:
                    print("[ERROR] Socket error, disconnected this gateway. Error Message:%s" % message)
                    client.shutdown(2)    # 0 = done receiving, 1 = done sending, 2 = both
                    client.close()
                    for gwinfo in _g_gatewayList:
                        if gwinfo[1] == _obj_json_msg["Gateway"]:
                            print ("[INFO] Remove Gateway: %s" % gwinfo[1])
                            _g_gatewayList.remove(gwinfo)
                    return

                _str_decodeMsg = _str_recvMsg.decode('utf-8')

                print("[MESSAGE] Reciving message from [Gateway] at %s : \n >>> %s <<<" % (
                    time.asctime(time.localtime(time.time())), _str_recvMsg))

                try:
                    _obj_json_msg = json.loads(_str_recvMsg)

                    _obj_json_msg["Server"] = _g_cst_serverName

                    if not ClientRegisted:
                        gatewayInfo.append(_obj_json_msg["Gateway"])

                        # 將此GW加入GW清單中
                        _g_gatewayList.append(gatewayInfo)
                        print ("[REGISTE] Gateway %s" % gatewayInfo)
                        ClientRegisted = True
                    else:
                        RoutingGW(_obj_json_msg)

                except:
                    ClientRegisted = False
                    print("[ERROR] Couldn't converte json to Objet!")

            if _str_recvMsg is None:
                client.shutdown(2)    # 0 = done receiving, 1 = done sending, 2 = both
                client.close()
                print("[ERROR] Socket timeout, disconnected this gateway.")
                for gwinfo in _g_gatewayList:
                    if gwinfo[1] == _obj_json_msg["Gateway"]:
                        print ("[INFO] Remove Gateway: %s" % gwinfo[1])
                        _g_gatewayList.remove(gwinfo)
                return


    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print("[ERROR] %s\n" % msg[1])
        sys.exit(1)

    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse tcp
    serverSocket.bind((_g_cst_SVSocketServerIP, _g_cst_SVSocketServerPort))
    serverSocket.listen(_g_cst_MaxGatewayConnectionCount)
    # serverSocket.settimeout(_g_cst_GatewayConnectionTimeOut)

    print('===============================================\n')
    print('---------------Gateway->>>Server---------------\n')
    print('>>>Start listen Gateways %s<<<' % (time.asctime(time.localtime(time.time()))))
    print('===============================================\n')

    while True:
        (clientSocket, address) = serverSocket.accept()
        print("[INFO] Client Info: ", clientSocket, address)
        t = Thread(target=clientServiceThread, args=(clientSocket,))
        t.start()

def RoutingGW(_obj_json_msg):

    for gw_rule in _g_cst_GWRoute:

        start_gw = gw_rule[0]
        destination_gws = []
        for i in range(1,len(gw_rule),1):
            spreate_obj_json_msg = copy.copy(_obj_json_msg)
            #destination_gws.append(gw_rule[i])
            if(spreate_obj_json_msg["Gateway"] == start_gw):
                spreate_obj_json_msg["Gateway"] = gw_rule[i]
                #print spreate_obj_json_msg
                RoutingDEVICE(spreate_obj_json_msg)


def RoutingDEVICE(_obj_json_msg):

    for device_rule in _g_cst_DEVICERoute:

        start_device = device_rule[0]
        destination_devices = []
        for i in range(1,len(device_rule),1):
            spreate_obj_json_msg = copy.copy(_obj_json_msg)
            #destination_gws.append(gw_rule[i])
            if(spreate_obj_json_msg["Device"] == start_device):
                spreate_obj_json_msg["Device"] = device_rule[i]
                if(spreate_obj_json_msg["Control"] == _g_cst_WhichTypeToTransport):
                    spreate_obj_json_msg["Control"] = "SET" 

                    #需要customize, 先寫死
                    spreate_obj_json_msg["LED"] = spreate_obj_json_msg["Switch"]

                    spreate_obj_json_msg.pop("Switch", None)

                    RoutedSendToGW(spreate_obj_json_msg)
                 
def RoutedSendToGW(_obj_json_msg):

    isSendGatewaySuccess = False
    spreate_obj_json_msg = copy.copy(_obj_json_msg)

    #轉成文字
    _str_sendToGWJson = json.dumps(spreate_obj_json_msg)

    #MQTT SV->GW單向傳輸
    if(_g_cst_ToGWProtocalHaveMQTT):
        MQTT_PublishMessage(_str_sendToGWJson)

    if(_g_cst_ToGWProtocalHaveSocket):
        for gw_client in _g_gatewayList:

            if(gw_client[1]==spreate_obj_json_msg["Gateway"]):
                print "Ready to transport message is: %s" % _str_sendToGWJson

                try:
                    gw_client[0].send(_str_sendToGWJson)
                    isSendGatewaySuccess = True
                except:
                    print "[ERROR] send to gateway have some error!"
                    isSendGatewaySuccess = False

        if not isSendGatewaySuccess:
            print "Destination GW:%s didn't online" % spreate_obj_json_msg["Gateway"]


t = Thread(target=serverSocketThread, args=())
t.start()

_g_instructionBuffer = []

########### WebSocket to SV ##############

# Called for every client connecting (after handshake)
def new_client(client, server):
    print('===============================================')
    print('---------------Gateway->>>Server---------------\n')
    print(">>>New client connected and was given id %d, handler %s, address %s<<<" % (
        client['id'], client['handler'], client['address']))
    print('===============================================\n')

    # server.send_message_to_all("Hey all, a new client has joined us")
    server.send_message(client, "Hi webclient")


# Called for every client disconnecting
def client_left(client, server):
    print("[INFO] Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200] + '..'
    print("[INFO] Client(%d) said: %s" % (client['id'], message))
    _g_instructionBuffer.append(message)


#WebServer = WebsocketServer(_g_cst_webSocketServerPORT, _g_cst_webSocketServerIP)
#WebServer.set_fn_new_client(new_client)
#WebServer.set_fn_client_left(client_left)
#WebServer.set_fn_message_received(message_received)
#WebServer.run_forever()

########### MQTT to GW ##############

def MQTT_TEST():
    print ">>MQTT Publishing test<<"
    mqttc = mqtt.Client("python_pub")
    mqttc.connect(_g_cst_ToMQTTTopicServerIP, _g_cst_ToMQTTTopicServerPort)
    mqttc.publish(_g_cst_MQTTTopicName, "{\"Gateway\":\"GW1\",\"Device\":\"D1\",\"Control\":\"SET\",\"LED\":\"ON\"}")
    mqttc.loop(2)  #timeout 2sec

def MQTT_PublishMessage(message):
    print "[INFO] MQTT Publishing message to topic: %s, Message:%s" % (_g_cst_MQTTTopicName, message)
    mqttc = mqtt.Client("python_pub")
    mqttc.connect(_g_cst_ToMQTTTopicServerIP, _g_cst_ToMQTTTopicServerPort)
    mqttc.publish(_g_cst_MQTTTopicName,message)
    mqttc.loop(2)  #timeout 2sec