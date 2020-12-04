import decimal
import json
from datetime import date, datetime,timedelta

class CJsonEncoder(json.JSONEncoder):
#解决python中转化成json的方法不能序列化datetime类型数据
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, timedelta):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)