
import yaml
import docker
from DockerOperation import *
from CreatReportID import *
import time
from GetDevices import *
from SettingInfo import *
from Utils.Tool.Kernel import Kernel
class DistributeScripts(Kernel):
    def __init__(self):
        self.testlist={}
        self.DockerOperation=DockerOperation() # 初始化docker
        self.DockerOperation.StopAllContainer() # 停止所有容器
        # self.ReportID = readReportID()
        # self.ATX= ConnectATX() # 连接ATX2
        # self.ATX.getDevicesIP() # 获取连接的设备id
        self.TestReSult=[]
        self.time= []

    def getDevice(self):
        #TestDevices=self.ATX.devIPList #ATX连接设备获取设备列表
        with open(DEVICEINFO, encoding='utf8') as f: # 从./deviceInfo.json获取当前成功装包的设备
            json_data = json.load(f)
            TestDevices = list(json_data.keys())
        return TestDevices

    def getDevUUID(self,devip): # 设备编号
        #UUID = self.ATX.devInfo[devip]
        with open(DEVICEINFO, encoding='utf8') as f:
            json_data = json.load(f)
            UUID = json_data[devip]
        return UUID

    def getJob(self):
        """
        获取所有要执行的用例
        param :
        return caseList:用例list
        """
        result = ServerCommand("ls /Muilt/Muilt/testflow/scripts/TestCase") # 获取TestCase下所有用例 例如testAutomaticallyMatchesSelectionBox.air
        caseList = result.split("\n")
        for i in caseList:
            if i == '':
                caseList.remove(i) # 删除
        return caseList

    def accessEnvironment(self):
        """
        获取环境
        param UUID: 设备ID
        return environment:环境服务器名称
        """
        try:
            config = SystemTool.readingIniConfiguration(os.path.join(SystemTool.getRootDirectory(),ConstantVar.EnvironmentConfig))  # 获取 环境配置.ini配置文件对象
            environment = SystemTool.getOnRegionAndKey(config, ConstantVar.DataArea, ConstantVar.Environment)  # 根据.ini文件的区域和key读取值   获取环境
            return str(environment)
        except  Exception as e:
            SystemTool.anomalyRaise(e, f"获取环境时异常")  # 打印异常

    def AutoConfig(self,equipment,performCase,state):
        """
        自动化用例执行及获取结果
        param equipment:当前所有设备list
        param performCase:需要执行的用例list
        param state:状态  分正常执行和异常重新执行
        return :
        """
        Kernel.FailureCase = [] # 初始化失败用例list
        #记录开始时间
        starttime=time.time()
        self.time.append(starttime)
        #获取设备数/脚本数
        DevNum=len(equipment) # 获取设备数量
        JobNum=len(performCase) # 获取用例数量
        if DevNum>=JobNum:
            """如果设备数量与脚本数量相等，按照1V1分配脚本到设备上"""
            print("设备数量大于或等于脚本数量")
            #脚本分发
            ID = 0 # 用例运行轮数   所有设备都运行一次用例叫一轮
            while ID < JobNum: # 本轮次所有设备都运行一次
                self.DockerOperation.Runcontainers(performCase[ID],equipment[ID],self.accessEnvironment()) # 传入 用例id 和设备id  运行一个容器来运行脚本
                ID = ID + 1
            self.DockerOperation.TestResultConfirmation()#间隔一段确认测试是否完成  docker有没有正常在运行
            #获取测试结果
            ID=0
            while ID< len(self.DockerOperation.DockerList): # 本轮次所有设备都获取一次结果
                 self.DockerOperation.GetTestResult(state,DockerID=self.DockerOperation.DockerList[ID],JobName=performCase[ID],ADBRemoteConnectionAddress = equipment[ID],starttime = starttime) #单个用例执行后复制测试结果到99机上
                 ID = ID + 1
            # 结果获取完成后初始化docker 容器进程
            self.DockerOperation.StopAllContainer()
        else:
            """脚本数量大于设备数量"""
            print("脚本数量大于设备数量")
            ExecutionNum = int(JobNum / DevNum) # 用例数量除设备数量  获得所有设备平均要运行次数
            Remainder = (JobNum % DevNum) # 用例数量除设备数量  取余数
            lunshu = 0
            while lunshu < ExecutionNum: # 如果 轮数小于平均运行用例次数
                """判断执行轮数"""
                DevID = 0
                JobID = lunshu * DevNum
                self.DockerOperation.DockerList = []
                print("开始分发脚本")
                while DevID < DevNum:
                    print("测试脚本名称：",performCase[JobID] ,"运行设备名称:",self.getDevUUID(equipment[DevID]))
                    self.DockerOperation.Runcontainers(performCase[JobID], equipment[DevID],self.accessEnvironment())# 传入 用例id 和设备id  运行一个容器来运行脚本
                    JobID = JobID + 1
                    DevID = DevID + 1
                    # 间隔30秒确认测试是否完成
                self.DockerOperation.TestResultConfirmation()
                # 获取测试结果
                ID = 0
                print("开始采集结果")
                JobID = lunshu * DevNum
                while ID < len(self.DockerOperation.DockerList):
                    print("传入DockerID：",self.DockerOperation.DockerList[ID], "传入脚本名称:", performCase[JobID])
                    self.DockerOperation.GetTestResult(state,DockerID=self.DockerOperation.DockerList[ID],JobName=performCase[JobID],ADBRemoteConnectionAddress = equipment[ID],starttime = starttime) #单个用例执行后复制测试结果到99机上
                    ID = ID + 1
                    JobID=JobID+1
                # 结果获取完成后初始化docker 容器进程
                self.DockerOperation.StopAllContainer() # 停止所有容器
                # 下一循环
                lunshu=lunshu+1
            if Remainder != 0:# 余数不为0时
                #初始化dockerList
                self.DockerOperation.DockerList = []
                print("余数:%s"%Remainder)
                DevID = 0
                JobID = (ExecutionNum * DevNum) # 平均运行用例次数 乘 设备数量
                while DevID < Remainder: # 如果设备数量小于余数
                    self.DockerOperation.Runcontainers(performCase[JobID], equipment[DevID],self.accessEnvironment())# 传入 用例id 和设备id  运行一个容器来运行脚本
                    DevID = DevID + 1
                    JobID=  JobID + 1
                # 间隔30秒确认测试是否完成
                self.DockerOperation.TestResultConfirmation()
                ID = 0
                JobID = (ExecutionNum * DevNum)
                while ID < len(self.DockerOperation.DockerList):
                    print("传入DockerID：", self.DockerOperation.DockerList[ID], "传入脚本名称:", performCase[JobID])
                    self.DockerOperation.GetTestResult(state,DockerID=self.DockerOperation.DockerList[ID],JobName=performCase[JobID],ADBRemoteConnectionAddress = equipment[ID],starttime = starttime)#单个用例执行后复制测试结果到99机上
                    ID = ID + 1
                    JobID=JobID+1
                # 结果获取完成后初始化docker容器进程
                self.DockerOperation.StopAllContainer()# 停止所有容器
        #结束测试，释放设备
        #self.ATX.releaseDevice()
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
    DS.AutoConfig(DS.getDevice(),DS.getJob(),ConstantVar.NormalExecution) # 自动化用例执行及获取结果
    if(len(Kernel.FailureCase) > 0): # 如果有执行失败的用例  启动失败重新运行
        print(f"需要重新运行用例{Kernel.FailureCase}")
        DS.AutoConfig(DS.getDevice(), Kernel.FailureCase, ConstantVar.ExceptionReexecution)  # 自动化用例执行及获取结果   失败重新运行
    #增加一个函数 读取所有用例的结果 将运行失败的用例组装成一个list再次运行一次
    from GetDevices import ConnectATX
    ATX = ConnectATX()
    ATX.releaseDevice() # 释放设备


