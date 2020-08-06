# -*- coding:utf-8 -*-

'''
@Author  :   xiaoyin_ing

@Email   :   2455899418@qq.com

@Software:   PyCharm

@File    :   test_isregister.py

@Time    :   2020/8/5 10:04

@Desc    :

'''
import unittest
import json
from ddt import ddt, data
from Common.handle_logger import myLogger
from TestDatas.excel_data_obtain import test_isregister_datas
from Common.handle_requests import set_request
from Common.handle_mysql import HandleDB
from Common.handle_case_relpace_data import replace_mark_with_data
from Common.handle_random_username_email_password import get_new_username
from Common.handle_conf import red_conf

db = HandleDB()
REPLACE_NOREGISTER_USERNAME_MARK = "#username#"
REPLACE_REGISTER_USERNAME_MARK = "$username$"

@ddt
class TestIsRegister(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        myLogger.info("==================确认用户注册模块接口测试开始==================")
        register_username = red_conf.get("register_user", "username")
        register_email = red_conf.get("register_user", "email")
        register_pwd = red_conf.get("register_user", "password")
        request_register_data = {"username": register_username, "email": register_email, "password": register_pwd, "password_confirm": register_pwd}
        register_url = "/user/register/"
        set_request(register_url, "POST", request_register_data)

    def setUp(self) -> None:
        myLogger.info("==================接口用例执行开始==================")

    @data(*test_isregister_datas)
    def test_isregitser(self, cases):
        self.__dict__['_testMethodDoc'] = str(cases["case_id"]) + "-" + cases["case_tittle"]
        myLogger.info("==================用例{}执行开始==================".format(str(cases["case_id"])))
        if cases["url"].find(REPLACE_NOREGISTER_USERNAME_MARK) != -1:
            username = get_new_username(int(cases["random_username_len"]))
            cases = replace_mark_with_data(cases, REPLACE_NOREGISTER_USERNAME_MARK, username)
        elif cases["url"].find(REPLACE_REGISTER_USERNAME_MARK) != -1:
            username = red_conf.get("register_user", "username")
            cases = replace_mark_with_data(cases, REPLACE_REGISTER_USERNAME_MARK, username)
        else:
            pass

        response_isregister = set_request(cases["url"], cases["method"])
        myLogger.info("实际结果为：{}".format(response_isregister.json()))

        expected = json.loads(cases["expect_res"])
        myLogger.info("期望结果为：{}".format(expected))

        # 断言
        try:
            self.assertEqual(response_isregister.status_code, cases['status_code'])
            self.assertEqual(response_isregister.json()["username"], expected["username"])
            self.assertEqual(response_isregister.json()["count"], expected["count"])
        except AssertionError:
            myLogger.info("用例执行失败")
            raise
        myLogger.info("==================用例结束==================")

    def tearDown(self) -> None:
        myLogger.info("==================接口用例执行结束==================")

    @classmethod
    def tearDownClass(cls) -> None:
        myLogger.info("==================确认用户注册模块接口测试结束==================")




