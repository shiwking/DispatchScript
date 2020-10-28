import requests
import json
from Setting import *
class ConnectATX(object):
    def __init__(self):
        self.BaseURL="http://10.30.20.29:4000/"
        self.userid='user_id="2|1:0|10:1603520841|7:user_id|32:c2hpd2tpbmdAYW5vbnltb3VzLmNvbQ==|cc78f84418a6cb723a546d64b1145fc7bdf0f12294806e95deb91e1227aa46da"; Path=/; Domain=10.30.20.29; Expires=Fri, 23 Oct 2020 06:13:43 GMT;'
        self.DevUUIDList=[]
        self.devIPList=[]
        self.devInfo= {}

    def getDevicesIP(self):
        """获取未使用设备的IP地址和端口"""
        #初始化所有设备

        URL= self.BaseURL+'api/v1/devices'
        URL2 = self.BaseURL + 'api/v1/user/devices'
        hearder={
            'Cookie': self.userid,
        }
        r = requests.get(URL,headers=hearder)
        reprot=r.json()
        print(reprot)
        for  deviceinfo  in reprot['devices']:
            if deviceinfo['present']==True and deviceinfo['using']==False:
                devUUID=deviceinfo['udid']
                self.DevUUIDList.append(devUUID)
                stu={"udid":devUUID}
                devdata=json.dumps(stu)
                requests.post(URL2, headers=hearder,data=devdata) #使用该设备
                getUsingDevinfo=requests.get(URL2+'/'+devUUID, headers=hearder) #获取使用设备的UUID
                getDevideInfo = getUsingDevinfo.json()['device']["sources"]

                for devinfo in getDevideInfo.keys():
                    devip=getDevideInfo[devinfo]['remoteConnectAddress']
                    self.devIPList.append(devip)
                    self.devInfo[devip]=devUUID


        with open(DEVICEINFO, "w") as f:
            json.dump(self.devInfo, f)

        if   len(self.devIPList)==0:
            print("设备数量为空")
            return None
        else:
            print("返回设备数量：",len(self.devIPList))
            return self.devIPList

    def releaseDevice(self):
        """释放设备"""
        print("开始释放设备")
        hearder = {
            'Cookie': self.userid,
        }
        URL = self.BaseURL + 'api/v1/user/devices/'
        print(URL)
        for devUUID in self.DevUUIDList:
            Result=requests.delete(URL+devUUID, headers=hearder)
            if Result.json()['success']==True:
                print(devUUID,"ATX设备释放成功！")
            else:
                print(devUUID,"ATX设备释放失败！")


if __name__ == '__main__':
     CA=ConnectATX()
     CA.getDevicesIP()
     # CA.releaseDevice()

