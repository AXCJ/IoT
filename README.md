Last update:2016/05/10
Author: Nathaniel Chen, EMP Chen @ NCKU NEAT.
Email: ar801112usase@hotmail.com


# 程式的開頭MOTD是在 http://www.kammerl.de/ascii/AsciiSignature.php 網站做的，字體是banner3-D。
# 請記得執行前檢查config_ServerIPList.py內，MQTT broker的位置跟port是否正確。
# 如果有少甚麼套件，請不要問作者...問問pip或者萬能google，99.99%都有解，除非你不小心砍掉本專案的什麼檔案。
# 規則表(xxxRule.py)前面的List可以參考檔案內的註解做修改mapping.

**NIT設置系統流程**

**2016/05/10**

**環境設置：**

任何平台只要能run python3即可

1.  建議安裝PyCharm

2.  從git clone下來，匯入專案[*https://bitbucket.org/thkaw/2015-iot-neat-infrastructure*](https://bitbucket.org/thkaw/2015-iot-neat-infrastructure) (注意必須在dev branch)

3.  重要資料夾結構與運行順序：

    1.  檢查config\_ServerIPList.py內的broker位置，替換為你自己的MQTT BrokerIP(推薦使用Mosquitto)

    2.  IoTServer

        1.  運行IoTServer.py

    3.  M2M FunctionServer

        1.  運行M2MFunctionServer.py

        2.  規則可以在M2MRule.py上改(參考投影片)

    4.  Node

        1.  運行Simulator\_Node.py(可選)

        2.  運行Dummy\_Node.py(可選)

**模擬情境1(兩假NODE)：**

Simulator\_Node目前為NODE-01，不須做任何動作。將由M2M FunctionServer/dummy\_Node\_New.py進行觸發，注意dummy\_Node\_New.py不遵守完整流程，僅做假的trigger訊號發送至NODE-02/SW2，之後立即結束運行dummy\_Node\_New，欲再次trigger需重新執行。

![1.png](https://bitbucket.org/repo/k98B5y/images/3451377721-1.png)

先執行上面環境設置後，執行Simulator\_Node後，執行dummy\_Node\_New.py則可觀察到Simulator\_Node之terminal訊息：

![2.png](https://bitbucket.org/repo/k98B5y/images/908414715-2.png)
**模擬情境2(一假NODE+一真實NODE)：**

Simulator\_Node目前為NODE-01，其具有Switch的function，可於terminal鍵入”t” enter後，將會發送M2M訊息至TOPIC: NODE-01/SW1


```
#!python

{'TopicName': "NODE-01/SW1", 'Control': 'M2M\_SET', 'Source': "NODE-01", 'M2M\_Value': 1}
```


而你可以自己將Simulator\_Node複製到實體的RPI上，做一點程式上的改變，使其能夠註冊為NODE-03，並自動交由M2M FS分派對應的RULE，NODE-03則會自動依照M2M FunctionServer/M2MRule.py內的規則自動訂閱至NODE-01/SW1。而當NODE-01發送訊息時則可設定該NODE-03的狀況

可進行TRACE CODE NODE-03上的副程式M2M\_RxRouting (與Simulator\_Node同樣)

```
#!python


**def RxRouting**(self, \_obj\_json\_msg):
nit.M2M\_RxRouting(\_obj\_json\_msg)

**def M2M\_RxRouting**(self, objJsonMsg):
class\_Node\_MQTTManager.SubscriberThreading.callbackST = self.CallBackRxRouting
separation\_obj\_json\_msg = copy.copy(objJsonMsg)
**if** separation\_obj\_json\_msg\["Control"\] == "ADDFS": \# Recive control from IoT Server for Function Server Topic
**for** fp **in** separation\_obj\_json\_msg\["FSPairs"\]:
\# \["FS1", "M2M", "10.0.0.1", "IOs"\]
fspair = class\_Node\_Obj.FSPair(fp\[0\], fp\[1\], fp\[2\], fp\[3\])
**if** (fp\[1\] == "M2M"):
**try**:
ReqToFS = {"Node": "%s" % self.nodeUUID, "Control": "M2M\_REQTOPICLIST",
"Source": "%s" % self.nodeUUID}
Send\_json = json.dumps(ReqToFS)
publisher.MQTT\_PublishMessage(fp\[0\], Send\_json)
class\_Node\_MQTTManager.SubscriberThreading(fp\[0\], self.nodeUUID).start()
**except** (RuntimeError, TypeError, NameError) **as** e:
print(bcolors.FAIL + "\[ERROR\] Send Request for topic list error!" + str(e) + bcolors.ENDC)
**return
elif** separation\_obj\_json\_msg\["Control"\] == "M2M\_REPTOPICLIST":
**for** subTopic **in** separation\_obj\_json\_msg\["SubscribeTopics"\]:
RuleObj = class\_Node\_Obj.M2M\_RuleObj(subTopic\["TopicName"\], subTopic\["Target"\],
subTopic\["TargetValueOverride"\])
self.Rules.append(RuleObj)
class\_Node\_MQTTManager.SubscriberThreading(subTopic\["TopicName"\], self.nodeUUID).start()
**elif** separation\_obj\_json\_msg\["Control"\] == "M2M\_SET":
**for** rule **in** self.Rules:
**if** rule.TopicName == separation\_obj\_json\_msg\["TopicName"\]:
print(
bcolors.OKGREEN + "&gt;&gt;Trigger&lt;&lt; Rx SET Msg " + rule.Target + " " + rule.TargetValueOverride + bcolors.ENDC)
```


在最後面的Control去看要設置什麼樣的動作，這邊假設是M2M\_SET要進行TERMINAL的畫面顯示，可以將此程式碼片段改為其他欲進行的動作