# coding=utf-8
import os

import pymysql

from Utils.Constant.ConstantVar import ConstantVar
from Utils.Tool.Kernel import Kernel
from Utils.Tool.SystemTool import SystemTool

pymysql.install_as_MySQLdb() # 让python3支持MySQLdb

class Mysql(Kernel):
    """Mysql数据库类"""

    @staticmethod
    def connectDatabase():
        '''
        连接数据库
        param :
        return   cursor,db:
        '''
        try:
            db = pymysql.connect(host="10.30.20.29", port=3306, user="root", password="@Root123", database="SausageAuto",charset='utf8') # host ip ，port端口号 ， user账号，password密码，database连接的数据库，charset 字符集
            cursor = db.cursor()
            return cursor,db
        except  Exception as e:
            SystemTool.anomalyRaise(e, "连接数据库时异常")  # 打印异常

    @staticmethod
    def connectDatabaseMySQLdb():
        '''
        连接数据库MySQLdb(SausageAuto)
        param :
        return   cursor,db:
        查询结果带字段名
        '''
        try:
            db = pymysql.connect(host="10.30.20.29", port=3306, user="root", password="@Root123", database="SausageAuto", charset='utf8',db='adu')  # host ip ，port端口号 ， user账号，password密码，database连接的数据库，charset 字符集
            cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
            return cursor, db
        except  Exception as e:
            SystemTool.anomalyRaise(e, "连接数据库MySQLdb(SausageAuto)时异常")  # 打印异常

    @staticmethod
    def connectDatabaseMySQLdbReprot():
        '''
        连接数据库MySQLdb(reprot)
        param :
        return   cursor,db:
        查询结果带字段名
        '''
        try:
            db = pymysql.connect(host="10.30.20.29", port=3306, user="root", password="@Root123", database="reprot", charset='utf8', db='adu')  # host ip ，port端口号 ， user账号，password密码，database连接的数据库，charset 字符集
            cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
            return cursor, db
        except  Exception as e:
            SystemTool.anomalyRaise(e, "连接数据库MySQLdb(reprot)时异常")  # 打印异常

    @staticmethod
    def UpdateLanguagesConfiguration(languages=""):
        '''
        更新语种配置表
        param languages:语种
        return
        '''
        cursor, db = Mysql.connectDatabase()  # 连接数据库
        try:
            Update = "UPDATE LanguagesConfiguration A SET A.Languages = '%s'" % (languages)
            print(Update)
            cursor.execute(Update)  # 执行sql语句
            db.commit()  # 执行sql语句提交
            print(str(cursor.rowcount) + " 条记录已更新")
            return str(cursor.rowcount)
        except  Exception as e:
            db.rollback()  # 回滚
            SystemTool.anomalyRaise(e, "更新语种配置表时异常")  # 打印异常
        finally:
            db.close()  # 关闭数据库连接

