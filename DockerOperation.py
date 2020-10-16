
import docker
from  ServerConect import *
from CreatReportID import *
class DockerOperation(object):
    def __init__(self):
        self.client = docker.DockerClient(base_url=DOCKERBASEURL)
        self.DockerList=[]


    def ImagesList(self):
        """获取镜像列表"""
        cls=self.client.images.list()
        return cls

    def dockerList(self):
        """获取容器运行列表"""
        cls=self.client.containers.list()
        return cls

    def Runcontainers(self,JobName,DevName,JobClass=SCRIPTFILEPATH):
        """运行一个容器"""
        JobName=JobName+"  "
        DevName=DevName+"  "
        Commd="python3  run.py "+JobClass+JobName+DevName
        volume = {"/Muilt": {"bind": "/Muilt", "mode": "rw"}}
        container = self.client.containers.run('airtest',Commd,volumes=volume,detach=True)
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

    def GetTestResult(self,DockerID,JobName):
        """单个用例执行后获取测试结果"""
        #切割脚本
        ReprotID=readReportID()
        print("开始存储%s结果"%JobName)
        Job=JobName.split('.')
        JobName1=Job[0]
        datatype=TESTRESULT + "/" +ReprotID
        #打包服务器上的日志文件


        try:
            ServerCommand("mkdir  "+datatype)
            ServerCommand("mkdir  " + datatype+"/ErrorLog")
            ServerCommand("mkdir  " + datatype+"/"+JobName1)
            command = "docker cp " + DockerID + ":"+DOCKERLOGFILE+"/"+JobName1+'.log  ' + TESTRESULT + ReprotID + "/" + JobName1
            print(command)
            command2 = "docker cp " + DockerID + ":"+DOCKERLOGFILE + "/data.json " + TESTRESULT + ReprotID + "/" + JobName1 + "/data.json"
            print(command2)
            ServerCommand(command2)
            ServerCommand(command)

        except:
            pass

    def getResultToServer(self, ReprotID):
        """复制结果到服务器"""
        try:
            command3 = "sshpass -p 'root' scp -r root@10.30.20.99:/TestResult/"+ReprotID +' /TestResult/' + ReprotID
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
        """Docker 进程确认，每隔30秒确认Docker 进程是否结束，最长5分钟，如未结束当异常处理"""
        i=0
        while i<10:
            if len(self.dockerList())==0:
               break
            sleep(5)
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
    DC.client.containers.run('airtest',volumes=volume,detach=True)


