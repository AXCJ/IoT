__author__ = 'Nathaniel'
import  threading
import  time


#打印当前线程的名字
def z():
    print("线程名：　"+threading.current_thread().getName())



t1=threading.Thread(target=z,name="my")
t1.start()
#t1.join()

