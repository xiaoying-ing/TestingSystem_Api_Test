# -*- coding:utf-8 -*-

'''
@Author  :   xiaoyin_ing

@Email   :   2455899418@qq.com

@Software:   PyCharm

@File    :   test_is_email_register.py

@Time    :   2020/8/6 15:38

@Desc    :

'''
import unittest
import json
from ddt import ddt, data
from Common.handle_logger import myLogger
from TestDatas.excel_data_obtain import test_is_email_register_datas
from Common.handle_requests import set_request
from Common.handle_mysql import HandleDB
from Common.handle_case_relpace_data import replace_mark_with_data
from Common.handle_random_username_email_password import get_new_email
from Common.handle_conf import red_conf

db = HandleDB()
REPLACE_NOREGISTER_EMAIL_MARK = "#email#"
REPLACE_REGISTER_EMAIL_MARK = "$email$"

@ddt
class TestIsEmailRegister(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        myLogger.info("==================确认邮箱注册模块接口测试开始==================")

    def setUp(self) -> None:
        myLogger.info("==================接口用例执行开始==================")

    @data(*test_is_email_register_datas)
    def test_is_email_register(self, cases):
        self.__dict__['_testMethodDoc'] = str(cases["case_id"]) + "-" + cases["case_tittle"]
        myLogger.info("==================用例{}执行开始==================".format(str(cases["case_id"])))
        if cases["url"].find(REPLACE_NOREGISTER_EMAIL_MARK) != -1:
            email = get_new_email()
            cases = replace_mark_with_data(cases, REPLACE_NOREGISTER_EMAIL_MARK, email)
        elif cases["url"].find(REPLACE_REGISTER_EMAIL_MARK) != -1:
            email = red_conf.get("register_user", "email")
            cases = replace_mark_with_data(cases, REPLACE_REGISTER_EMAIL_MARK, email)
        else:
            pass
        response_is_email_register = set_request(cases["url"], cases["method"])
        myLogger.info("实际结果为：{}".format(response_is_email_register.json()))

        expected = json.loads(cases["expect_res"])
        myLogger.info("期望结果为：{}".format(expected))

        # 断言
        try:
            self.assertEqual(response_is_email_register.status_code, cases['status_code'])
            self.assertEqual(response_is_email_register.json()["email"], expected["email"])
            self.assertEqual(response_is_email_register.json()["count"], expected["count"])
        except AssertionError:
            myLogger.info("用例执行失败")
            raise
        myLogger.info("==================用例结束==================")

    def tearDown(self) -> None:
        myLogger.info("==================接口用例执行结束==================")

    @classmethod
    def tearDownClass(cls) -> None:
        myLogger.info("==================确认邮箱注册模块接口测试结束==================")
