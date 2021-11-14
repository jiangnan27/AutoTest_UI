#! /usr/bin/python
# -*- coding:utf-8 -*-
# 所有的工具类方法，此中不允许私自修改

import hashlib
import random
import re
import time
import ast
from jsonschema import validate, draft7_format_checker
from jsonschema.exceptions import SchemaError, ValidationError
from utils.my_logger import log


class __AddValue:
    """
    反射机制
    用来设置全局变量
    """
    var = None


def my_hasattr(attr_name: str):
    """
    判断是否有全局变量
    :param attr_name: 全局变量名
    :return: bool值
    """
    return hasattr(__AddValue, attr_name)


def my_setattr(attr_name: str, attr_value):
    """
    设置全局变量
    :param attr_name:全局变量名
    :param attr_value: 全局变量值
    """
    setattr(__AddValue, attr_name, attr_value)


def my_getattr(attr_name: str, default=None, print_error=False):
    """
    引用全局变量
    :param attr_name: 全局变量名
    :param default: 默认返回值
    :param print_error: 是否需要打印error信息
    :return: 全局变量值
    """
    got_data = None
    if '.' in attr_name:
        from core.api.samples import get_json
        got_data = get_json(attr_name)
    if not got_data:
        if not hasattr(__AddValue, attr_name):
            if default is not None:
                if print_error:
                    log.warning(f'not found \"{attr_name}\", user defined return {default}')
                return default
            else:
                if print_error:
                    log.warning(f'not found \"{attr_name}\", default return {default}')
                return None
        else:
            got_data = getattr(__AddValue, attr_name)
    return got_data


def safe_eval(data):
    try:
        result = ast.literal_eval(data)
        return result
    except Exception as e:
        # log.warning(f'safe_eval is errored: {e.args}')
        return data


def my_delattr(attr_name: str):
    """
    删除全局变量
    :param attr_name: 全局变量名
    """
    if hasattr(__AddValue, attr_name):
        delattr(__AddValue, attr_name)


def my_random_int(min_num: int = 0, max_num: int = 999):
    """
    随机整数
    :param min_num: 最小数
    :param max_num: 最大数
    :return: 随机整数
    """
    return random.randint(min_num, max_num)


def my_random_float(min_num: int, max_num: int, decimal_count: int = None):
    """随机浮点数，可以选择精度"""
    result = random.uniform(min_num, max_num)
    if decimal_count:
        return round(result, decimal_count)
    else:
        return result


def my_random_str(str_count: int):
    """随机数量的字符串"""
    if str_count <= 10000:
        res = ''
        for i in range(str_count):
            rand_str = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
            res += rand_str
        return res
    else:
        raise Exception('"random_str" 限制最高 10000 个')


def my_get_now(time_format='%Y-%m-%d %H:%M:%S', num: int = 0):
    """
    获取现在的完整时间
    :param time_format: 时间格式
    :param num: 前推/后推（秒）
    """
    return time.strftime(time_format, time.localtime(time.time() + num))


def my_get_date(time_format='%Y-%m-%d', num: int or float = 0):
    """获取日期
    :param time_format: 时间格式
    :param num: 前推/后推（天）
    """
    return time.strftime(time_format, time.localtime(time.time() + num*3600*24))


def my_get_time(time_format='%H:%M:%S', num: int = 0):
    """获取时间
    :param time_format: 时间格式
    :param num: 前推/后推（秒）
    """
    return time.strftime(time_format, time.localtime(time.time() + num))


def my_md5(text):
    """MD5加密"""
    m1 = hashlib.md5()
    m1.update(text.encode('utf-8'))
    md5_str = m1.hexdigest()
    return md5_str


def my_remove_spaces(text):
    """祛除所有空格"""
    pattern = re.compile(r'\s+')
    return re.sub(pattern, "", text)


def my_retain_int(value):
    """只保留数字"""
    return int(re.sub(r'[^\d]+', '', value))


def my_del_symbol(value):
    """
    祛除所有非中文和英文和阿拉字符
    例如： 符号、空格、换行符等等
    """
    return re.sub(r'[^\w\u4e00-\u9fff]+', '', value)


def my_schema(schema_data: dict, validate_data: dict):
    def _get_error_path(error_path: list):
        b = ''
        for v in error_path:
            if isinstance(v, int):
                b += str(f'[{v}]')
            elif v == error_path[0]:
                b += str(v)
            else:
                b += str('.' + v)
        return b

    try:
        validate(instance=validate_data, schema=schema_data, format_checker=draft7_format_checker)
        return validate_data
    except SchemaError as e:
        log.error("验证模式schema出错：\n\t出错位置：{}\n\t提示信息：{}".format("data."+_get_error_path(e.path), e.message))
        log.error(schema_data)
        raise e
    except ValidationError as e:
        log.error("json数据不符合schema规定：\n\t出错字段：{}\n\t提示信息：{}".format("data."+_get_error_path(e.path), e.message))
        log.error(validate_data)
        raise e
