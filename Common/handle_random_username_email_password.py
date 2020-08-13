# -*- coding:utf-8 -*-

'''
@Author  :   xiaoyin_ing

@Email   :   2455899418@qq.com

@Software:   PyCharm

@File    :   handle_phone.py

@Time    :   2020/7/6 15:49

@Desc    :

'''
import random
from Common.handle_mysql import HandleDB


def get_new_username(username_len):
    db = HandleDB()
    while True:
        username = __generator_string(username_len)
        count = db.get_count('select * from auth_user where username="{}"'.format(username))
        if count == 0:
            db.close()
            return username


def get_password(password_len):
    password = __generator_string(password_len)
    return password


def get_new_projects_datas(datas_len):
    db = HandleDB()
    while True:
        datas = __generator_string(datas_len)
        count = db.get_count('SELECT * FROM tb_projects WHERE name="{}"'.format(datas))
        if count == 0:
            db.close()
            return datas


def get_new_email():
    db = HandleDB()
    while True:
        # 1生成
        email = __generator_email()
        # 2校验，有
        count = db.get_count('select * from auth_user where email="{}"'.format(email))
        if count == 0:  # 如果email没有在数据库查到。表示是未注册的email。
            db.close()
            return email


def get_old_user():
    '''
    从配置文件获取指定的用户名和密码
    确保此帐号，在系统当中是注册了的。
    返回：用户名和密码。
    :return:
    '''
    from Common.handle_conf import red_conf
    from Common.handle_requests import set_request
    user = red_conf.get("register_user", "username")
    password = red_conf.get("register_user", "password")
    email = red_conf.get("register_user", "email")
    # 如果数据库查找到user，就直接返回。如果没有，则调用注册接口注册一个。
    # 不管注册与否，直接调用注册接口。
    set_request("/user/register/", "post", {"username": user, "email": email, "password": password, "password_confirm": password})
    return user, password


def __generator_string(length):
    all_str = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    random_string_list = []
    for _ in range(length):
        random_string_list.append(random.choice(all_str))
    random_string = "".join(random_string_list)
    return random_string


def __generator_email(emailType=None, rang=None):
    __email_type = ["@qq.com", "@163.com", "@126.com", "@189.com"]
    # 如果没有指定邮箱类型，默认在 __emailtype中随机一个
    if emailType is None:
        __randomEmail = random.choice(__email_type)
    else:
        __randomEmail = emailType
    # 如果没有指定邮箱长度，默认在4-10之间随机
    if rang is None:
        __rang = random.randint(4, 10)
    else:
        __rang = int(rang)
    __Number = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPWRSTUVWXYZ"
    __randomNumber = "".join(random.choice(__Number) for i in range(__rang))
    _email = __randomNumber + __randomEmail
    return _email


if __name__ == '__main__':
    print(get_new_email())
    print(get_new_username(8))
    print(get_password(6))
