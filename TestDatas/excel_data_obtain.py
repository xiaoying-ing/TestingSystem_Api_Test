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
sheet_name_list = ["register", "isregister", "is_email_register", "login", "projects"]
test_register = read_test_datas(test_table_name, sheet_name_list[0])
test_register_datas = test_register.obtain_datas()

test_isregister = read_test_datas(test_table_name, sheet_name_list[1])
test_isregister_datas = test_isregister.obtain_datas()

test_is_email_register = read_test_datas(test_table_name, sheet_name_list[2])
test_is_email_register_datas = test_is_email_register.obtain_datas()

test_login = read_test_datas(test_table_name, sheet_name_list[3])
test_login_datas = test_login.obtain_datas()

test_projects = read_test_datas(test_table_name, sheet_name_list[4])
test_projects_datas = test_projects.obtain_datas()
if __name__ == '__main__':
    # 登录模块数据替换测试 from Common.handle_random_username_email_password import get_new_email, get_password,
    # get_new_username from Common.handle_case_relpace_data import replace_mark_with_data from Common.handle_conf
    # import red_conf from Common.handle_db import HandleDB REPLACE_NO_REGISTER_USERNAME_MARK = "#username#"
    # REPLACE_NO_REGISTER_PASSWORD_MARK = "#password#" REPLACE_REGISTER_USERNAME_MARK = "$username$"
    # REPLACE_REGISTER_PASSWORD_MARK = "$password$" REPLACE_USER_ID_MARK = "$user_id$" case = test_login_datas #
    # pprint(cases) register_username = red_conf.get("register_user", "username") register_password = red_conf.get(
    # "register_user", "password") db = HandleDB() for cases in case: if cases["request_data"].find(
    # REPLACE_REGISTER_USERNAME_MARK) != -1 or cases["request_data"].find( REPLACE_REGISTER_PASSWORD_MARK) != -1 or
    # cases["request_data"].find(REPLACE_NO_REGISTER_USERNAME_MARK) \ != -1 or cases["request_data"].find(
    # REPLACE_NO_REGISTER_PASSWORD_MARK) != -1: no_register_username = get_new_username(int(cases[
    # 'random_username_len'])) no_register_password = get_password(int(cases['random_password_len'])) cases =
    # replace_mark_with_data(cases, REPLACE_REGISTER_USERNAME_MARK, register_username) cases =
    # replace_mark_with_data(cases, REPLACE_REGISTER_PASSWORD_MARK, register_password) cases =
    # replace_mark_with_data(cases, REPLACE_NO_REGISTER_USERNAME_MARK, no_register_username) cases =
    # replace_mark_with_data(cases, REPLACE_NO_REGISTER_PASSWORD_MARK, no_register_password) if cases['check_sql']:
    # user_id = db.select_one_data(cases['check_sql'])["id"] cases = replace_mark_with_data(cases,
    # REPLACE_USER_ID_MARK, str(user_id)) pprint(case)

    # 项目模块数据替换测试
    from Common.handle_random_username_email_password import get_new_projects_datas
    from Common.handle_random_username_email_password import get_old_user
    from Common.handle_case_relpace_data import replace_mark_with_data
    from Common.handle_requests import set_request
    from Common.handle_conf import red_conf
    from Common.handle_db import HandleDB

    REPLACE_PROJECTS_NAME_MARK = "#name#"
    REPLACE_PROJECTS_LEADER_MARK = "#leader#"
    REPLACE_PROJECTS_TESTER_MARK = "#tester#"
    REPLACE_PROJECTS_PROGRAMMER_MARK = "#programmer#"
    REPLACE_PROJECTS_PUBLISH_APP_MARK = "#app#"
    REPLACE_PROJECTS_DESC_MARK = "#desc#"
    REPLACE_PROJECTS_DB_ID_MARK = "#id#"
    REPLACE_PROJECTS_DB_GREATE_TIME_MARK = "#create_time#"
    REPLACE_PROJECTS_RENAME_MARK = "$name$"
    # 请求登录接口
    user, password = get_old_user()
    response_login = set_request("/user/login/", "post", {"username": user, "password": password})
    token = response_login.json()["token"]
    # print(test_projects_datas)
    case = test_projects_datas
    db = HandleDB()

    projects_rename = red_conf.get("project", "name")
    for cases in case:
        if cases['request_data'].find(REPLACE_PROJECTS_NAME_MARK) != -1 or cases['request_data'].find(
                REPLACE_PROJECTS_LEADER_MARK) != -1 or cases['request_data'].find(
            REPLACE_PROJECTS_TESTER_MARK) != -1 or cases[
            'request_data'].find(REPLACE_PROJECTS_PROGRAMMER_MARK) != -1 or cases['request_data'].find(
            REPLACE_PROJECTS_PUBLISH_APP_MARK) != -1 or cases['request_data'].find(
            REPLACE_PROJECTS_DESC_MARK) != -1:
            name = get_new_projects_datas(int(cases['random_name_len']))
            leader = get_new_projects_datas(int(cases['random_leader_len']))
            tester = get_new_projects_datas(int(cases['random_tester_len']))
            programmer = get_new_projects_datas(int(cases['random_programmer_len']))
            publish_app = get_new_projects_datas(int(cases['random_publish_app_len']))
            desc = get_new_projects_datas(int(cases['random_desc_len']))
            cases = replace_mark_with_data(cases, REPLACE_PROJECTS_NAME_MARK, name)
            cases = replace_mark_with_data(cases, REPLACE_PROJECTS_LEADER_MARK, leader)
            cases = replace_mark_with_data(cases, REPLACE_PROJECTS_TESTER_MARK, tester)
            cases = replace_mark_with_data(cases, REPLACE_PROJECTS_PROGRAMMER_MARK, programmer)
            cases = replace_mark_with_data(cases, REPLACE_PROJECTS_PUBLISH_APP_MARK, publish_app)
            cases = replace_mark_with_data(cases, REPLACE_PROJECTS_DESC_MARK, desc)
            if cases['request_data'].find(REPLACE_PROJECTS_RENAME_MARK) != -1:
                cases = replace_mark_with_data(cases, REPLACE_PROJECTS_RENAME_MARK, projects_rename)

        # 加入请求项目接口的代码
        if cases['check_sql']:
            project_id = db.select_one_data(cases['check_sql'])['id']
            project_create_time = db.select_one_data(cases['check_sql'])['create_time']
            cases = replace_mark_with_data(cases, REPLACE_PROJECTS_DB_ID_MARK, project_id)
            cases = replace_mark_with_data(cases, REPLACE_PROJECTS_DB_GREATE_TIME_MARK, project_create_time)
    print(case)



