#! /usr/bin/python
# -*- coding:utf-8 -*-
import copy

from pymysql import connect, cursors
import datetime
from decimal import Decimal
import decimal
from utils.my_logger import log


class DoMysql:
    def __init__(self, host: str, port: int, user, password: str, db_name: str):
        if not isinstance(port, int):
            port = int(port)
        if not isinstance(password, str):
            password = str(password)
        try:
            log.info('用户{} 连接MySql {} -> {}库'.format(user, host, db_name))
            self.connect = connect(host=host,
                                   port=port,
                                   user=user,
                                   password=password,
                                   db=db_name,
                                   charset='utf8mb4',  # 编码格式
                                   cursorclass=cursors.DictCursor)  # 让返回字典型的值
            self.cursor = self.connect.cursor()  # 建立游标
        except Exception as e1:
            log.info('连接失败：{}'.format(e1))

    def __del__(self):  # 析构函数，实例删除时触发
        if hasattr(self, "connect"):
            self.cursor.close()  # 先关闭游标
            self.connect.close()  # 再关闭连接

    def query_db(self, sql):
        """
        查询数据库
        :param sql:sql查询语句
        :return 返回一个 [dict, dict] 数据
        """
        try:
            log.info('查询数据库：{}'.format(sql))
            self.cursor.execute(sql)  # 执行sql语句
            result = self.cursor.fetchall()  # 获取执行的结果

            # 处理mysql的数据类型为python的数据类型
            new_result = list()
            new_dict = dict()
            for one_result in result:
                for k, v in one_result.items():
                    if isinstance(v, datetime.datetime):
                        new_dict[k] = f'{v}'
                    elif isinstance(v, decimal.Decimal):
                        new_dict[k] = float(v)
                    else:
                        new_dict[k] = v
                new_result.append(copy.deepcopy(new_dict))

            log.info('查询结果：{}'.format(new_result))
            return new_result
        except NameError as e:
            log.error('查询失败：{}'.format(e))

    def update_db(self, sql):
        """
        更新行记录
        :param sql:sql语句
        """
        try:
            log.info('更新操作：{}'.format(sql))
            result = self.cursor.execute(sql)
            self.connect.commit()  # 所有对数据库有改动的操作都需要commit
            log.info(f"更新成功：Affected rows: {result}")
            return result
        except Exception as e:
            log.info(f'更新失败：{e}')
            self.connect.rollback()  # 如果出了错，就需要回滚所有的操作


def connect_mysql(db_info, env_db):
    host = db_info["mysql_info"][env_db]["host"]
    port = int(db_info["mysql_info"][env_db]["port"])
    user = db_info["mysql_info"][env_db]["user"]
    password = str(db_info["mysql_info"][env_db]["password"])
    db_name = db_info["mysql_info"][env_db]["db_name"]
    return DoMysql(host, port, user, password, db_name)


if __name__ == '__main__':
    pass
