"""
======================
Author: 柠檬班-小简
Time: 2020/7/3 20:41
Project: day5
Company: 湖南零檬信息技术有限公司
======================
"""
"""
1、数据库连接 conn  cur
2、获取一条数据？
3、获取条数
4、获取所有的数据
5、关闭数据库连接
"""
import pymysql

from Common.handle_conf import red_conf


class HandleDB:

    def __init__(self):
        # 连接数据库，创建游标。
        # 1、建立连接
        self.conn = pymysql.connect(
            host=red_conf.get("mysql", "host"),
            port=red_conf.getint("mysql", "port"),
            user=red_conf.get("mysql", "user"),
            password=red_conf.get("mysql", "password"),
            database=red_conf.get("mysql", "database"),
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        # 2、创建游标
        self.cur = self.conn.cursor()

    def select_one_data(self, sql):
        self.conn.commit()
        self.cur.execute(sql)
        return self.cur.fetchone()

    def select_all_data(self, sql):
        self.conn.commit()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def get_count(self, sql):
        self.conn.commit()
        return self.cur.execute(sql)

    def update(self, sql):
        """
        对数据库进行增、删、改的操作。
        :param sql:
        :return:
        """
        self.cur.execute(sql)
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    # sql = 'select * from member LIMIT 3'
    # db = HandleDB()
    # count = db.get_count(sql)
    # print("结果个数为：",count)
    # data = db.select_one_data(sql)
    # print("一条数据：",data)
    # all = db.select_all_data(sql)
    # print("所有的数据：",all)
    # db.close()
    # 初始化数据库对象
    db = HandleDB()
    sql = 'SELECT id FROM auth_user WHERE username="ajshjhka"'
    all = db.select_all_data(sql)
    print(all)

