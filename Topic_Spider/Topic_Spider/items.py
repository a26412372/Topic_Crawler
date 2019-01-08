# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import string

class TopicSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TopicItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()      #文章標題
    content = scrapy.Field()    #文章內容
    image_url = scrapy.Field()  #文章圖片
