__author__ = 'Nathaniel'
import  threading
import  time
import json
from urllib.request import urlopen
import threading

import requests


#打印当前线程的名字
def z():
    print("线程名：　"+threading.current_thread().getName())


def fetchIoTNodeList():
    print("jsdsdddddddddddddddddddddddddd")

    try:
        url = "http://192.168.88.253:5000/nit/iotsv/api/nodes"
        response = requests.get(url)
        
        nodelist = json.loads(response.content.decode("utf-8"))
        print(str(nodelist))
    except Exception as e:
        print("eeeeeeeeeeeeeeee"+e)


fetchIoTNodeList()

# t1=threading.Thread(target=z,name="my")
# t1.start()
#t1.join()

