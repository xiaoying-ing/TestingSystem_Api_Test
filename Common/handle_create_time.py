# -*- coding:utf-8 -*-

'''
@Author  :   xiaoyin_ing

@Email   :   2455899418@qq.com

@Software:   PyCharm

@File    :   handle_create_time.py

@Time    :   2020/8/14 10:53

@Desc    :

'''


def handle_time(expected_time):
    fir_time_str = expected_time.replace(" ", "T")
    sen_time_str = fir_time_str + "+08:00"
    mark = sen_time_str[sen_time_str.index("T") + 1] + sen_time_str[sen_time_str.index("T") + 2]
    replace_time_str = str(int(mark) + 8)
    sen_time_str_list = list(sen_time_str)
    sen_time_str_list[11], sen_time_str_list[12] = replace_time_str[0], replace_time_str[1]
    fin_time_str = "".join(sen_time_str_list)
    return fin_time_str
