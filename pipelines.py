# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# class MvidPipeline(object):
#     def process_item(self, item, spider):
#         return item

#import MySQLdb

from scrapy.exceptions import NotConfigured
import logging
#from sqlalchemy.orm import sessionmaker
#from MVID.models import QuoteDB, db_connect, create_table
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import DropItem
import json

class CSVPipeline(object):

  @classmethod
  def from_crawler(cls, crawler):
    pipeline = cls()
    crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    return pipeline

  def spider_opened(self, spider):
    self.file = open('%s_items.csv' % spider.name, 'w+b')
    self.exportering = CsvItemExporter(self.file)
    #self.exportering.fields_to_export = ['comment_text', 'comment_id', 'user_name', 'user_id', 'link', 'date']
    self.exportering.start_exporting()

  def spider_closed(self, spider):
    self.exportering.finish_exporting()
    #file = self.files.pop(spider)
    self.file.close()

  def process_item(self, item, spider):
    if item['main_comment_id'] and  type(item['main_comment_id']) is list: 
            if '{commentID}' in item['main_comment_id']:
                return
    self.exportering.export_item(item)
    return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('{}_items.json'.format(spider.name), 'w', encoding= 'utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if '{commentID}' in item['main_comment_id']:
          return
        line = json.dumps(dict(item)) + ",\n"
        self.file.write(line)
        return item


# class ScrapySpiderPipeline(object):
#     def __init__(self):
#         """
#         Initializes database connection and sessionmaker.
#         Creates deals table.
#         """
#         engine = db_connect()
#         create_table(engine)
#         self.Session = sessionmaker(bind=engine)

#     def process_item(self, item, spider):
#         """Save deals in the database.

#         This method is called for every item pipeline component.
#         """
#         session = self.Session()
#         quotedb = QuoteDB(spider.name)
#         quotedb.quote = item["quote"]
#         quotedb.author = item["author"]

#         try:
#             session.add(quotedb)
#             session.commit()
#         except:
#             session.rollback()
#             raise
#         finally:
#             session.close()

#         return item

# class MYSQLPipeline(object):

#     def __init__(self, db, user, passwd, host):
#         self.db = db
#         self.user = user
#         self.passwd = passwd
#         self.host = host

#     @classmethod
#     def from_crawler(cls, crawler):
#         db_settings = crawler.settings.getdict("DB_SETTINGS")
#         if not db_settings:
#             raise NotConfigured
#         db = db_settings['db']
#         user = db_settings['user']
#         passwd = db_settings['passwd']
#         host = db_settings['host']
#         return cls(db, user, passwd, host)

#     def open_spider(self, spider):
#         self.conn = MySQLdb.connect(db=self.db,
#                                user=self.user, passwd=self.passwd,
#                                host=self.host,
#                                charset='utf8', use_unicode=True)
#         self.cursor = self.conn.cursor()
#         self.cursor.execute("CREATE TABLE IF NOT EXISTS {} (main_comment_id VARCHAR(255), comment_text VARCHAR(255), comment_id VARCHAR(255), user_name VARCHAR(255) , user_id VARCHAR(255), link VARCHAR(255), nodate VARCHAR(255)) ENGINE=INNODB;".format( spider.name))

#     def process_item(self, item, spider):
#         if item['main_comment_id'] and  type(item['main_comment_id']) is list: 
#             if '{commentID}' in item['main_comment_id']:
#                 return
#         logging.warning(spider.name)
#         #spider_name = spider.name

#         # if item.get("main_comment_id"):
#         #     main_comment_id = ' '.join(x for x in item.get("main_comment_id") if x)
#         # else:
#         #     main_comment_id = ""

#         # if item.get("comment_text"):
#         #     comment_text = ' '.join(x for x in item.get("comment_text") if x)
#         # else:
#         #     comment_text = ""

#         # if item.get("comment_id"):    
#         #     comment_id =  ' '.join(x for x in item.get("comment_id") if x)
#         # else:
#         #     comment_id = ""

#         # if item.get("user_name"): 
#         #     user_name =  ' '.join(x for x in item.get("user_name") if x)
#         # else:
#         #     user_name = ""

#         # if item.get("user_id"): 
#         #     user_id =  ' '.join(x for x in item.get("user_id") if x)
#         # else:
#         #     user_id = "" 

#         # if item.get("link"):   
#         #     link = ' '.join(x for x in item.get("link") if x)  
#         # else:
#         #     link = "" 

#         #date = str(item.get("date")[0]) #', '.join(x for x in item.get("date") if x)  

#         sql = "INSERT INTO {} (main_comment_id, comment_text, comment_id, user_name, user_id, link, nodate) VALUES ({}, {},{},{},{},{},{});".format(spider.name, item.get("main_comment_id"), item.get("comment_text"), item.get("comment_id"), item.get("user_name"), item.get("user_id"), item.get("link"), item.get("date"))   #(spider_name, main_comment_id, comment_text, comment_id, user_name, user_id, link, date)

#         #values = (str(spider.name), str(item.get("main_comment_id")), item.get("comment_text"), item.get("comment_id"), item.get("user_name"), item.get("user_id"), item.get("link"), item.get("date"))
       

#         # if not link:
#         #     link = self.conn.escape_string("")
#         # if not user_id:
#         #     link = self.conn.escape_string("")
        
        
#         self.cursor.execute(sql)
#         self.conn.commit()
        
#         return item


#     def close_spider(self, spider):
#         self.conn.close()