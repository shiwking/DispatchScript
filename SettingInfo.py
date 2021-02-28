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
TESTRESULT99 = "/TestResult/" #10.30.20.99 上的 TestResult文件夹
TESTRESULT="/var/jenkins_home/TestResult/"
TESTRESULT2="/var/jenkins_home/TestResult"
PROJECEFILE="/Muilt/Muilt/"
LOCALLOGFILES="/var/jenkins_home/TestResult/"
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
    userid = 'user_id="2|1:0|10:1614428232|7:user_id|32:c2hpd2tpbmdAYW5vbnltb3VzLmNvbQ==|772a936bf17ba72c48ab4feccb68a7efabc78af4c1fbb3a9cb92e0e331da5250"; JSESSIONID.3fecd8dd=node01039qu0n4ute0191ysna90qiv910.node0'
elif platform.system().lower() == "linux":  # 判断当前运行环境为linux时
    outpath = "/DownloadAPK"
    ATXSERVER = "http://10.30.20.29:4000/"
    DEVICEINFO = "/var/jenkins_home/deviceInfo.json"
    SuccessfulDevices = "/SuccessfulDevices.json"
    ATXPROVIDER_URL = "http://10.30.20.29:3500/app/install?udid="
    userid = 'user_id="2|1:0|10:1614428232|7:user_id|32:c2hpd2tpbmdAYW5vbnltb3VzLmNvbQ==|772a936bf17ba72c48ab4feccb68a7efabc78af4c1fbb3a9cb92e0e331da5250"; JSESSIONID.3fecd8dd=node01039qu0n4ute0191ysna90qiv910.node0'