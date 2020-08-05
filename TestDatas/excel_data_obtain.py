# -*- coding:utf-8 -*-

'''
@Author  :   xiaoyin_ing

@Email   :   2455899418@qq.com

@Software:   PyCharm

@File    :   data_obtain.py

@Time    :   2020/7/3 11:20

@Desc    :

'''
from Common.handle_excel import HandleExcel
from Common.handle_path import test_datas_dir
from pprint import pprint
import os


class read_test_datas:
    def __init__(self, table_name, sheet_name):
        self.sheet_names = sheet_name
        self.table_name = table_name

    def obtain_datas(self):
        case_path = os.path.join(test_datas_dir, self.table_name)
        case_datas = HandleExcel(case_path, self.sheet_names)
        case_all_datas = case_datas.read_test_cases_datas()
        case_datas.close_file()
        return case_all_datas


test_table_name = "TestSystem_api_Testcase.xlsx"
sheet_name_list = ["register", "isregister"]
test_register = read_test_datas(test_table_name, sheet_name_list[0])
test_register_datas = test_register.obtain_datas()

test_isregister = read_test_datas(test_table_name, sheet_name_list[1])
test_isregister_datas = test_isregister.obtain_datas()

if __name__ == '__main__':
    from Common.handle_random_username_email_password import get_new_email, get_password, get_new_username
    from Common.handle_case_relpace_data import replace_mark_with_data
    from Common.handle_conf import red_conf
    REPLACE_NOREGISTER_USERNAME = "#username#"
    REPLACE_REGISTER_USERNAME = "$username$"
    # REPLACE_PASSWORD = "#password#"
    # REPLACE_EMAIL = "#email#"
    # REPLACE_ID = "#id#"
    # pprint(test_isregister_datas)
    case = test_isregister_datas
    for cases in case:
        if cases["url"].find(REPLACE_NOREGISTER_USERNAME) != -1:
            username = get_new_username(int(cases["random_username_len"]))
    #         password = get_password(int(cases["random_password_len"]))
    #         email = get_new_email()
            cases = replace_mark_with_data(cases, REPLACE_NOREGISTER_USERNAME, username)
    #         cases = replace_mark_with_data(cases, REPLACE_PASSWORD, password)
    #         cases = replace_mark_with_data(cases, REPLACE_EMAIL, email)
        elif cases["url"].find(REPLACE_REGISTER_USERNAME) != -1:
            username = red_conf.get("register_user", "username")
            cases = replace_mark_with_data(cases, REPLACE_REGISTER_USERNAME, username)
        else:
            pass
    pprint(case)