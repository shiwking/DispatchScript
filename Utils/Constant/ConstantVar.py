# coding=utf-8
import os
import time
import socket
import platform

class ConstantVar():
        #常量类

        '''系统常量'''
        ProjectName = "DispatchScript"  # 项目名

        """运行环境"""
        Windows = "windows"
        Linux = "linux"
        slash = None
        if platform.system().lower() == Windows: # 判断当前运行环境为windows时
            slash = "\\"
        elif platform.system().lower() == Linux:# 判断当前运行环境为linux时
            slash = "/"
        Sprit = slash # 当前运行环境斜杠

        '''linux路径'''
        OutOfSyncPath = "/home" # linux不会同步的路径

        """模板"""
        DataTemplate = os.path.join("Utils", "Template", "Json", "dataTemplate.json") # data.json模板
        ConfigIniTemplate = os.path.join("Utils", "Template", "IniConfig", "Config.ini")  # Config.ini模板

        """文件路径及文件常量"""
        TestCasePath = os.path.join("Muilt", "Muilt", "testflow", "scripts","TestCase") # TestCase路径
        TemporaryPath = os.path.join("Utils", "Temporary") # 临时文件夹路径
        PicturePath = os.path.join("Utils", "Picture")  # 用例图片路径
        TESTRESULT = "TestResult" # 结果文件夹
        TestResult = "TestResult"  # 测试结果文件夹
        DataJson = "data.json"
        Log = "log" # 日志文件夹
        LogHtml = "log.html" # 日志html

        """图片"""
        PrivacyAgreementAcceptance = os.path.join("Utils", "Picture","GameSystem","tpl1611209285654.png")  # 隐私协议 接受图像

        """文件后缀"""
        Json = ".json"  # 套件总json
        Xlsx = ".xlsx"
        Py = ".py"
        Air = ".air"
        Html = ".html"
        """状态"""
        FirstTake = "先行服"
        DevTake = "开发服"
        Develop = "Develop" # 开发服
        Release = "Release" # 先行服
        NormalExecution = "正常执行" # 正常执行
        ExceptionReexecution = "异常重新执行" # 异常重新执行

        """.ini文件"""
        ConfigIni = "Config.ini" # .ini配置文件
        DataArea = "Data" #   Data区域
        DockerIDKey = "DockerID" #   DockerID key
        EnvironmentConfig = os.path.join("Utils", "IniConfig", "EnvironmentConfig.ini")  # 环境配置.ini
        Environment = "Environment" # Environment key
