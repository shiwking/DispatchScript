import re
import pymysql
from Setting import *
def readReportID():
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
    sql = """SELECT MAX(id) AS max_score FROM airtestreprotlist;"""
    cursor.execute(sql)
    db.commit()
    testdata = str(cursor.fetchone())
    test = re.findall(r"\d+", testdata)
    Lowlast_line=str(test[0])
    reprotID=str(int(Lowlast_line)+1)
    print(reprotID)
    db.close()
    return reprotID


if __name__ == '__main__':

    readReportID()
