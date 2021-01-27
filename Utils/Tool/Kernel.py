
import traceback
import datetime


# 核心类
class Kernel():
    AbnormalRerun = 0  # 异常重运行次数
    FailureCase = [] # 失败用例list
