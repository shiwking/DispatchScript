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

        """文件路径及文件常量"""
        TestCasePath = os.path.join("Muilt", "Muilt", "testflow", "scripts","TestCase") # TestCase路径
        TemporaryPath = os.path.join("Utils", "Temporary") # 临时文件夹路径
        TestResult = "TestResult"  # 测试结果文件夹
        DataJson = "data.json"
        Log = "log" # 日志文件夹
        LogHtml = "log.html" # 日志html

        """文件后缀"""
        Json = ".json"  # 套件总json
        Xlsx = ".xlsx"
        Py = ".py"
        Air = ".air"
        Html = ".html"

