# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
from pymongo import MongoClient
from .settings import MYSQL_DBNAME,MYSQL_PASSWD,MYSQL_USER,MYSQL_HOST,MDB_HOST,MDB_PROT

'''
def process_item(self, item, spider):
    if isinstance(item, WhoscoredNewItem):
        table_name = item.pop('table_name')
        col_str = ''
        row_str = ''
        for key in item.keys():
            col_str = col_str + " " + key + ","
            row_str = "{}'{}',".format(row_str, item[key] if "'" not in item[key] else item[key].replace("'", "\\'"))
            sql = "insert INTO {} ({}) VALUES ({}) ON DUPLICATE KEY UPDATE ".format(table_name, col_str[1:-1],
                                                                                    row_str[:-1])
        for (key, value) in six.iteritems(item):
            sql += "{} = '{}', ".format(key, value if "'" not in value else value.replace("'", "\\'"))
        sql = sql[:-2]
        self.cursor.execute(sql)  # 执行SQL
        self.cnx.commit()  # 写入操作
'''
class WbtcPipeline(object):
    def __init__(self):
        self.conn = MongoClient(MDB_HOST, MDB_PROT)
        self.db = self.conn.scrapy
        self.collectiong = self.db.homelist
        # self.dbpool = pymysql.connect(MYSQL_HOST,MYSQL_USER, MYSQL_PASSWD, MYSQL_DBNAME,charset ='utf8')
        # self.cursor = self.dbpool.cursor()
    def process_item(self, item, spider):
        # self._conditional_insert(item)
        return item

    def _conditional_insert(self, item):
        self.collectiong.insert(dict(item))
        # self.cursor.execute(
        #     "insert into home_list(title,room,money,addr) values('%s','%s','%s','%s')"%(item['title'],item['room'],item['money'],item['addr_end'])
        # )
        # self.dbpool.commit()

    def close_spider(self,spider):
        self.conn.close()
