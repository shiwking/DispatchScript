import sys
from  run  import run
from GetDevices import ConnectATX
import os
import wget
import json


"""步骤1，读取Jenkins调度时传入的参数"""
print("步骤1.开始解析Jenkins参数")
Commad = sys.argv
TestAPKName = Commad[1]
platform = [Commad[2]]
environment = [Commad[3]]


"""步骤2.开始Download APK文件"""
print("步骤2.开始DownLoad APK文件")
outpath = "/DownloadAPK"
# outpath = "D:\\"
def WgetAPK(environment,TestAPKName):
    """下载APK"""
    if environment[0] =="Develop":
        BaseURL="http://soft.f.xmfunny.com:8888/sausage/apk/开发/"
    else:
        BaseURL = "http://soft.f.xmfunny.com:8888/sausage/apk/先行/"
    url=os.path.join(BaseURL,TestAPKName)
    wget.download(url,out=outpath)
WgetAPK(environment,TestAPKName)


"""步骤3.APK下载成功后，开始执行安装"""
print("步骤3.开始载入配置文件....")
def WiertJson():
    jsonFile=os.path.join(outpath,"config.json")
    APKPath=os.path.join(outpath,TestAPKName)
    if environment[0] == "Develop":
        PKG = "com.sofunny.ChickenDEV"
    else:
        PKG = "com.sofunny.chickendinnerfirst"
    new_dict={
        "APKPath":APKPath,
        "PKG":PKG
    }
    json_str = json.dumps(new_dict)
    new_dict = json.loads(json_str)
    with open(jsonFile, "w") as f:
        json.dump(new_dict, f)
    print("配置文件载入完成....")
WiertJson()

"""步骤4.开始执行安装...."""
print("步骤4.开始执行安装....")
ConnectATX = ConnectATX()
devices = ConnectATX.getDevicesIP()
air = 'installPKG.air'
run(devices, air, run_all=True)
print("设备安装完成.....")


"""步骤5.安装成功，开始释放设备。"""
print("步骤5.开始释放设备....清理APK文件...")
ConnectATX.releaseDevice()
APKPath = os.path.join(outpath, TestAPKName)
if os.path.exists(APKPath):
    os.remove(APKPath)
    print("文件删除成功")
from  time import sleep
sleep(10)
