import requests
from Setting import *
import json
class ConnectATX(object):
    def __init__(self):
        self.BaseURL=ATXSERVER
        self.userid='user_id="2|1:0|10:1600841623|7:user_id|32:c2hpd2tpbmdAYW5vbnltb3VzLmNvbQ==|142b8bf618d52712b74812e1b00b9b0f24f3a5a12c95457fe98f0878511d8156"; Path=/; Domain=10.30.20.29; Expires=Fri, 23 Oct 2020 06:13:43 GMT;'
        self.DevUUIDList=[]
        self.devIPList=[]

    def getDevicesIP(self):
        """获取未使用设备的IP地址和端口"""
        URL= self.BaseURL+'api/v1/devices'
        URL2 = self.BaseURL + 'api/v1/user/devices'
        hearder={
            'Cookie': self.userid,
        }

        r = requests.get(URL,headers=hearder)
        reprot=r.json()
        for  deviceinfo  in reprot['devices']:
            print(deviceinfo)
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

        if   len(self.devIPList)==0:
            print("设备数量为空")
            return None
        else:
            print("返回设备数量：",len(self.devIPList))
            return self.devIPList

    def releaseDevice(self):
        """释放设备"""
        print(self.DevUUIDList)
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
     # print(CA.getDevicesIP())
     CA.releaseDevice()
