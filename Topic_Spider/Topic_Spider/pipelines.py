# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from twisted.enterprise import adbapi
import requests


class TopicSpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class MySQLAsyncPipeline:
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'scrapy_default')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', '3306')
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', '')
        
        self.dbpool = adbapi.ConnectionPool('MySQLdb',host=host,db=db,user=user,passwd=passwd,charset='utf8')

    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        item['content'] = "".join(item['content'])
        item['content'] = item['content'].replace(' ', '')
        self.dbpool.runInteraction(self.insert_db, item)
        return item

    def insert_db(self, tx, item):
        values = (
                item['id'],
                item['title'],
                item['content'],
                item['image_url'],
            )
        sql = 'INSERT INTO article(id, title, content, image_url) VALUES(%s,%s,%s,%s)'
        tx.execute(sql, values)
