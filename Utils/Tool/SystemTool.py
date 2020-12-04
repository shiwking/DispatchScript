# -*- encoding=utf8 -*-
# @Author:
import sys
import traceback
import subprocess
import os
import configparser
import shutil
import json
import datetime,time
import ctypes
import logging
import platform
from Utils.Constant.ConstantVar import ConstantVar
# 系统工具类
class SystemTool():

    @staticmethod
    def anomalyRaise(e, message):
        """
       打印异常并且再次抛出异常
       :param e: 异常
       :param message: 异常信息
       """
        print(e.args)
        print(message)
        raise

    @staticmethod
    def readFileRStr(path):
        """
       读取指定文件内容返回字符串
       param path:地址
       return rowList：记录每行信息的list
       """
        data = ""  # 返回的字符串
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                # 按照行读取
                for line in f.readlines():
                    # line = line.strip() # 去除行尾的\n
                    data += line  # 追加进字符串
                # print(data)
                return data
        except  Exception as e:
            SystemTool.anomalyRaise(e, "读取指定文件内容返回字符串时异常")  # 打印异常

    @staticmethod
    def getRootDirectory():
        """
       获取项目根目录路径
       param :
       return rootPath：根目录路径
       """
        rootPath = ""  # 根目录路径
        if (SystemTool.acquireEnvironment() == ConstantVar.Windows):  # 如果当前环境为windows
            curPath = os.path.abspath(os.path.dirname(__file__))
            rootPath = curPath[:curPath.find(ConstantVar.ProjectName + ConstantVar.Sprit) + len(ConstantVar.ProjectName + ConstantVar.Sprit)]  # 获取myProject，也就是项目的根路径
        elif (SystemTool.acquireEnvironment() == ConstantVar.Linux):  # 如果当前环境为linux
            curPath = os.path.abspath(os.path.dirname(__file__))
            rootPath = curPath[:curPath.find(os.path.join(ConstantVar.ProjectName + ConstantVar.Sprit)) + len(
                os.path.join(ConstantVar.ProjectName + ConstantVar.Sprit))]  # 获取myProject，也就是项目的根路径
        return rootPath

    @staticmethod
    def acquireEnvironment():
        """
       获取当前运行环境
       param :
       return TestCaseFiles：用例文件夹集
       """
        currentEnvironment = ""  # 当前环境
        try:
            if platform.system().lower() == ConstantVar.Windows:  # 判断当前运行环境为windows时
                currentEnvironment = ConstantVar.Windows
            elif platform.system().lower() == ConstantVar.Linux:  # 判断当前运行环境为linux时
                currentEnvironment = ConstantVar.Linux
            return currentEnvironment
        except  Exception as e:
            SystemTool.anomalyRaise(e, "获取当前运行环境时异常")  # 打印异常

    @staticmethod
    def readJson(path):
        """
       根据指定路径读取json文件 返回字典
       param path:地址
       return dictionaries:字典
       """
        try:
            with open(path, 'r', encoding='utf8') as fp:
                json_data = json.load(fp)
            return json_data  # 返回字典格式的json
        except  Exception as e:
            SystemTool.anomalyRaise(e, "根据指定路径读取json文件 返回字典时异常")  # 打印异常

    @staticmethod
    def writeOutJsonNoLock(json, path, way):
        """
       写出json到指定文件（无锁）
       param json:json
       param path:地址
       param way:写入方式
       """
        try:
            if (way == "覆盖"):
                with open(path, "w") as fp:  # w，代表覆盖内容
                    fp.write(json)
            elif (way == "追加"):
                with open(path, "a") as fp:  # a，代表追加内容
                    fp.write(json)
        except  Exception as e:
            SystemTool.anomalyRaise(e, "写出json到指定文件（无锁）时异常")  # 打印异常