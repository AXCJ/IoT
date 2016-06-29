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
import class_Node_MQTTManager
import random
import base64
import uuid

NodeUUID = "CamGPS_NCKUMVLAB92823@NODE-" + str(uuid.uuid1())

is_request = False
CG = False
if CG:
    import picamera
    camera = picamera.PiCamera()
    camera.resolution = (150, 85)
    from gps3 import gps3
    gps_socket = gps3.GPSDSocket()
    gps_fix = gps3.Fix()
    gps_socket.connect()
    gps_socket.watch()

Functions = ["Image"]
NodeFunctions = ['Cam']  # ['Cam', 'GPS', 'CG']
NodePosition = 'Tiger'
FuncSVList = []
cameraIdx = 0



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


def PUBLISHER(FS, MSG):
    publisher = class_Node_MQTTManager.PublisherManager()
    publisher.MQTT_PublishMessage(FS, MSG)


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
    if fs is not None and fs not in FuncSVList:
        FuncSVList.append(fs)
        print(FuncSVList)
    if _obj_json_msg["Source"] == 'CG_NCKUMVLAB92823@FS-41d0b11e-3d3a-11e6-a655-3c07544f6d45':
        if _obj_json_msg["Control"] == "IMG_REQUEST":  # reply image if get img_request
            initMSGObj = {'TopicName': _obj_json_msg["Source"], 'Control': 'IMG_REPLY', 'Source': NodeUUID, 'Position': NodePosition}
            gpsData = ['25.033' + str(random.randint(1, 1000)), '121.564101']
            if CG:
                imgData = imageToBase64Str()
                for new_data in gps_socket:
                    if new_data:
                        gps_fix.refresh(new_data)
                        Latitude = gps_fix.TPV['lat']
                        Longitude = gps_fix.TPV['lon']
                        if (Latitude != "n/a" and Longitude != "n/a"):
                            # print('Latitude: ', gps_fix.TPV['time'])
                            gpsData = [Latitude, Longitude]
                            break
            else:
                imgData = imageToBase64Str(NodePosition)

            initMSGObj['GI'] = {'GPS': gpsData, "IMG": imgData}
            initMSGSTR = json.dumps(initMSGObj)  # 將對象轉json(JavaScript Object Notation)
            nit.DirectMSG(_obj_json_msg["Source"], initMSGSTR)  # Publish directly
            print(bcolors.WARNING + "[IMG] Sending image success!" + bcolors.ENDC)

    if is_request:
        if _obj_json_msg["Control"] == 'IMG_REPLY':
            if _obj_json_msg['GI'] != "":
                # file name = Lat_Lon.jpg
                fileName = time.strftime("%Y%m%d_%H %M %S") + '_' + _obj_json_msg['GI']['GPS'][0] + '_' + _obj_json_msg['GI']['GPS'][1] + '.jpg'
                dirPath = os.path.join(os.path.abspath(os.curdir) + '/' + time.strftime("%Y%m%d") + '/' + NodePosition + '/' + _obj_json_msg['Position'])  # save image into directory 'Image'
                if not os.path.exists(dirPath):
                    os.makedirs(dirPath)
                filePath = os.path.join(dirPath, fileName)
                with open(filePath, 'wb') as fw:
                    imgStr = _obj_json_msg['GI']['IMG'].encode('utf-8')  # str to bytes
                    img = base64.decodebytes(imgStr)  # base64 to binary
                    fw.write(img)
                    print(bcolors.WARNING + "[IMG] Save image success!" + bcolors.ENDC)



def imageToBase64Str(obj=''):
    try:
        if CG:
            imgName = "Capture" + str(cameraIdx) + ".jpg"
            dirPath = os.path.join(os.path.abspath(os.curdir) + '/' + 'CAMERA')
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
            f = os.path.join(dirPath, imgName)
            camera.capture(f)
        # time.sleep(1)
        else:
            f = obj + '.jpg'
        with open(f, "rb") as f_img:
            image = base64.encodebytes(f_img.read())  # binary to base64
            imgStr = image.decode('utf-8')  # bytes to str
            print(bcolors.WARNING + "[IMAGE] Open image success" + bcolors.ENDC)
        return imgStr
    except:
        raise CustomError(bcolors.FAIL + '[Err] File does not exist.' + bcolors.ENDC)


def loop():
    try:
        if not FuncSVList:
            raise CustomError(bcolors.FAIL + '[Err] No FunctionServer.' + bcolors.ENDC)
        else:
            decide = input("[Trig] Enter command e.g. 'img' to send image or 'r' to request img:\n       "
                           "Enter 'c' to toggle image saving switch:\n")
            if decide == "img":
                for FS in FuncSVList:
                    initMSGObj = {'TopicName': FS, 'Control': 'ID', 'Source': NodeUUID, 'Position': NodePosition}
                    if FS == "CG_NCKUMVLAB92823@FS-41d0b11e-3d3a-11e6-a655-3c07544f6d45":
                        gpsData = ['25.033' + str(random.randint(1, 1000)), '121.564101']
                        if CG:
                            imgData = imageToBase64Str()
                            for new_data in gps_socket:
                                if new_data:
                                    gps_fix.refresh(new_data)
                                    Latitude = gps_fix.TPV['lat']
                                    Longitude = gps_fix.TPV['lon']
                                    if (Latitude != "n/a" and Longitude != "n/a"):
                                        # print('Latitude: ', gps_fix.TPV['time'])
                                        gpsData = [Latitude, Longitude]
                                        break
                        else:
                            imgData = imageToBase64Str(input('[img] Enter image name for sending. (e.g. cat, view): '))

                        # initMSGObj["IMG"] = imageToBase64Str()  # In Python 3, they removed byte support in json
                        # initMSGObj['GPS'] = ['Latitude', 'Longitude']
                        initMSGObj['GI'] = {'GPS': gpsData,
                                            "IMG": imgData}
                        initMSGSTR = json.dumps(initMSGObj)  # 將對象轉json(JavaScript Object Notation)
                        nit.DirectMSG(FS, initMSGSTR)  # Publish directly
                        # threading.Thread(target=nit.DirectMSG(FS, initMSGSTR), name="pub_thread").start()
                        # print(bcolors.OKBLUE + '[Thread] active_count: ' + str(threading.active_count()) + bcolors.ENDC)
                        # print(bcolors.OKBLUE + '[Thread] threading.enumerate: ' + str(threading.enumerate()) + bcolors.ENDC)

            elif decide == "r":
                for FS in FuncSVList:
                    initMSGObj = {'TopicName': FS, 'Control': 'IMG_REQUEST', 'Source': str(NodeUUID),
                                  'Position': input('[Trig] Enter the position: ')}
                    initMSGSTR = json.dumps(initMSGObj)  # 將對象轉json(JavaScript Object Notation)
                    nit.DirectMSG(FS, initMSGSTR)

            elif decide == 'c':
                global is_request
                is_request = not is_request
                print('save image = %s' % is_request)
                # nit.DirectMSG('IOTSV/REG', '123456')


            else:
                print(bcolors.FAIL + '[Err] Please enter correct command.' + bcolors.ENDC)
    except CustomError as e:
        print(e)
        # pass



if __name__ == "__main__":
    MQTT_Thread = threading.Thread(target=NodeToServerMQTTThread, name="main_thread")
    MQTT_Thread.start()
    # for x in range(5):
    #     initMSGObj = {'TopicName': 'CG_NCKUMVLAB92823@FS-41d0b11e-3d3a-11e6-a655-3c07544f6d45', 'Control': 'NO', 'Source': NodeUUID, 'Position': NodePosition}
    #     imgData = imageToBase64Str('cat')
    #     initMSGObj['IMG'] = imgData
    #     print(bcolors.OKBLUE + '[Thread] active_count: ' + str(threading.active_count()) + bcolors.ENDC)
    #     print(bcolors.OKBLUE + '[Thread] threading.enumerate: ' + str(threading.enumerate()) + bcolors.ENDC)
    #     initMSGSTR = json.dumps(initMSGObj)  # 將對象轉json(JavaScript Object Notation)
    #     threading.Thread(
    #         target=PUBLISHER('CG_NCKUMVLAB92823@FS-41d0b11e-3d3a-11e6-a655-3c07544f6d45', initMSGSTR)).start()
    #     threading.Thread(
    #         target=PUBLISHER('CG_NCKUMVLAB92823@FS-41d0b11e-3d3a-11e6-a655-3c07544f6d45', initMSGSTR)).start()
    #     threading.Thread(
    #         target=PUBLISHER('CG_NCKUMVLAB92823@FS-41d0b11e-3d3a-11e6-a655-3c07544f6d45', initMSGSTR)).start()
    #     threading.Thread(
    #         target=PUBLISHER('CG_NCKUMVLAB92823@FS-41d0b11e-3d3a-11e6-a655-3c07544f6d45', initMSGSTR)).start()
    #     threading.Thread(
    #         target=PUBLISHER('CG_NCKUMVLAB92823@FS-41d0b11e-3d3a-11e6-a655-3c07544f6d45', initMSGSTR)).start()
    #     # PUBLISHER('CG_NCKUMVLAB92823@FS-41d0b11e-3d3a-11e6-a655-3c07544f6d45', initMSGSTR)
    #     print(bcolors.OKBLUE + '[Thread] active_count: ' + str(threading.active_count()) + bcolors.ENDC)
    #     print(bcolors.OKBLUE + '[Thread] threading.enumerate: ' + str(threading.enumerate()) + bcolors.ENDC)

    time.sleep(4)
    while True:
        time.sleep(0.1)
        loop()
