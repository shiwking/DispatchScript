
import yaml
from DockerOperation import *
from CreatReportID import *
import time
from GetDevices import *

class DistributeScripts(object):
    def __init__(self):
        self.testlist={}
        self.DockerOperation=DockerOperation()
        self.DockerOperation.StopAllContainer()
        self.CreatID = CreatID()
        # self.ReportID = readReportID()
        self.ATX= ConnectATX()
        self.ATX.getDevicesIP()
        self.TestReSult=[]
        self.time= []


    def getDevice(self):

        TestDevices=self.ATX.devIPList #链接设备获取设备列表

        return TestDevices

    def getJob(self):
        TestScripts=ServerCommand("ls /Muilt/Muilt/testflow/scripts/TestCase")
        result = ServerCommand("ls /Muilt/Muilt/testflow/scripts/TestCase")
        num = result.split("\n")
        for i in num:
            if i == '':
                num.remove(i)
        print(num)
        return num

    def AutoConfig(self):
        #记录开始时间
        starttime=time.time()
        self.time.append(starttime)
        #获取设备数/脚本数
        DevNum=len(self.getDevice())
        JobNum=len(self.getJob())
        if DevNum>=JobNum:
            """如果设备数量与脚本数量相等，按照1V1分配脚本到设备上"""
            print("设备数量大于或等于脚本数量")
            #脚本分发
            ID = 0
            while ID < JobNum:
                self.DockerOperation.Runcontainers(self.getJob()[ID],self.getDevice()[ID])
                print(self.getJob()[ID],self.getDevice()[ID],self.DockerOperation.DockerList[ID])
                ID = ID + 1
            #间隔30秒确认测试是否完成
            self.DockerOperation.TestResultConfirmation()
            #获取测试结果
            ID=0
            while ID< len(self.DockerOperation.DockerList):
                 self.DockerOperation.GetTestResult(DockerID=self.DockerOperation.DockerList[ID],JobName=self.getJob()[ID])
                 ID=ID+1
            # 结果获取完成后初始化docker 容器进程
            self.DockerOperation.StopAllContainer()


        else:
            """脚本数量大于设备数量"""
            print("脚本数量大于设备数量")
            ExecutionNum = int(JobNum / DevNum)
            Remainder = (JobNum % DevNum)

            lunshu = 0
            while lunshu < ExecutionNum:
                """判断执行轮数"""
                DevID = 0
                JobID = lunshu * DevNum
                self.DockerOperation.DockerList = []
                print("开始分发脚本")
                while DevID < DevNum:
                    print("测试脚本名称：",self.getJob()[JobID] ,"运行设备名称:",self.getDevice()[DevID])
                    self.DockerOperation.Runcontainers(self.getJob()[JobID], self.getDevice()[DevID])
                    JobID = JobID + 1
                    DevID = DevID + 1
                    # 间隔30秒确认测试是否完成
                self.DockerOperation.TestResultConfirmation()
                # 获取测试结果
                ID = 0
                print("开始采集结果")
                JobID = lunshu * DevNum
                while ID < len(self.DockerOperation.DockerList):
                    print("传入DockerID：",self.DockerOperation.DockerList[ID], "传入脚本名称:", self.getJob()[JobID])
                    self.DockerOperation.GetTestResult(DockerID=self.DockerOperation.DockerList[ID],JobName=self.getJob()[JobID])
                    ID = ID + 1
                    JobID=JobID+1
                # 结果获取完成后初始化docker 容器进程
                self.DockerOperation.StopAllContainer()
                # 下一循环
                lunshu = lunshu + 1

                # 余数
            if Remainder != 0:
                #初始化dockerList
                self.DockerOperation.DockerList = []
                print("余数:%s"%Remainder)
                DevID = 0
                JobID = (ExecutionNum * DevNum)
                while DevID < Remainder:
                    self.DockerOperation.Runcontainers(self.getJob()[JobID], self.getDevice()[DevID])
                    DevID = DevID + 1
                    JobID=  JobID + 1
                # 间隔30秒确认测试是否完成
                self.DockerOperation.TestResultConfirmation()

                ID = 0
                JobID = (ExecutionNum * DevNum)
                while ID < len(self.DockerOperation.DockerList):
                    print("传入DockerID：", self.DockerOperation.DockerList[ID], "传入脚本名称:", self.getJob()[JobID])
                    self.DockerOperation.GetTestResult(DockerID=self.DockerOperation.DockerList[ID],JobName=self.getJob()[JobID])
                    ID = ID + 1
                    JobID=JobID+1
                # 结果获取完成后初始化docker容器进程
                self.DockerOperation.StopAllContainer()
        #结束测试，释放设备
        self.ATX.releaseDevice()
        # 记录结束时间
        endtime=time.time()
        self.time.append(endtime)
        #从服务器上下载内容到本地
        runtime=str(int((self.time[1]-self.time[0]))/60)
        RemoteScp(ReprotID=readReportID())
        # 将测试结果存储到服务器上
        self.DockerOperation.getResultToServer(ReprotID=readReportID())
        #解析测试结果
        self.DockerOperation.readResult(ReprotID=readReportID(),runtime=runtime)



if __name__ == '__main__':
    DS=DistributeScripts()
    DS.AutoConfig()


