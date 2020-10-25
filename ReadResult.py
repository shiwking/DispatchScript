TESTRESULT='/TestResult/'
import time
from  ServerConect import *
from  CreatReportID import readReportID
TestResult = []
class Reprot(object):
    def  __int__(self):
        pass


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
                        runtime="%.3f" % (time.time() - json_data['start']),
                        FilePath = Path+"/"+TestCase+"/"+TestCase+".log/log.html"
                        print(FilePath)
                        devlist.append(DevName)
                    TestCaseResult = {'scriptName': TestCase, 'status': status, "path": FilePath, "createtime": createtime,
                                      "device": devlist[0],"runtime":runtime}

                    print(TestCaseResult)
                    TestResult.append(TestCaseResult)
            except:
                pass


    def WiterReprot(self):
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
        localtime1 = time.localtime(float(self.time[0]))
        localtime = time.strftime("%Y_%m_%d_%H_%M_%S", localtime1)
        testName='AutoTest'+(str(localtime))
        Allruntime=str(int((self.time[1]-self.time[0])/60))
        isDelete=0
        insert_db_Summary(testName,AllNum,PassNum,FailNum,SkiplNum,Allruntime,localtime,isDelete)
        print("报告汇总结果写入成功")

        print("开始写入用例测试结果")
        testid = 0
        for caseResult in self.TestReSult:
            caseName=caseResult['scriptName']
            runtime=caseResult['runtime']
            logoinfo=caseResult['path']
            createtime=caseResult['createtime']
            teststatus=caseResult['status']
            isDelete=0
            testresult_id =SearchTestID(testName)
            ReportID = readReportID()
            testDevice=caseResult['device']
            print(testid,caseName,runtime,logoinfo,createtime,teststatus,isDelete,testresult_id,ReportID,testDevice)
            insert_db(testid,caseName,runtime,logoinfo,createtime,teststatus,isDelete,testresult_id,ReportID,testDevice)
            testid=testid+1

if __name__ == '__main__':
    RS=Reprot()
    RS.ReadReport("219")
    print("开始写入数据")
    RS.WiterReprot()