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
sheet_name_list = ["register", "isregister", "is_email_register", "login"]
test_register = read_test_datas(test_table_name, sheet_name_list[0])
test_register_datas = test_register.obtain_datas()

test_isregister = read_test_datas(test_table_name, sheet_name_list[1])
test_isregister_datas = test_isregister.obtain_datas()

test_is_email_register = read_test_datas(test_table_name, sheet_name_list[2])
test_is_email_register_datas = test_is_email_register.obtain_datas()

test_login = read_test_datas(test_table_name, sheet_name_list[3])
test_login_datas = test_login.obtain_datas()
if __name__ == '__main__':
    from Common.handle_random_username_email_password import get_new_email, get_password, get_new_username
    from Common.handle_case_relpace_data import replace_mark_with_data
    from Common.handle_conf import red_conf
    from Common.handle_db import HandleDB
    REPLACE_NO_REGISTER_USERNAME_MARK = "#username#"
    REPLACE_NO_REGISTER_PASSWORD_MARK = "#password#"
    REPLACE_REGISTER_USERNAME_MARK = "$username$"
    REPLACE_REGISTER_PASSWORD_MARK = "$password$"
    REPLACE_USER_ID_MARK = "$user_id$"
    case = test_login_datas
    # pprint(cases)
    register_username = red_conf.get("register_user", "username")
    register_password = red_conf.get("register_user", "password")
    db = HandleDB()
    for cases in case:
        if cases["request_data"].find(REPLACE_REGISTER_USERNAME_MARK) != -1 or cases["request_data"].find(
                REPLACE_REGISTER_PASSWORD_MARK) != -1 or cases["request_data"].find(REPLACE_NO_REGISTER_USERNAME_MARK) \
                != -1 or cases["request_data"].find(REPLACE_NO_REGISTER_PASSWORD_MARK) != -1:
            no_register_username = get_new_username(int(cases['random_username_len']))
            no_register_password = get_password(int(cases['random_password_len']))
            cases = replace_mark_with_data(cases, REPLACE_REGISTER_USERNAME_MARK, register_username)
            cases = replace_mark_with_data(cases, REPLACE_REGISTER_PASSWORD_MARK, register_password)
            cases = replace_mark_with_data(cases, REPLACE_NO_REGISTER_USERNAME_MARK, no_register_username)
            cases = replace_mark_with_data(cases, REPLACE_NO_REGISTER_PASSWORD_MARK, no_register_password)
        if cases['check_sql']:
            user_id = db.select_one_data(cases['check_sql'])["id"]
            cases = replace_mark_with_data(cases, REPLACE_USER_ID_MARK, str(user_id))
    pprint(case)