TESTRESULT='/TestResult/'
import time
from  ServerConect import *
import json
TestResult = []
class Reprot(object):
    def  __int__(self):
        self.time = []

    def ReadReport(self,readReportID):
        import os
        import json
        print("测试完成开始读取结果")
        Path = TESTRESULT + readReportID
        print(Path)
        CaseList = os.listdir(Path)
        print(CaseList)
        for TestCase in CaseList:
            TestCaseJson = os.path.join(Path, TestCase, "data.json")
            print(TestCaseJson)
            if TestCase == "ErrorLog":
                continue
            try:
                with open(TestCaseJson, 'r', encoding='utf8')as fp:
                    json_data = json.load(fp)
                    localtime1 = time.localtime(float(json_data["start"]))
                    createtime = time.strftime("%Y-%m-%d %H:%M:%S", localtime1)
                    devlist = []
                    for DevName in json_data["tests"].keys():
                        if json_data["tests"][DevName]['status'] == 0:
                            status = "Pass"
                        else:
                            status = "Fail"
                        FilePath = Path+"/"+TestCase+"/"+TestCase+".log/log.html"
                        print(FilePath)
                        devlist.append(DevName)
                    TestCaseResult = {'scriptName': TestCase, 'status': status, "path": FilePath, "createtime": createtime,
                                      "device": devlist[0]}
                    print(TestCaseResult)
                    TestResult.append(TestCaseResult)
            except:
                pass
    def ReadDevinfo(self,devIP):

        DEVICEINFO = "/var/jenkins_home/deviceInfo.json"
        with open(DEVICEINFO, 'r') as load_f:
            load_dict = json.load(load_f)
        devuuid= load_dict[devIP]
        return devuuid

    def WiterReprot(self,ReportID,runtime):
        print("开始写入汇总结果")
        TestScripNum =len(TestResult)
        print(TestScripNum)
        passlist=[]
        faillist=[]
        skiplist=[]
        for testpass in TestResult:
            Result=testpass['status']
            if Result=='Pass':
                passlist.append(Result)
            elif Result=='Fail':
                faillist.append(Result)
            elif Result=='Skip':
                skiplist.append(Result)

        PassNum  = len(passlist)
        FailNum  = len(faillist)
        SkiplNum = len(skiplist)
        AllNum=PassNum+FailNum+SkiplNum
        localtime1 = time.localtime(time.time())
        localtime = time.strftime("%Y_%m_%d_%H_%M_%S", localtime1)
        testName='AutoTest'+(str(localtime))
        isDelete=0
        insert_db_Summary(testName,AllNum,PassNum,FailNum,SkiplNum,runtime,localtime,isDelete)
        print("报告汇总结果写入成功")
        print("开始写入用例测试结果")
        testid = 0
        for caseResult in TestResult:
            caseName=caseResult['scriptName']
            runtime="30"
            logoinfo=caseResult['path']
            createtime=caseResult['createtime']
            teststatus=caseResult['status']
            isDelete=0
            testresult_id =SearchTestID(testName)
            testDevice=caseResult['device']
            DevUUID=self.ReadDevinfo(testDevice)
            print(testid,caseName,runtime,logoinfo,createtime,teststatus,isDelete,testresult_id,ReportID,DevUUID)
            insert_db(testid,caseName,runtime,logoinfo,createtime,teststatus,isDelete,testresult_id,ReportID,DevUUID)
            testid=testid+1

if __name__ == '__main__':
    import sys
    Commad = sys.argv
    ReportID = Commad[1]
    runtime=Commad[2]
    RS=Reprot()
    RS.ReadReport(ReportID)
    print("开始写入数据")
    RS.WiterReprot(ReportID,runtime)