from Setting import *
import yaml
import os
TestScripts=["test1.air","test2.air","test3.air","test4.air","test5.air","test6.air","test7.air","test8.air","test9.air"]

TestDevices=["192.168.191.1:5555",
             "192.168.191.2:5555",
             "192.168.191.3:5555",
             "192.168.191.4:5555",
             "192.168.191.5:5555",
            ]

TestDeviceNum = len(TestDevices)
TestScriptNum = len(TestScripts)
print("设备数量：", TestDeviceNum, "脚本数量：", TestScriptNum)



def  AutoConfig(TestDevices,TestScripts):
    dockerCompose={
        'version': "3",
        'services':{
            }
        }

    if TestDeviceNum==TestScriptNum:
        """如果设备数量与脚本数量相等，按照1V1分配脚本到设备上"""
        print("设备数量=脚本数量")
        ID=0
        testlist = {}
        while ID<TestDeviceNum:

            ServerId = "S" + str(ID)

            command="airtest run /TestCase/"+TestScripts[ID] +"  --device  Android://127.0.0.1:5037/"+TestDevices[ID]
            serverConf={
                'image': 'airtest',
                'command': command,
                'volumes': ['/TestCase:/TestCase']
                }
            testlist[ServerId]=serverConf
            ID=ID+1


        print(dockerCompose)

    elif TestDeviceNum>TestScriptNum:
        """如果设备数量大于脚本数量，按照脚本数量作为上限防止越界"""
        print("设备数量大于脚本数量")
        testlist = {}
        ID = 0
        while ID < TestScriptNum:

            ServerId = "S" + str(ID)

            command = "airtest run /TestCase/" + TestScripts[ID] + "  --device  Android://127.0.0.1:5037/" + \
                      TestDevices[ID]
            serverConf = {
                'image': 'airtest',
                'command': command,
                'volumes': ['/TestCase:/TestCase']
            }
            testlist[ServerId] = serverConf
            ID = ID + 1
        dockerCompose['services'] = testlist


    else:
        """脚本数量大于设备数量"""
        print("设备数量<脚本数量")
        #执行轮数
        ExecutionNum=int(TestScriptNum / TestDeviceNum)
        Remainder = (TestScriptNum % TestDeviceNum)
        testlist={}
        lunshu=0
        while lunshu<ExecutionNum:
            """判断执行轮数"""

            DevID = 0
            JobID = lunshu * TestDeviceNum

            while DevID<TestDeviceNum:
                DockerName = "S" + str(DevID)
                command = "airtest run /TestCase/" + TestScripts[JobID] + "  --device  Android://127.0.0.1:5037/" + TestDevices[DevID]
                serverConf = {
                    'image': 'airtest',
                    'command': command,
                    'volumes': ['/TestCase:/TestCase']
                            }
                testlist[DockerName] = serverConf
                JobID=JobID+1
                DevID=DevID+1
                dockerCompose['services'] = testlist  #追加写入 。此处应该清空替换 明天搞

            lunshu=lunshu+1




        #余数
        if Remainder!=0:

            testlist={}
            DevID=0
            JobID = (ExecutionNum * TestDeviceNum)
            while DevID < Remainder:

                DockerName = "S" + str(DevID)


                command = "airtest run /TestCase/" + TestScripts[JobID] + "  --device  Android://127.0.0.1:5037/" + TestDevices[DevID]

                serverConf = {
                    'image': 'airtest',
                    'command': command,
                    'volumes': ['/TestCase:/TestCase']
                }

                DevID=DevID+1
                JobID=JobID+1
                testlist[DockerName] = serverConf
                dockerCompose['services'] = testlist


            with open(LOCALFILE, "w", encoding="utf-8") as f:
                yaml.dump(dockerCompose, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

if __name__ == '__main__':

    AutoConfig(TestDevices,TestScripts)