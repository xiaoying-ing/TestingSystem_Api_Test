# -*- coding:utf-8 -*-

'''
@Author  :   xiaoyin_ing

@Email   :   2455899418@qq.com

@Software:   PyCharm

@File    :   test_interfaces.py

@Time    :   2020/8/17 11:58

@Desc    :

'''
import unittest
import json
from Common.handle_create_time import handle_time
from jsonpath import jsonpath
from ddt import ddt, data
from Common.handle_logger import myLogger
from Common.handle_case_relpace_data import EnvData
from TestDatas.excel_data_obtain import test_interfaces_datas
from Common.handle_requests import set_request
from Common.handle_mysql import HandleDB
from Common.handle_conf import red_conf
from Common.handle_case_relpace_data import replace_mark_with_data
from Common.handle_random_username_email_password import get_new_interfaces_name, get_old_interfaces_name, \
    get_old_project_id, get_new_project_id, get_old_user
from Common.handle_random_username_email_password import get_new_username as get_random_str

db = HandleDB()
REPLACE_INTERFACES_NAME_MARK = "#name#"
REPLACE_INTERFACES_TESTER_MARK = "#tester#"
REPLACE_PROJECTS_ID_MARK = "#project_id#"
REPLACE_INTERFACES_DESC_MARK = "#desc#"
REPLACE_INTERFACES_ID_MARK = "#id#"
REPLACE_INTERFACES_CREATE_TIME_MARK = "#create_time#"
REPLACE_PROJECTS_NAME_MARK = "#project_name#"
REPLACE_INTERFACES_OLD_NAME_MARK = "$name$"
REPLACE_INTERFACES_OLD_PROJECT_ID_MARK = "$project_id$"

@ddt
class TestInterfaces(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        myLogger.info("==================接口模块接口测试开始==================")
        user, password = get_old_user()
        response_login = set_request("/user/login/", "post", {"username": user, "password": password})
        myLogger.info("登录的响应数据:{}".format(response_login.json()))
        setattr(EnvData, "token", jsonpath(response_login.json(), "$..token")[0])
        myLogger.info("登录用户token:{}".format(EnvData.token))

    def setUp(self) -> None:
        myLogger.info("==================接口模块接口用例执行开始==================")

    @data(*test_interfaces_datas)
    def test_interfaces(self, cases):
        self.__dict__['_testMethodDoc'] = str(cases["case_id"]) + "-" + cases["case_tittle"]
        myLogger.info("==================用例{}执行开始==================".format(str(cases["case_id"])))
        if cases['request_data'].find(REPLACE_INTERFACES_NAME_MARK) != -1 or cases['request_data'].find(
                REPLACE_INTERFACES_TESTER_MARK) != -1 or cases['request_data'].find(
            REPLACE_PROJECTS_ID_MARK) != -1 or cases[
            'request_data'].find(REPLACE_INTERFACES_DESC_MARK) != -1 or cases['request_data'].find(
            REPLACE_INTERFACES_OLD_NAME_MARK) != -1 or cases['request_data'].find(
            REPLACE_INTERFACES_OLD_PROJECT_ID_MARK) != -1:
            new_interfaces_name = get_new_interfaces_name(int(cases['random_name_len']))
            new_interfaces_tester = get_random_str(int(cases['random_tester_len']))
            new_interfaces_project_id = get_new_project_id()
            new_interfaces_desc = get_random_str(int(cases['random_desc_len']))
            old_interfaces_name = get_old_interfaces_name()
            old_interfaces_project_id = get_old_project_id()

            cases = replace_mark_with_data(cases, REPLACE_INTERFACES_NAME_MARK, new_interfaces_name)
            cases = replace_mark_with_data(cases, REPLACE_INTERFACES_TESTER_MARK, new_interfaces_tester)
            cases = replace_mark_with_data(cases, REPLACE_PROJECTS_ID_MARK, str(new_interfaces_project_id))
            cases = replace_mark_with_data(cases, REPLACE_INTERFACES_DESC_MARK, new_interfaces_desc)
            cases = replace_mark_with_data(cases, REPLACE_INTERFACES_OLD_NAME_MARK, old_interfaces_name)
            cases = replace_mark_with_data(cases, REPLACE_INTERFACES_OLD_PROJECT_ID_MARK, str(old_interfaces_project_id))
            # if cases['request_data'].find(REPLACE_PROJECTS_RENAME_MARK) != -1:
            #     cases = replace_mark_with_data(cases, REPLACE_PROJECTS_RENAME_MARK, projects_rename)

        # 发送请求
        request_data = json.loads(cases['request_data'])
        response_interfaces = set_request(cases['url'], cases['method'], request_data, token=EnvData.token)

        # 加入请求项目接口的代码
        if cases['check_sql']:
            interfaces_id = db.select_one_data(cases['check_sql'])['id']
            interfaces_create_time = db.select_one_data(cases['check_sql'])['create_time']
            project_name = db.select_one_data(cases['check_sql'])['name']
            cases = replace_mark_with_data(cases, REPLACE_INTERFACES_ID_MARK, str(interfaces_id))
            cases = replace_mark_with_data(cases, REPLACE_INTERFACES_CREATE_TIME_MARK, str(interfaces_create_time))
            cases = replace_mark_with_data(cases, REPLACE_PROJECTS_NAME_MARK, project_name)
            myLogger.info("数据替换完成")

        # 处理期望结果
        expected = json.loads(cases['expect_res'])
        try:
            if expected['create_time']:
                expected['create_time'] = handle_time(expected['create_time'])
        except KeyError:
            pass
        myLogger.info("期望结果为:{}".format(expected))
        myLogger.info("实际结果为:{}".format(response_interfaces.json()))

        # 断言
        try:
            self.assertEqual(response_interfaces.status_code, cases['status_code'])
            self.assertEqual(response_interfaces.json(), expected)

        except AssertionError:
            myLogger.info("用例执行失败")
            raise

    def tearDown(self) -> None:
        myLogger.info("==================接口模块接口用例执行结束==================")

    @classmethod
    def tearDownClass(cls) -> None:
        myLogger.info("==================接口模块接口测试结束==================")
