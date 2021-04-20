# -*- encoding=utf8 -*-
import platform
import sys
import wget
import json
from SettingInfo import *
from airtest.core.api import *
from Utils.Constant.ConstantVar import ConstantVar
from Utils.Tool.Mysql import Mysql
from Utils.Tool.SystemTool import SystemTool
from  run  import run
from GetDevices import ConnectATX


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
            self.TestAPKName = "dev_P2325_develop_F2_87899736_8d58eeec6_1abc8c97a_1ef41e0c4_0be918ffd_0a9e863.apk"  # APK title
            self.deviceCategory = ["Android"]  # Android或IOS
            self.environment = ["auto-test1Develop"]  # 环境    auto-test1Develop或auto-test2Release
        elif platform.system().lower() == "linux":  # 判断当前运行环境为linux时
            self.Commad=sys.argv  # 上传前解除注释
            self.TestAPKName = self.Commad[1] # 上传前解除注释   apk
            self.platform=[self.Commad[2]] # 上传前解除注释      测试平台
            self.environment=[self.Commad[3]] # 上传前解除注释   自动化运行环境
            self.language = self.Commad[4]  # 上传前解除注释   语种
            print(f"apk:{self.TestAPKName} 测试平台：{self.platform} 自动化运行环境：{self.environment} 语种：{self.language}")
            # self.TestAPKName = "dev_P2325_develop_F2_87899736_8d58eeec6_1abc8c97a_1ef41e0c4_0be918ffd_0a9e863.apk"   # 上传前注释
            # self.deviceCategory = ["Android"]   # 上传前注释
            # self.environment = ["test1Develop"]   # 上传前注释
        self.ConnectATX = ConnectATX()
        self.ConnectATX.getDevicesIP()
        self.InitDevList()
        self.WiertJson()
        Mysql.UpdateLanguagesConfiguration(self.language) # 更新语种配置表
        bool = Mysql.resetAccount(None, None, self.environment, None)  # 释放被征用账号
        if (bool == True):
            print(f"自动化运行环境：{self.environment} 账号释放成功" )

    def DownURL(self):

        """步骤2.开始Download APK文件"""
        BaseURL = None
        if(ConstantVar.Release in self.environment[0]): # 如果当前选中环境包含  “Release”
            BaseURL = "http://soft.f.xmfunny.com:8888/sausage/apk/先行/"
        elif((ConstantVar.Develop in self.environment[0])):# 如果当前选中环境包含  “Develop”
            BaseURL = "http://soft.f.xmfunny.com:8888/sausage/apk/开发/"
        config = SystemTool.readingIniConfiguration(os.path.join(SystemTool.getRootDirectory(),ConstantVar.EnvironmentConfig))  # 获取 环境配置.ini配置文件对象
        SystemTool.setOnRegionAndKey(config, os.path.join(SystemTool.getRootDirectory(),ConstantVar.EnvironmentConfig), ConstantVar.DataArea, ConstantVar.Environment, self.environment[0])  # 根据.ini文件的区域和key设置值    设置所选环境
        url=os.path.join(BaseURL,self.TestAPKName)
        return url

    def WiertJson(self):
        """
        步骤3.写入运行环境配置文件
        """
        PKG = None # 包
        jsonFile=os.path.join(outpath,"config.json")
        APKPath=os.path.join(outpath,self.TestAPKName)
        if (ConstantVar.Release in self.environment[0]):  # 如果当前选中环境包含  “Release”
            PKG = "com.sofunny.chickendinnerfirst"
        elif ((ConstantVar.Develop in self.environment[0])):  # 如果当前选中环境包含  “Develop”
            PKG = "com.sofunny.ChickenDEV"
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
        for dev in devices:
            try:
                connect_device("Android://127.0.0.1:5037/"+dev)
                print(dev,"链接成功！")
            except:
                print("ACK")
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







