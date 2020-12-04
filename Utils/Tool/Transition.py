# coding=utf-8
import time
import json
import demjson
from Utils.Tool.CJsonEncoder import DecimalEncoder


class Transition():
        #转换类
        @staticmethod
        def JsonTurnDictionary(json_response):
            """
            json转字典
            param json_response:json
            return  dictionary：字典
            """
            dict_json = demjson.decode(str(json_response))  # 将json字符串转换成dic字典对象
            return dict_json

        @staticmethod
        def DictionaryTurnJsonSerialize(dictionary):
            """
            字典转json(处理序列化问题)
            param dictionary:字典
            return  str_json：json
            """
            str_json = json.dumps(dictionary, cls=DecimalEncoder)  # 将字典转换成json
            return str_json