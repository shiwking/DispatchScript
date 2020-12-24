import requests
import json
from SettingInfo import *
from Utils.Tool.SystemTool import SystemTool
class ConnectATX(object):
    def __init__(self):
        self.BaseURL="http://10.30.20.29:4000/"
        self.userid=userid
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
                self.idleTimeout(devUUID)
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
        if len(self.devIPList) == 0:
            print("设备数量为空,程序退出")
            import sys
            sys.exit(0)
        else:
            print("返回设备数量：", len(self.devIPList))
            return self.devIPList

    def releaseDevice(self):
        """释放设备"""
        print("开始释放设备")
        hearder = {
            'Cookie': self.userid,
        }
        URL = self.BaseURL + 'api/v1/user/devices/'
        json_data = SystemTool.readJson(DEVICEINFO) # 读取 deviceInfo.json
        for key,serialNo in json_data.items():
            Result=requests.delete(URL + serialNo, headers=hearder)
            if Result.json()['success']==True:
                print(serialNo,"ATX设备释放成功！")
            else:
                print(serialNo,"ATX设备释放失败！")

    def idleTimeout(self,udid):
        """
        占用设备，修改占用设备时间1000分钟
        """
        hearder = {
            'Cookie': self.userid,
        }
        URL = self.BaseURL + 'api/v1/user/devices'
        stu = {
                "udid": udid,
                "idleTimeout": 60000
            }
        testdata= json.dumps(stu)
        try:
            requests.post(URL,data=testdata,headers=hearder)

        except:
            print("设备时间修改失败，请关注~")

if __name__ == '__main__':
     CA=ConnectATX()
     CA.getDevicesIP()
     CA.releaseDevice()

