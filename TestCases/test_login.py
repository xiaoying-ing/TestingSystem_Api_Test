# -*- coding:utf-8 -*-

'''
@Author  :   xiaoyin_ing

@Email   :   2455899418@qq.com

@Software:   PyCharm

@File    :   test_login.py

@Time    :   2020/8/7 13:48

@Desc    :

'''
import unittest
import json
from ddt import ddt, data
from Common.handle_logger import myLogger
from TestDatas.excel_data_obtain import test_login_datas
from Common.handle_requests import set_request
from Common.handle_mysql import HandleDB
from Common.handle_conf import red_conf
from Common.handle_case_relpace_data import replace_mark_with_data
from Common.handle_random_username_email_password import get_new_username, get_password

db = HandleDB()
REPLACE_NO_REGISTER_USERNAME_MARK = "#username#"
REPLACE_NO_REGISTER_PASSWORD_MARK = "#password#"
REPLACE_REGISTER_USERNAME_MARK = "$username$"
REPLACE_REGISTER_PASSWORD_MARK = "$password$"
REPLACE_USER_ID_MARK = "$user_id$"

@ddt
class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        myLogger.info("==================登录模块接口测试开始==================")

    def setUp(self) -> None:
        myLogger.info("==================接口用例执行开始==================")

    @data(*test_login_datas)
    def test_login(self,cases):
        self.__dict__['_testMethodDoc'] = str(cases["case_id"]) + "-" + cases["case_tittle"]
        myLogger.info("==================用例{}执行开始==================".format(str(cases["case_id"])))
        register_username = red_conf.get("register_user", "username")
        register_password = red_conf.get("register_user", "password")
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
            myLogger.info("替换后的最终测试数据:{}".format(cases))

        expected = json.loads(cases['expect_res'])
        myLogger.info("预期结果:{}".format(expected))

        request_data = json.loads(cases['request_data'])
        response_login = set_request(cases['url'], cases["method"], request_data)
        myLogger.info("实际结果:{}".format(response_login.json()))

        # 断言
        try:
            self.assertEqual(response_login.status_code, cases['status_code'])
            if cases['check_sql']:
                self.assertIsNotNone(response_login.json()["token"])
                self.assertEqual(response_login.json()["user_id"], expected["user_id"])
                self.assertEqual(response_login.json()["username"], expected["username"])
                try:
                    if expected["non_field_errors"]:
                        self.assertEqual(response_login.json()["non_field_errors"], expected["non_field_errors"])
                    elif expected["username"]:
                        self.assertEqual(response_login.json()["username"], expected["username"])
                    elif expected["passwprd"]:
                        self.assertEqual(response_login.json()["password"], expected["password"])
                except KeyError:
                    pass

        except AssertionError:
            myLogger.info("用例执行失败")
            raise

    def tearDown(self) -> None:
        myLogger.info("==================接口用例执行结束==================")

    @classmethod
    def tearDownClass(cls) -> None:
        myLogger.info("==================注册模块接口测试结束==================")

