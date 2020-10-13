from time  import sleep
import datetime
from CreatReportID import *
import os
# SERVERIP="192.168.206.134"


"""脚本Docker运行目标服务器"""
SERVERIP="10.30.20.99"
SERVERIP2="10.30.20.29"
PORT="22"
USERNAME="root"
PASSWORD="root"
# LOCALFILE="D:\docker-compose.yml"
# REMOTEFILE="/Muilt/DockerSetting/docker-compose.yml"
# BUILDDOCKER="cd /Muilt/DockerSetting/ && docker-compose -f docker-compose.yml up -d"
# DOCKERBASEURL='tcp://192.168.206.134:2375'
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