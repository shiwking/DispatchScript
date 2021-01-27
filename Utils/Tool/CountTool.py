# coding=utf-8
import decimal


class CountTool():
    #计算 类

    @staticmethod
    def add(value1, value2, keepDecimal):
        """
        数值相加
        param value1: 数值2
        param value2: 数值2
        param keepDecimal: 保留小数位  %.0f 整数  %.3f 保留3位小数
        return 值
        """
        return  (keepDecimal % decimal.Decimal(value1) + decimal.Decimal(value2))

    @staticmethod
    def multiply(value1, value2, keepDecimal):
        """
        数值相乘
        param value1: 数值2
        param value2: 数值2
        param keepDecimal: 保留小数位  %.0f 整数  %.3f 保留3位小数
        return 值
        """
        return (keepDecimal % (decimal.Decimal(value1) * decimal.Decimal(value2)))  # 相乘后保留0位小数

    @staticmethod
    def subAbs(value1, value2, keepDecimal):
        """
        相减
        param value1: 数值2
        param value2: 数值2
        param keepDecimal: 保留小数位  %.0f 整数  %.3f 保留3位小数
        return 值
        """
        return (keepDecimal % abs(decimal.Decimal(value1) - decimal.Decimal(value2)))  # 绝对值后保留3位小数

    @staticmethod
    def divide(value1, value2, keepDecimal):
        """
        相除
        param value1: 数值2
        param value2: 数值2
        param keepDecimal: 保留小数位  %.0f 整数  %.3f 保留3位小数
        return 值
        """
        return (keepDecimal % (decimal.Decimal(value1) / decimal.Decimal(value2)))  # 除后保留3位小数

    @staticmethod
    def round_up(value):
        """
        替换内置round函数,实现保留2位小数的精确四舍五入
        :param value: 需转换数值
        """
        return round(value * 1000) / 1000.0

    @staticmethod
    def getListAverage(list):
        """
        获取列表平均值
        :param list: 列表
        """
        import decimal
        lenght = len(list)  # 列表长度
        sum = 0
        for i in list:
            sum = decimal.Decimal(sum) + decimal.Decimal(i)
        return ('%.3f' % (decimal.Decimal(sum) / decimal.Decimal(lenght)))  # 除后保留3位小数