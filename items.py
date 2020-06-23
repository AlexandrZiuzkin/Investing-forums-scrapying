# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

def edit(value):
    return str(value).replace("'","").replace('"',"")#.replace(r"\r","").replace(r"\n","")
class MvidItem(scrapy.Item):
    source = scrapy.Field(serializer=edit)
    position = scrapy.Field(serializer=edit)
    main_comment_id = scrapy.Field(serializer=edit)
    comment_text = scrapy.Field(serializer=edit)
    comment_id = scrapy.Field(serializer=edit)
    user_name = scrapy.Field(serializer=edit)
    user_id = scrapy.Field(serializer=edit)
    link = scrapy.Field()
    date = scrapy.Field(serializer=edit)
    selfurl = scrapy.Field()
    

    


    

