# -*- coding:utf-8 -*-

'''
@Author  :   xiaoyin_ing

@Email   :   2455899418@qq.com

@Software:   PyCharm

@File    :   test_register.py

@Time    :   2020/8/3 17:55

@Desc    :

'''
import unittest
import json
from ddt import ddt, data
from Common.handle_logger import myLogger
from TestDatas.excel_data_obtain import test_register_datas
from Common.handle_requests import set_request
from Common.handle_mysql import HandleDB
from Common.handle_case_relpace_data import replace_mark_with_data
from Common.handle_random_username_email_password import get_new_username, get_password, get_new_email

db = HandleDB()
REPLACE_USERNAME = "#username#"
REPLACE_PASSWORD = "#password#"
REPLACE_EMAIL = "#email#"
REPLACE_ID = "#id#"

@ddt
class TestRegister(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        myLogger.info("==================注册模块接口测试开始==================")

    def setUp(self) -> None:
        myLogger.info("==================接口用例执行开始==================")

    @data(*test_register_datas)
    def test_register(self, cases):
        self.__dict__['_testMethodDoc'] = str(cases["case_id"]) + "-" + cases["case_tittle"]
        myLogger.info("==================用例{}执行开始==================".format(str(cases["case_id"])))
        if cases["request_data"].find("#username#") != -1 or cases["request_data"].find("#password#") or cases["request_data"].find("#email#") != -1:
            username = get_new_username(int(cases["random_username_len"]))
            password = get_password(int(cases["random_password_len"]))
            email = get_new_email()
            cases = replace_mark_with_data(cases, REPLACE_USERNAME, username)
            cases = replace_mark_with_data(cases, REPLACE_PASSWORD, password)
            cases = replace_mark_with_data(cases, REPLACE_EMAIL, email)

        response_register = set_request(cases["url"], cases["method"], cases["request_data"])
        myLogger.info("实际结果为：{}".format(response_register.json()))
        if cases["check_sql"]:
            user_id = db.select_one_data(cases["check_sql"])["id"]
            cases = replace_mark_with_data(cases, REPLACE_ID, str(user_id))
            myLogger.info("最终的测试数据为：{}".format(cases))
        expected = json.loads(cases['expect_res'])
        myLogger.info("期望结果为：{}".format(expected))

        # 断言
        try:
            self.assertEqual(response_register.status_code, cases['status_code'])
            if cases["check_sql"]:
                self.assertEqual(response_register.json()["id"], int(expected["id"]))
                self.assertEqual(response_register.json()["username"], expected["username"])
        except AssertionError:
            myLogger.info("用例执行失败")
            raise
        myLogger.info("==================用例结束==================")

    def tearDown(self) -> None:
        myLogger.info("==================接口用例执行结束==================")

    @classmethod
    def tearDownClass(cls) -> None:
        myLogger.info("==================注册模块接口测试结束==================")


