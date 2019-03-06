# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors
import time


# class Liepinspd2Pipeline(object):
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
#         """
#         数据库建立连接
#         :param settings: 配置参数
#         :return: 实例化参数
#         """
#
#         adbparams = dict(
#             host=settings['MYSQL_HOST'],
#             db=settings['MYSQL_DBNAME'],
#             user=settings['MYSQL_USER'],
#             password=settings['MYSQL_PASSWORD'],
#             cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
#         )
#         # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
#         dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
#         # 返回实例化参数
#         return cls(dbpool)
#
#     def process_item(self, item, spider):
#         """
#         使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
#         """
#         query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和操作数据
#         # 添加异常处理
#         query.addCallback(self.handle_error)  # 处理异常
#
#     def do_insert(self, cursor, item):
#         # 对数据库进行插入操作，并不需要commit，twisted会自动commit
#         insert_sql = "insert into liepin_job(as_of_date,ticker,company_name,job_name,salary,city,education,work_year,pub_time,origin_site) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#         cursor.execute(insert_sql, (item['as_of_date'], str(item['ticker']), str(item['company_name']), str(item['job_name']),
#                                     str(item['salary']),str(item['city']),str(item['education']),str(item['work_year']),str(item['pub_time']),str(item['origin_site'])))
#
#     def handle_error(self, failure):
#         if failure:
#             # 打印错误信息
#             print(failure)

class Liepinspd2Pipeline(object):
    """
    同步操作
    """

    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect('rm-2zewagytttzk6f24xno.mysql.rds.aliyuncs.com', 'cn_ainvest_db', 'cn_ainvest_sd3a1', 'special_data')  # 有中文要存入数据库的话要加charset='utf8'
        # 创建游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # sql语句
        insert_sql = """
        insert into job_info(as_of_date,ticker,company_name,job_name,job_label,salary,city,education,work_year,pub_time,job_describe,spider_time,function) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, (item['as_of_date'], str(item['ticker']), str(item['company_name']), str(item['job_name']),str(item['job_label']),
                                    str(item['salary']),str(item['city']),str(item['education']),str(item['work_year']),str(item['pub_time']),str(item['job_describe']),item['spider_time'],str(item['function'])))
        # 提交，不进行提交无法保存到数据库
        self.conn.commit()

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()
