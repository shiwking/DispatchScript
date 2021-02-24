

import docker
import os
import time
from  ServerConect import *
from CreatReportID import *
from  time import sleep
from Utils.Tool.SystemTool import SystemTool
from Utils.Tool.Transition import Transition
from Utils.Constant.ConstantVar import ConstantVar
class DockerOperation(object):
    def __init__(self):
        self.client = docker.DockerClient(base_url=DOCKERBASEURL) # tcp://10.30.20.99:2375     远程99
        self.DockerList=[]


    def ImagesList(self):
        """获取镜像列表"""
        cls=self.client.images.list()
        return cls

    def dockerList(self):
        """获取容器运行列表"""
        cls=self.client.containers.list()
        return cls

    def Runcontainers(self,JobName,DevName,Environment,JobClass=SCRIPTFILEPATH):
        """
        运行一个99机器上容器 运行用例
        JobName： 用例名.air
        DevName ：设备序列号
        Environment：环境
        JobClass：/Muilt/Muilt/testflow/scripts/TestCase/
        """
        JobName=JobName+"  "
        DevName=DevName+"  "
        Environment = Environment + "  "
        print("python3  run.py "+JobClass+JobName+DevName+Environment)
        Commd = "python3  run.py "+JobClass+JobName+DevName+Environment
        volume = {"/Muilt": {"bind": "/Muilt", "mode": "rw"}} # volume：容器卷 意思是使用airtest镜像启动一个容器，将宿主机上的/Muilt复制一份到容器中 可读可写
        container = self.client.containers.run('airtest',Commd,volumes=volume,detach=True) # 调用99号机上run方法    airtest：99号几上镜像名 Commd：run方法所需参数 volume：容器卷 意思是使用airtest镜像启动一个容器，将宿主机上的/Muilt复制一份到容器中 可读可写
        self.DockerList.append(container.short_id)
        return container.short_id

    def StopAllContainer(self):
        """停止所有容器运行"""
        for container in self.client.containers.list():
            container.stop()

    def GetLogs(self,DockerID):
        """获取容器日志"""
        container = self.client.containers.get(DockerID)
        return  container.logs()

    def GetTestResult(self,DockerID,JobName,ADBRemoteConnectionAddress,starttime):
        """
       单个用例执行后获取测试结果   执行机器10.30.20.99
       param DockerID:dockerID
       param JobName:用例air名
       param ADBRemoteConnectionAddress:ADB远程连接地址
       param starttime:开始时间
       return status：用例结果
       """
        ReprotID = readReportID() # 读取airtestreprotlist 最大的id +1 为当前运行报告id  例如 /TestResult/83  的83
        print("开始存储%s结果"%JobName)
        Job=JobName.split('.')
        JobName1=Job[0] # 用例英文名
        datatype=TESTRESULT + ReprotID # 例如：/TestResult/83
        #打包服务器上的日志文件
        ADBAddress = ADBRemoteConnectionAddress.replace(".","_") # 将ADB远程连接地址的“.” 替换为“_”
        ADBAddress = ADBAddress.replace(":", "_")  # 将ADB远程连接地址的“:” 替换为“_”
        status = "" # 用例执行状态
        try:
            #
            sleep(5)
            ServerCommand("mkdir  " + datatype) # 99创建 /TestResult/82文件夹
            ServerCommand("mkdir  " + os.path.join(datatype,"ErrorLog")) # 99创建 /TestResult/82/ErrorLog'文件夹
            ServerCommand("mkdir  " + os.path.join(datatype,JobName1))# 99创建 /TestResult/82/testAutomaticallyMatchesSelectionBox文件夹
            command = "docker cp " + DockerID + ":" + os.path.join(DOCKERLOGFILE,JobName1 + '.log') + " " + os.path.join(datatype,JobName1) # 从docker上复制/LogDir/testAutomaticallyMatchesSelectionBox.log  到99 /TestResult/83/testAutomaticallyMatchesSelectionBox
            print(command)
            command2 = "docker cp " + DockerID + ":" + os.path.join(DOCKERLOGFILE,"data.json") + " " + os.path.join(datatype,JobName1,"data.json")# 从docker上复制/LogDir/data.json  到99 /TestResult/83/testAutomaticallyMatchesSelectionBox/data.json
            print(command2)
            cmd_result2 = ServerCommand(command2) # 执行命令
            cmd_result1 = ServerCommand(command)
            self.setDockerID(ReprotID, JobName1, DockerID)  # 设置dockerID 到Config.ini
        except:
            try:
                #如果脚本运行不正常设置为脚本运行失败
                dataJson = SystemTool.readJson(os.path.join(SystemTool.getRootDirectory(),ConstantVar.DataTemplate)) # 读取data.json模板
                dataJson["start"] = str(starttime) # 设置开始时间
                dataJson["script"] = os.path.join(ConstantVar.TestCasePath,JobName1 + ConstantVar.Air)  # 往data.json  中script 设置当前运行用例.air路径
                dataJson["tests"] = {ADBRemoteConnectionAddress:{"status": 2,"path": os.path.join(SystemTool.getRootDirectory(),ConstantVar.TestCasePath,JobName,ConstantVar.Log,ADBAddress,ConstantVar.LogHtml)}}  # 设置tests字典中的值
                str_json = Transition.DictionaryTurnJsonSerialize(dataJson)  # 字典转json
                SystemTool.writeOutJsonNoLock(str_json, os.path.join(SystemTool.getRootDirectory(),ConstantVar.TemporaryPath, ConstantVar.DataJson), "覆盖")  # 写出data.json到临时文件
                command3 = "sshpass -p 'root' scp -r " + os.path.join(SystemTool.getRootDirectory(),ConstantVar.TemporaryPath, ConstantVar.DataJson) + ' root@10.30.20.99:' + TESTRESULT + os.path.join(ReprotID,JobName1) # 将data.json复制到99机器的 /TestResult/82/用例下
                ServerCommand(command3, IP=SERVERIP2)
            except  Exception as e:
                SystemTool.anomalyRaise(e, "根据模板生成data.json失败")  # 打印异常

    def setDockerID(self,ReprotID,JobName1,DockerID):
        '''
        设置dockerID 到Config.ini 例如：/TestResult/83/testAutomaticallyMatchesSelectionBox/Config.ini
        param ReprotID: 例如：83
        param JobName1:用例名
        param DockerID:dockerID
        return   :
        '''
        try:
            SystemTool.thereIsNoCreationNotLock(os.path.join(TESTRESULT2,ReprotID,JobName1)) # docker创建/TestResult/83/testAutomaticallyMatchesSelectionBox  有同步到29
            configPath = os.path.join(TESTRESULT2,ReprotID,JobName1,ConstantVar.ConfigIni)
            SystemTool.copyFile(os.path.join(SystemTool.getRootDirectory(), ConstantVar.ConfigIniTemplate), configPath)  # 复制Config.ini模板 到/TestResult/83/testAutomaticallyMatchesSelectionBox/Config.ini
            config = SystemTool.readingIniConfiguration(configPath)  # 获取闪退 设备Config.ini配置文件对象
            SystemTool.setOnRegionAndKey(config, configPath, ConstantVar.DataArea, ConstantVar.DockerIDKey, DockerID)  # 根据.ini文件的区域和key设置值
        except  Exception as e:
            SystemTool.anomalyRaise(e, f"设置dockerID 到Config.ini时异常")  # 打印异常

    def getResultToServer(self, ReprotID):
        """复制结果到服务器 从99复制/TestResult/ReprotID到29"""
        try:
            #command3 = "sshpass -p 'root' scp -r root@10.30.20.99:/TestResult/"+ReprotID +' /TestResult/' + ReprotID # 复制99的/TestResult/ReprotID 到29/TestResult/ReprotID
            command3 = "sshpass -p 'root' scp -r root@10.30.20.99:" + TESTRESULT + ReprotID + ' ' + TESTRESULT2  # 复制99的/TestResult/ReprotID 到29/TestResult
            print(command3)
            ServerCommand(command3, IP=SERVERIP2)
        except:
            pass
    def readResult(self, ReprotID,runtime):
        """开始解析测试结果"""
        try:
            command="python3 /testReprot/ReadResult.py " + ReprotID + "  "+ runtime
            print(command)
            ServerCommand(command, IP=SERVERIP2)
        except:
            pass


    def TestResultConfirmation(self):
        """Docker 进程确认，每隔30秒确认Docker 进程是否结束，最长8分钟，如未结束当异常处理"""
        i=0
        while i<60:
            if len(self.dockerList())==0:
               break
            sleep(8)
            i=i+1

        # if len(self.dockerList())!=0:
        #     #获取错误日志
        #     import re
        #     pattern = re.compile('r: (.+)>]')
        #     resultList = pattern.findall(self.dockerList())
        #     # resultList=["a9167480fe"]
        #     for DockerID in resultList:
        #         DocErrorInfo = self.GetLogs(DockerID).decode('utf-8')
        #         fileName="./Error/"+DockerID+".txt"
        #         with open(fileName, "w") as f:
        #             f.write(DocErrorInfo)
        #     #此处上传老是出问题,后续可以考虑用Zip 进行



if __name__ == '__main__':
    DC=DockerOperation()
    volume={"/Muilt": {"bind": "/Muilt", "mode": "rw"}}
    DC.client.containers.run('airtest',volumes=volume,detach=True) # 远程启动docker


