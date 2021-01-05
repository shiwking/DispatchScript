__author__ = "shiwking"
# 安装包
import os
import sys



rootpath = str("/" + os.path.join("var", "jenkins_home","DispatchScript"))
syspath = sys.path
# sys.path = []
sys.path.append(rootpath)  # 将工程根目录加入到python搜索路径中
sys.path.extend([rootpath + i for i in os.listdir(rootpath) if i[0] != "."])  # 将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)
import json
import requests
from airtest.core.api import *
from poco.drivers.unity3d import UnityPoco
from SettingInfo import *
from Utils.Tool.SystemTool import SystemTool
from Utils.Constant.ConstantVar import ConstantVar

auto_setup(__file__)
PWD = os.path.dirname(__file__)
sys.path.append(rootpath)
from SettingInfo import *
# init_device(platform="Android", uuid=deviceID) # 初始化设备
#connect_device("Android://127.0.0.1:5037/" + deviceID)  # 连接设备 10.40.7.104:5555  7056efbb
with open("/DownloadAPK/config.json",'r',encoding='utf-8')as fp:
    json_data = json.load(fp)
PKG = json_data["PKG"]
APK = json_data["APKPath"]
downloadPath=json_data["downloadPath"]
print(downloadPath)
# windows端调试时解开
#connect_device("Android://127.0.0.1:5037/10.40.7.104:5555") # 10.40.7.104:5555  7056efbb
# PKG = "com.sofunny.chickendinnerfirst"
# APK = "E:\\DownloadAPK\\first-test_P452_release_v31_0.31.6-986_F2_63fb564d_95bec1b62_308dc55cc_1aaf47a4e_9ba99a42_3a2f741.apk"
# TestAPKName = "first-test_P452_release_v31_0.31.6-986_F2_63fb564d_95bec1b62_308dc55cc_1aaf47a4e_9ba99a42_3a2f741.apk"  # f
# BaseURL = "http://soft.f.xmfunny.com:8888/sausage/apk/先行/"
# outpath = "E:\\DownloadAPK"
# url = os.path.join(BaseURL, TestAPKName)  # 下载包地址
# wget.download(url, out=Setting.Outpath) # 包下载到指定路径
def IPgetUUID(IP):
    """通过Ip获取UUID"""
    print("开始获取UUID")
    with open(DEVICEINFO,encoding='utf8') as f:
        json_data = json.load(f)
        UUID=json_data[IP]
        return UUID

def installPKG():
    """安装APK
    先判断手机当前APK是否存在,如果存在则卸载,如果不存在,直接安装
    尝试使用Airtest自带安装方案,如该方案安装失败则使用ATX自带安装方案
    上述两种方案均安装失败后,则删除配置文件内的设备ID 防止后续被脚本调用
    """
    print(G.DEVICE.uuid,"开始执行安装流程.............")
    if PKG not in device().list_app():
        print("APK不存在，开始安装！")
        try:

            install(APK, replace=False, install_options=["-g"])  # 正确的
            print(G.DEVICE.uuid,":安装成功")
            SuccessfulDevWriter()
        except:
            try:
                print("第一种方式安装失败，尝试使用第二种安装方式")
                BaseURL=ATXPROVIDER_URL+UUID
                print(downloadPath)
                stu = {"url": downloadPath,"launch":True}
                hearder = {
                    'Cookie': userid,
                }
                print(BaseURL,stu,hearder)
                Result = requests.post(BaseURL,stu,hearder)
                RequestReprot=Result.json()
                if RequestReprot["success"]==True:
                    print(G.DEVICE.uuid, ":安装成功")
                    SuccessfulDevWriter()
            except:
                    pass





    else:
        uninstall(PKG)
        print(G.DEVICE.uuid,":开始卸载旧版本")
        print(G.DEVICE.uuid,":开始安装")
        try:
            install(APK, replace=False, install_options=["-g"])  # 正确的
            log(G.DEVICE.uuid,":安装成功")
            SuccessfulDevWriter()
        except:
            try:
                print("第一种方式安装失败，尝试使用第二种安装方式")
                BaseURL=ATXPROVIDER_URL+UUID
                stu = {"url": downloadPath,"launch":True}
                hearder = {
                    'Cookie': userid,
                }
                print(BaseURL,stu,hearder)
                Result = requests.post(BaseURL,stu,hearder)
                print(Result.json())
                RequestReprot=Result.json()
                if RequestReprot["success"]==True:
                    print(G.DEVICE.uuid, ":安装成功")
                    SuccessfulDevWriter()
                else:
                    with open(DEVICEINFO, encoding='utf-8') as f:
                        json_data = json.load(f)
                        e1 = json_data.pop(G.DEVICE.uuid)
                        with open(DEVICEINFO, "w") as f:
                            json.dump(e1, f)
                        log(G.DEVICE.uuid, "设备移除成功！")
                    raise Exception(G.DEVICE.uuid, ":安装失败")
            except:
                log(G.DEVICE.uuid, "方式2安装失败！，移除设备列表")
                with open(DEVICEINFO, encoding='utf-8') as f:
                    json_data = json.load(f)
                    e1 = json_data.pop(G.DEVICE.uuid)
                    with open(DEVICEINFO, "w") as f:
                        json.dump(e1, f)
                    log(G.DEVICE.uuid,"设备移除成功！")


def SuccessfulDevWriter():
    with open(SuccessfulDevices, "r", encoding="utf-8") as f:
        SuccessfulDev = json.load(f)
        newdata = {G.DEVICE.uuid: IPgetUUID(G.DEVICE.uuid)}
        SuccessfulDev.update(newdata)
    with open(SuccessfulDevices, "w", encoding="utf-8") as f:
        json.dump(SuccessfulDev, f)
    print("可用设备写入成功")

def AccessEnvironment():
    """
    获取环境服务器名称
    param UUID: 设备ID
    return environment:环境服务器名称
    """
    try:
        config = SystemTool.readingIniConfiguration(ConstantVar.EnvironmentConfig)  # 获取 环境配置.ini配置文件对象
        environment = SystemTool.getOnRegionAndKey(config, ConstantVar.DataArea, ConstantVar.Environment)  # 根据.ini文件的区域和key读取值   获取环境
        environment = environment.replace(ConstantVar.Develop,"") # 消除末尾Develop
        environment = environment.replace(ConstantVar.Release, "") # 消除末尾Release
        return environment
    except  Exception as e:
        SystemTool.anomalyRaise(e, f"获取环境服务器名称时异常")  # 打印异常


def switchServer(UUID):
    """
    切换服务器
    param UUID: 设备ID
    """
    try:
        start_app(PKG)  # 启动游戏
        time.sleep(25)
        poco = UnityPoco()
        poco.wait_for_any([poco("BtnLogin")], timeout=35)  # 等待登录按钮显示元素
        time.sleep(2)
        poco("BtnServerList").click()  # 点击服务器列表
        print(f"[{UUID}]切换自动化服务器成功")
        poco.wait_for_any([poco("Title")], timeout=20)  # 等待标题元素显示
        time.sleep(2)
        environment = AccessEnvironment() # 获取环境服务器名称
        poco(text=environment).click()  # 点击服务器
        time.sleep(3)
        stop_app(PKG) # 关闭游戏
    except  Exception as e:
        SystemTool.rerun(switchServer, e, f"切换服务器", UUID)  # 重新运行

UUID = IPgetUUID(G.DEVICE.uuid)
installPKG() # 安装包
switchServer(UUID) # 切换服务器