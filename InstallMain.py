# -*- encoding=utf8 -*-
import platform
import sys

from airtest.core.api import connect_device

from  run  import run
from GetDevices import ConnectATX
import wget
import json
from SettingInfo import *



class  InstallPKG(object):
    def __init__(self):
        """
        初始化Jenkins参数
        TestAPKName： 测试APK包名称
        platform ：测试环境
        environment：测试平台
        getDevicesIP ：获取当前可用设备IP ，写入JsonFile
        """
        if platform.system().lower() == "windows":  # 判断当前运行环境为windows时
            self.TestAPKName = "first-test_P459_release_v32_0.32.1-1001_F2_27b158c7_e262f0fa7_26b96d031_d41bb5364_7b6db728_89dbfa1.apk"  # APK title
            self.deviceCategory = ["Android"]  # Android或IOS
            self.environment = ["Release"]  # 环境    Release或Develop
        elif platform.system().lower() == "linux":  # 判断当前运行环境为linux时
            # self.Commad=sys.argv  # 上传前解除注释
            # self.TestAPKName = self.Commad[1] # 上传前解除注释
            # self.platform=[self.Commad[2]] # 上传前解除注释
            # self.environment=[self.Commad[3]] # 上传前解除注释
            self.TestAPKName = "first-test_P459_release_v32_0.32.1-1001_F2_27b158c7_e262f0fa7_26b96d031_d41bb5364_7b6db728_89dbfa1.apk"   # 上传前注释
            self.deviceCategory = ["Android"]   # 上传前注释
            self.environment = ["Release"]   # 上传前注释
        self.ConnectATX = ConnectATX()
        self.ConnectATX.getDevicesIP()
        self.InitDevList()
        self.WiertJson()

    def DownURL(self):

        """步骤2.开始Download APK文件"""
        if self.environment[0] =="Develop":
            BaseURL="http://soft.f.xmfunny.com:8888/sausage/apk/开发/"
        else:
            BaseURL = "http://soft.f.xmfunny.com:8888/sausage/apk/先行/"
        url=os.path.join(BaseURL,self.TestAPKName)
        return url

    def WiertJson(self):
        """
        步骤3.写入运行环境配置文件
        """
        jsonFile=os.path.join(outpath,"config.json")
        APKPath=os.path.join(outpath,self.TestAPKName)
        if self.environment[0] == "Develop":
            PKG = "com.sofunny.ChickenDEV"
        else:
            PKG = "com.sofunny.chickendinnerfirst"
        new_dict={
            "APKPath":APKPath,
            "PKG":PKG,
            "downloadPath":self.DownURL()
        }
        json_str = json.dumps(new_dict,ensure_ascii=False)
        new_dict = json.loads(json_str)
        with open(jsonFile, "w",encoding='utf-8') as f:
            json.dump(new_dict, f)
        print("配置文件载入完成....")


    def Devinfo(self):
        """
        获取设备IP列表
        """
        with open(DEVICEINFO,encoding='utf8') as f:
            json_data = json.load(f)
            DevIpList=list(json_data.keys())
            return DevIpList

    def GoInstallAPK(self):
        """
        执行安装APK
        """
        air = 'installPKG.air'
        devices =None
        if platform.system().lower() == "windows":  # 判断当前运行环境为windows时
            connect_device("Android://127.0.0.1:5037/7056efbb") # 10.40.7.104:5555  7056efbb
            devices=["7056efbb"]
        elif platform.system().lower() == "linux":  # 判断当前运行环境为linux时
            devices=self.Devinfo()
        run(devices, air, run_all=True)

    def remoAPK(self):
        """删除APK"""
        APKPath = os.path.join(outpath, self.TestAPKName)
        if os.path.exists(APKPath):
            os.remove(APKPath)
            print("文件删除成功")

    def InitDevList(self):
        """
        初始化可用设备列表
        """
        SuccessfulDev = {}
        with open(SuccessfulDevices, "w", encoding="utf-8") as f:
            json.dump(SuccessfulDev, f)

if __name__ == '__main__':

    InstallPKG=InstallPKG()
    #下载文件
    wget.download(InstallPKG.DownURL(),out=outpath)
    #开始安装
    InstallPKG.GoInstallAPK()
    #安装完成后移除文件APL
    InstallPKG.remoAPK()







