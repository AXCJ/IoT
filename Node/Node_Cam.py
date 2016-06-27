#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import threading
import time
import json
import os
sys.path.append(os.path.split(os.getcwd())[0])
sys.path.append(os.path.join(os.path.split(os.getcwd())[0], 'NIT_Module'))
import NIT_Node_Module
sys.path.append("..")
from terminalColor import bcolors
import random
import base64

NodeUUID = "NODE-Cam" + str(random.randint(1, 1000))
# NodeUUID ="NODE-" +uuid.uuid1()

Functions = ["Image"]
NodeFunctions = ['Cam']  # ['Cam', 'GPS', 'CG']
NodePosition = 'Tiger'
FuncSVList = []
global is_request
is_request = False

print("::::::::::::::::::::::::::::::::::::::::::")
print("::::::::::::::::::::::::::::::::::::::::::")
print("'##::: ##::'#######::'########::'########:")
print(" ###:: ##:'##.... ##: ##.... ##: ##.....::")
print(" ####: ##: ##:::: ##: ##:::: ##: ##:::::::")
print(" ## ## ##: ##:::: ##: ##:::: ##: ######:::")
print(" ##. ####: ##:::: ##: ##:::: ##: ##...::::")
print(" ##:. ###: ##:::: ##: ##:::: ##: ##:::::::")
print(" ##::. ##:. #######:: ########:: ########:")
print("..::::..:::.......:::........:::........::")
print("::::::::::::::::::::::::::::::::::::::::::\n")

nit = NIT_Node_Module.NIT_Node(NodeUUID, Functions, NodeFunctions, NodePosition)


class CustomError(Exception):
    """Base class for other exceptions"""
    def __init__(self, msg='err'):
        self.msg = msg


# Connect to MQTT Server for communication
def NodeToServerMQTTThread():
    # print("thread name：　" + threading.current_thread().getName())

    # callback
    nit.CallBackRxRouting = RxRouting
    print(bcolors.HEADER + '===============================================\n' + bcolors.ENDC)
    print(bcolors.HEADER + '---------------Node(%s)--->>>Server in MQTT-\n' % NodeUUID + bcolors.ENDC)
    print(bcolors.HEADER + '>>>Start connect Server %s<<<' % (
        time.asctime(time.localtime(time.time()))) + bcolors.ENDC)
    print(bcolors.HEADER + '===============================================\n' + bcolors.ENDC)
    print(bcolors.HEADER + 'Register to IoT Server successful! \n' + bcolors.ENDC)

    try:
        nit.RegisterNoode()  # 向IoT_Server註冊 TopicName = "IOTSV/REG" , 'Control': 'NODE_REG'

    except (RuntimeError, TypeError, NameError) as e:
        print(bcolors.FAIL + "[INFO]Register error." + str(e) + bcolors.ENDC)
        raise
        sys.exit(1)


########### Keyboard interactive ##############
def RxRouting(self, _obj_json_msg):  # 收到訊息會執行這個，可在這邊新增功能
    fs = nit.M2M_RxRouting(_obj_json_msg)
    global is_request
    if fs is not None:
        FuncSVList.append(fs)

    if _obj_json_msg["Source"] == 'FS_Pic':
        if _obj_json_msg["Control"] == "IMG_REQUEST":  # reply image if get img_request
            initMSGObj = {'TopicName': _obj_json_msg["Source"], 'Control': 'IMG_REPLY', 'Source': str(NodeUUID)}
            initMSGObj['GI'] = {'GPS': ['25.033' + str(random.randint(1, 1000)), '121.564101'],
                                "IMG": imageToBase64Str(NodePosition)}
            initMSGSTR = json.dumps(initMSGObj)  # 將對象轉json(JavaScript Object Notation)
            # nit.DirectMSG(FS, initMSGSTR)  # Publish directly
            threading.Thread(target=nit.DirectMSG(_obj_json_msg["Source"], initMSGSTR), name="pub_thread").start()

    if is_request:
        if _obj_json_msg["Control"] == 'IMG_REPLY':
            if _obj_json_msg['GI'] != "":
                fileName = _obj_json_msg['GI']['GPS'][0] + '_' + _obj_json_msg['GI']['GPS'][1] + '.jpg'  # file name = Lat_Lon
                dirPath = os.path.join(os.path.abspath(os.curdir), 'Image')  # save image into directory 'Image'
                if not os.path.exists(dirPath):
                    os.makedirs(dirPath)
                filePath = os.path.join(dirPath, fileName)
                with open(filePath, 'wb') as fw:
                    imgStr = _obj_json_msg['GI']['IMG'].encode('utf-8')  # str to bytes
                    img = base64.decodebytes(imgStr)  # base64 to binary
                    fw.write(img)
                    print(bcolors.WARNING + "[IMG] Save image success!" + bcolors.ENDC)



def imageToBase64Str(obj):
    try:
        with open(obj + ".jpg", "rb") as f_img:
            image = base64.encodebytes(f_img.read())  # binary to base64
            imgStr = image.decode('utf-8')  # bytes to str
            print(bcolors.WARNING + "[IMAGE] Success" + bcolors.ENDC)
        return imgStr
    except:
        raise CustomError(bcolors.FAIL + '[Err] File does not exist.' + bcolors.ENDC)


def loop():
    try:
        if not FuncSVList:
            raise CustomError(bcolors.FAIL + '[Err] No FunctionServer.' + bcolors.ENDC)
        else:
            decide = input("[Trig] Enter command e.g. 'img' to send image or 'r' to request img:\n       Enter 'c' to toggle image saveing witch:\n")
            if decide == "img":
                for FS in FuncSVList:
                    initMSGObj = {'TopicName': FS, 'Control': 'ID', 'Source': str(NodeUUID)}

                    if FS == "FS_Pic":
                        # initMSGObj["IMG"] = imageToBase64Str()  # In Python 3, they removed byte support in json
                        # initMSGObj['GPS'] = ['latitude', 'longitude']
                        initMSGObj['GI'] = {'GPS': ['25.033493', '121.564101'],
                                            "IMG": imageToBase64Str(input('[img] Enter image name for sending. (e.g. cat, view): '))}
                        initMSGSTR = json.dumps(initMSGObj)  # 將對象轉json(JavaScript Object Notation)
                        # nit.DirectMSG(FS, initMSGSTR)  # Publish directly
                        threading.Thread(target=nit.DirectMSG(FS, initMSGSTR), name="pub_thread").start()
                        # print(bcolors.OKBLUE + '[Thread] active_count: ' + str(threading.active_count()) + bcolors.ENDC)
                        # print(bcolors.OKBLUE + '[Thread] threading.enumerate: ' + str(threading.enumerate()) + bcolors.ENDC)

            elif decide == "r":
                for FS in FuncSVList:
                    initMSGObj = {'TopicName': FS, 'Control': 'IMG_REQUEST', 'Source': str(NodeUUID), 'Position': input('[Trig] Enter the position: ')}
                    initMSGSTR = json.dumps(initMSGObj)  # 將對象轉json(JavaScript Object Notation)
                    nit.DirectMSG(FS, initMSGSTR)

            elif decide == 'c':
                global is_request
                is_request = not is_request


            else:
                print(bcolors.FAIL + '[Err] Please enter correct command.' + bcolors.ENDC)
    except CustomError as e:
        print(e)



if __name__ == "__main__":
    MQTT_Thread = threading.Thread(target=NodeToServerMQTTThread, name="main_thread")
    MQTT_Thread.start()
    time.sleep(4)
    while True:
        time.sleep(0.1)
        loop()
