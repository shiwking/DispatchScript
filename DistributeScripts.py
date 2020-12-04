
import yaml
from DockerOperation import *
from CreatReportID import *
import time
from GetDevices import *
from SettingInfo import *
class DistributeScripts(object):
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

    def getJob(self): # 获取当前用例数
        result = ServerCommand("ls /Muilt/Muilt/testflow/scripts/TestCase")
        num = result.split("\n")
        for i in num:
            if i == '':
                num.remove(i)
        return num

    def AutoConfig(self):
        #记录开始时间
        starttime=time.time()
        self.time.append(starttime)
        #获取设备数/脚本数
        DevNum=len(self.getDevice()) # 获取设备数量
        JobNum=len(self.getJob()) # 获取用例数量
        if DevNum>=JobNum:
            """如果设备数量与脚本数量相等，按照1V1分配脚本到设备上"""
            print("设备数量大于或等于脚本数量")
            #脚本分发
            ID = 0 # 用例运行轮数   所有设备都运行一次用例叫一轮
            while ID < JobNum: # 如果轮数小于 用例数量
                self.DockerOperation.Runcontainers(self.getJob()[ID],self.getDevice()[ID]) # 传入 用例id 和设备id  运行一个容器来运行脚本
                print(self.getJob()[ID],self.getDevice()[ID],self.DockerOperation.DockerList[ID])
                ID = ID + 1
            self.DockerOperation.TestResultConfirmation()#间隔一段确认测试是否完成  docker有没有正常在运行
            #获取测试结果
            ID=0
            while ID< len(self.DockerOperation.DockerList): # 如果设备数量小于轮数
                 self.DockerOperation.GetTestResult(DockerID=self.DockerOperation.DockerList[ID],JobName=self.getJob()[ID],ADBRemoteConnectionAddress = self.getDevice()[ID],starttime = starttime)
                 ID=ID+1
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
                    print("测试脚本名称：",self.getJob()[JobID] ,"运行设备名称:",self.getDevUUID(self.getDevice()[DevID]))
                    self.DockerOperation.Runcontainers(self.getJob()[JobID], self.getDevice()[DevID])# 传入 用例id 和设备id  运行一个容器来运行脚本
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
                    self.DockerOperation.GetTestResult(DockerID=self.DockerOperation.DockerList[ID],JobName=self.getJob()[JobID],ADBRemoteConnectionAddress = self.getDevice()[ID],starttime = starttime) #单个用例执行后获取测试结果
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
                    self.DockerOperation.Runcontainers(self.getJob()[JobID], self.getDevice()[DevID])# 传入 用例id 和设备id  运行一个容器来运行脚本
                    DevID = DevID + 1
                    JobID=  JobID + 1
                # 间隔30秒确认测试是否完成
                self.DockerOperation.TestResultConfirmation()
                ID = 0
                JobID = (ExecutionNum * DevNum)
                while ID < len(self.DockerOperation.DockerList):
                    print("传入DockerID：", self.DockerOperation.DockerList[ID], "传入脚本名称:", self.getJob()[JobID])
                    self.DockerOperation.GetTestResult(DockerID=self.DockerOperation.DockerList[ID],JobName=self.getJob()[JobID],ADBRemoteConnectionAddress = self.getDevice()[ID],starttime = starttime)#单个用例执行后获取测试结果
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
    DS.AutoConfig()
    from GetDevices import ConnectATX
    ATX = ConnectATX()
    ATX.releaseDevice()


