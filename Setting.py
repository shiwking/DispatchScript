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
LOCALLOGFILES='D:\\TestResult\\'
SCRIPTFILEPATH="/Muilt/Muilt/testflow/scripts/TestCase/"

DOCKERLOGFILE="/LogDir"

MYSQLHOST="10.30.20.29"
MYSQLPORT=3306
MYSQLUSER="root"
MYSQLPASSWORD="@Root123"
MYSQLDB="reprot"


ATXSERVER="http://10.30.20.29:4000/"
DEVICEINFO="/var/jenkins_home/deviceInfo.json"
# DEVICEINFO="D:\\deviceInfo.json"
