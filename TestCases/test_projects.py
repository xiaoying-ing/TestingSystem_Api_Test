# -*- coding:utf-8 -*-

'''
@Author  :   xiaoyin_ing

@Email   :   2455899418@qq.com

@Software:   PyCharm

@File    :   test_projects.py

@Time    :   2020/8/13 15:55

@Desc    :

'''
import unittest
import json
from Common.handle_create_time import handle_time
from jsonpath import jsonpath
from ddt import ddt, data
from Common.handle_logger import myLogger
from Common.handle_case_relpace_data import EnvData
from TestDatas.excel_data_obtain import test_projects_datas
from Common.handle_requests import set_request
from Common.handle_mysql import HandleDB
from Common.handle_conf import red_conf
from Common.handle_case_relpace_data import replace_mark_with_data
from Common.handle_random_username_email_password import get_new_projects_datas, get_old_user

db = HandleDB()
REPLACE_PROJECTS_NAME_MARK = "#name#"
REPLACE_PROJECTS_LEADER_MARK = "#leader#"
REPLACE_PROJECTS_TESTER_MARK = "#tester#"
REPLACE_PROJECTS_PROGRAMMER_MARK = "#programmer#"
REPLACE_PROJECTS_PUBLISH_APP_MARK = "#app#"
REPLACE_PROJECTS_DESC_MARK = "#desc#"
REPLACE_PROJECTS_DB_ID_MARK = "#id#"
REPLACE_PROJECTS_DB_GREATE_TIME_MARK = "#create_time#"
REPLACE_PROJECTS_RENAME_MARK = "$name$"

@ddt
class TestProjects(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        myLogger.info("==================项目接口测试开始==================")
        user, password = get_old_user()
        response_login = set_request("/user/login/", "post", {"username": user, "password": password})
        myLogger.info("登录的响应数据:{}".format(response_login.json()))
        setattr(EnvData, "token", jsonpath(response_login.json(), "$..token")[0])
        myLogger.info("登录用户token:{}".format(EnvData.token))

    def setUp(self) -> None:
        myLogger.info("==================项目接口测试用例执行开始==================")

    @data(*test_projects_datas)
    def test_projects(self, cases):
        self.__dict__['_testMethodDoc'] = str(cases["case_id"]) + "-" + cases["case_tittle"]
        myLogger.info("==================用例{}执行开始==================".format(str(cases["case_id"])))
        projects_rename = red_conf.get("project", "name")

        # 以请求数据中的数据标记为源头，初步替换真实数据
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

        # 发送请求
        request_data = json.loads(cases['request_data'])
        response_projects = set_request(cases['url'], cases['method'], request_data, token=EnvData.token)

        # 继续替换期望结果中的数据为真实数据
        if cases['check_sql']:
            project_id = db.select_one_data(cases['check_sql'])['id']
            project_create_time = db.select_one_data(cases['check_sql'])['create_time']
            cases = replace_mark_with_data(cases, REPLACE_PROJECTS_DB_ID_MARK, str(project_id))
            cases = replace_mark_with_data(cases, REPLACE_PROJECTS_DB_GREATE_TIME_MARK, str(project_create_time))
            myLogger.info("数据替换完毕")

        # 处理期望结果
        expected = json.loads(cases['expect_res'])
        try:
            if expected['create_time']:
                expected['create_time'] = handle_time(expected['create_time'])
        except KeyError:
            pass
        myLogger.info("期望结果为:{}".format(expected))
        myLogger.info("实际结果为:{}".format(response_projects.json()))

        # 断言
        try:
            self.assertEqual(response_projects.status_code, cases['status_code'])
            self.assertEqual(response_projects.json(), expected)

        except AssertionError:
            myLogger.info("用例执行失败")
            raise

    def tearDown(self) -> None:
        myLogger.info("==================项目接口用例执行结束==================")

    @classmethod
    def tearDownClass(cls) -> None:
        myLogger.info("==================项目接口测试结束==================")
