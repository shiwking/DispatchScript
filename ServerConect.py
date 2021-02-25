from SettingInfo import *
import paramiko
import pymysql
import re
def ServerCommand(command,IP=SERVERIP,port=PORT,username=USERNAME,passwrod=PASSWORD):

    """"
    :param command ：命令行
    :param ip: 服务器ip地址
    :param port: 端口(22)
    :param user: 用户名
    :param password: 用户密码
    """
    ssh = paramiko.SSHClient()#绑定一个实例
    ssh.load_system_host_keys()#加载known_hosts文件
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())#远程连接如果提示yes/no时，默认为yes
    ssh.connect(IP,port,username,passwrod,allow_agent=False,look_for_keys=False) #连接远程主机
    stdin, stdout, stderr = ssh.exec_command(command)   #执行指令，并将命令本身及命令的执行结果赋值到标准办入、标准输出或者标准错误
    cmd_result = stdout.read().decode('utf-8') #取得执行的输出
    ssh.close()
    return  cmd_result

def SshScpPut(local_file, remote_file,ip=SERVERIP, port=PORT, user=USERNAME, password=PASSWORD ):

    """
    :param ip: 服务器ip地址
    :param port: 端口(22)
    :param user: 用户名
    :param password: 用户密码
    :param local_file: 本地文件地址
    :param remote_file: 要上传的文件地址（例：/test.txt）
    :return:
    """

    ssh = paramiko.SSHClient()#绑定一个实例
    ssh.load_system_host_keys()  # 加载known_hosts文件
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())#远程连接如果提示yes/no时，默认为yes
    ssh.connect(ip, port, user, password,allow_agent=False,look_for_keys=False)#连接远程主机
    sftp = ssh.open_sftp()
    sftp.put(local_file, remote_file)
    print("脚本上传成功")

def RemoteScp(ReprotID,local_file=LOCALLOGFILES, ip=SERVERIP, port=PORT, user=USERNAME, password=PASSWORD ):
    """获取docker服务器上的运行结果存储到99本地上"""
    print("开始下载文件到本地")

    ssh = paramiko.SSHClient()#绑定一个实例
    ssh.load_system_host_keys()  # 加载known_hosts文件
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())#远程连接如果提示yes/no时，默认为yes
    ssh.connect(ip, port, user, password,allow_agent=False,look_for_keys=False)#连接远程主机
    sftp = ssh.open_sftp()
    remote_file = TESTRESULT99 + ReprotID + "/"
    CaseNames=sftp.listdir(remote_file)
    print(CaseNames)
    sftp.close()
    print("文件下载成功")

def mkdir(path):
    """创建文件夹，如果没有创建，有跳过
    """
    import os
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

def insert_db(testid,testfunction,runtime,logoinfo,createtime,teststatus,isDelete,testresult_id,ReportID,testDevice):
    """用例执行结果"""
    # 建立数据库连接
    db = pymysql.connect(
        host=MYSQLHOST,
        port=MYSQLPORT,
        user=MYSQLUSER,
        passwd=MYSQLPASSWORD,
        db=MYSQLDB
    )
    # 通过 cursor() 创建游标对象
    cursor = db.cursor()
    # 若id选择自动递增并为主键，可以设为null,让其自动增长。
    sql = """insert into airtestresultinfo (id,testid,testfunction,runtime,logoinfo,createtime,teststatus,isDelete,testresult_id,ReportID,testDevice) value(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cursor.execute(sql, (testid, testfunction, runtime,logoinfo,createtime,teststatus,isDelete,testresult_id,ReportID,testDevice))
    db.commit()
    db.close()
def insert_db_Summary(testName,TestAll,TestPass,TestFail,TestSkip,RunTime,CreateTime,isDelete):
    """插入汇总用例结果"""
    # 建立数据库连接
    db = pymysql.connect(
        host=MYSQLHOST,
        port=MYSQLPORT,
        user=MYSQLUSER,
        passwd=MYSQLPASSWORD,
        db=MYSQLDB
    )
    # 通过 cursor() 创建游标对象
    cursor = db.cursor()
    # 若id选择自动递增并为主键，可以设为null,让其自动增长。
    sql = """insert into airtestreprotlist (id,testName,TestAll,TestPass,TestFail,TestSkip,RunTime,CreateTime,isDelete) value(null,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cursor.execute(sql, (testName,TestAll,TestPass,TestFail,TestSkip,RunTime,CreateTime,isDelete))
    db.commit()
    db.close()
def SearchTestID(testName):
    db = pymysql.connect(
        host=MYSQLHOST,
        port=MYSQLPORT,
        user=MYSQLUSER,
        passwd=MYSQLPASSWORD,
        db=MYSQLDB
    )
    # 通过 cursor() 创建游标对象
    cursor = db.cursor()
    sql = "select id from airtestreprotlist WHERE testname = '%s'" %(testName)
    cursor.execute(sql)
    Result=cursor.fetchall()
    test1 = re.findall("[1-9]{1,10}", str(Result))
    print(test1[0])
    db.close()
    return test1[0]


if __name__ == '__main__':
    result=ServerCommand("ls /Muilt/Muilt/testflow/scripts/TestCase")
    num = result.split("\n")
    for i in num:
        if i=='':
            num.remove(i)