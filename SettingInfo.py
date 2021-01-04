import platform
from time  import sleep
import datetime
import os
"""脚本Docker运行目标服务器"""
SERVERIP="10.30.20.99"
SERVERIP2="10.30.20.29"
PORT="22"
USERNAME="root"
PASSWORD="root"

DOCKERBASEURL='tcp://10.30.20.99:2375'
DODCERIDLIST=[]
TESTRESULT="/TestResult/"
PROJECEFILE="/Muilt/Muilt/"
LOCALLOGFILES="/TestResult/"
SCRIPTFILEPATH="/Muilt/Muilt/testflow/scripts/TestCase/"

DOCKERLOGFILE="/LogDir"

MYSQLHOST="10.30.20.29"
MYSQLPORT=3306
MYSQLUSER="root"
MYSQLPASSWORD="@Root123"
MYSQLDB="reprot"


if platform.system().lower() == "windows":  # 判断当前运行环境为windows时
    outpath = r"E:\DispatchScript\DownloadAPK"
    ATXSERVER = "http://10.30.20.29:4000/"
    DEVICEINFO = r"E:\DispatchScript\deviceInfo.json"
    SuccessfulDevices =r"E:\DispatchScript\SuccessfulDevices.json"
    ATXPROVIDER_URL = "http://10.30.20.29:3500/app/install?udid="
    userid = 'user_id="2|1:0|10:1609209313|7:user_id|32:c2hpd2tpbmdAYW5vbnltb3VzLmNvbQ==|a87978b7aca1d6a488f923baf30bdb3524590fdd47527295bb0cac0e89735bff"; Path=/; Domain=10.30.20.29; Expires=Fri, 23 Oct 2020 06:13:43 GMT;'
elif platform.system().lower() == "linux":  # 判断当前运行环境为linux时
    outpath = "/DownloadAPK"
    ATXSERVER = "http://10.30.20.29:4000/"
    DEVICEINFO = "/var/jenkins_home/deviceInfo.json"
    SuccessfulDevices = "/SuccessfulDevices.json"
    ATXPROVIDER_URL = "http://10.30.20.29:3500/app/install?udid="
    userid = 'user_id="2|1:0|10:1609209313|7:user_id|32:c2hpd2tpbmdAYW5vbnltb3VzLmNvbQ==|a87978b7aca1d6a488f923baf30bdb3524590fdd47527295bb0cac0e89735bff"; Path=/; Domain=10.30.20.29; Expires=Fri, 23 Oct 2020 06:13:43 GMT;'