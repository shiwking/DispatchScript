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

    @staticmethod
    def resetAccount(account, accountType, server, useDevice):
        '''
        释放被征用账号
        param account:账号
        param accountType:账号类型  例如：普通账号
        param server:服务器  例如： 开发服 先行服
        param useDevice:占用设备
        return   bool:成功或失败标识
        '''
        cursor, db = Mysql.connectDatabase()  # 连接数据库
        a = "UPDATE AccountPool SET UseDevice=''"
        try:
            b = Mysql.determineIfFieldIsNone(account != None or accountType != None or server != None or useDevice != None, " WHERE")
            c = Mysql.determineIfFieldIsNone(account != None, f" Account = '{account}'")
            d = Mysql.determineIfFieldIsNone(accountType != None, f" AND AccountType = '{accountType}'")
            e = Mysql.determineIfFieldIsNone(server != None, f" AND Server = '{server}'")
            f = Mysql.determineIfFieldIsNone(useDevice != None, f" AND UseDevice = '{useDevice}'")
            UpdateUseDevice = a + b + c + d + e + f
            UpdateUseDevice = Mysql.whereDispose(UpdateUseDevice)  # 对where进行处理
            print(UpdateUseDevice)
            cursor.execute(UpdateUseDevice)  # 执行sql语句
            db.commit()  # 执行sql语句提交
            if (cursor.rowcount == 0):  # 如果更新数量为0 说明更新失败 账号已被征用
                return False
            else:
                return True
        except  Exception as e:
            db.rollback()  # 回滚
            SystemTool.anomalyRaise(e, "释放所有被征用账号时异常")  # 打印异常
        finally:
            db.close()  # 关闭数据库连接

    @staticmethod
    def determineIfFieldIsNone(condition, sql):
        '''
        根据字段是否为None进行修改
        param condition:条件
        param sql:sql
        return   rsql:返回sql
        '''
        rsql = ""  # 返回sql
        try:
            if (condition):
                rsql = sql
            else:
                rsql = ""
            return rsql
        except  Exception as e:
            SystemTool.anomalyRaise(e, "根据字段是否为None进行修改时异常")  # 打印异常

    @staticmethod
    def whereDispose(sql):
        '''
        对where进行处理
        param sql:sql
        return   rsql:返回sql
        '''
        rsql = ""  # 返回sql
        try:
            rsql = sql.replace(" WHERE AND ", " WHERE ")
            return rsql
        except  Exception as e:
            SystemTool.anomalyRaise(e, "对where进行处理时异常")  # 打印异常

