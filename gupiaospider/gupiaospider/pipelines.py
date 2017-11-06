# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from pymongo import MongoClient


class GupiaospiderPipeline(object):
    def __init__(self):
        conn = MongoClient(settings['MDB_HOST'], settings['MDB_PROT'])
        db = conn[settings['MDB_DATABASE']]
        self.collection = db[settings['MDB_TABLE']]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
