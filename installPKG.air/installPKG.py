# -*- encoding=utf8 -*-
__author__ = "shiwking"

import json
from airtest.core.api import *
auto_setup(__file__)
PWD = os.path.dirname(__file__)
with open("/DownloadAPK/config.json",'r',encoding='utf8')as fp:
    json_data = json.load(fp)

PKG = json_data["PKG"]
APK = json_data["APKPath"]


if PKG not in device().list_app():
    log(":开始安装")
    install(APK ,replace=False,install_options=["-g"])
    log(":安装成功")
else:
    uninstall(PKG)
    log(":开始卸载旧版本")
    log(":开始安装")
    install(APK, replace=False, install_options=["-g"])
    log("安装成功")

start_app(PKG)

