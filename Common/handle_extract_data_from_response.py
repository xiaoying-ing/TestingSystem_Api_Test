# -*- coding:utf-8 -*-

'''
@Author  :   xiaoyin_ing

@Email   :   2455899418@qq.com

@Software:   PyCharm

@File    :   handle_extract_data_from_response.py

@Time    :   2020/7/24 16:47

@Desc    :   从响应结果中获取数据，设置成环境变量

'''
import jsonpath
from Common.handle_case_relpace_data import EnvData


def extract_data_from_response(extract_exprs, response_dict):
    '''
    根据jsonpath提取表达式，从响应结果当中，提取数据并设置为环境变量EnvData类的类属性，作为全局变量使用。
    :param extract_exprs:从Excel当中读取出来的，提取表达式的字符串
    :param response_dict:http请求后的响应结果
    :return:
    '''
    extract_dict = eval(extract_exprs)
    for key, value in extract_dict.items():
        res = str(jsonpath.jsonpath(response_dict, value)[0])
        setattr(EnvData, key, res)