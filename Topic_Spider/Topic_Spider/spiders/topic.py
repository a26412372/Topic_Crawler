# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import TopicItem
import requests
import os
import shutil

x = 1
class TopicSpider(scrapy.Spider):
    name = 'topic'
    allowed_domains = ['topic.spider.com']
    start_urls = ['http://disable.yam.org.tw/archives/category/topic']
    
    def parse(self, response):
        #分析專欄文章頁面中的每篇文章的連結
        le = LinkExtractor(restrict_css='div.post-excerpt h2')
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_topic, dont_filter=True)

        #分析'下一頁'連結
        le = LinkExtractor(restrict_css='div.navigation a.next')
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)

    def parse_topic(self, response):
        global x

        topic = TopicItem()
        topic['id'] = 'image' + str(x)

        sel = response.css('h1.title')
        topic['title'] = sel.xpath('./text()').extract_first()

        sel = response.css('div.post-content')
        data = sel.xpath('./p')
        topic['content'] = data.xpath('./text()').extract()

        sel = response.css('div.wp-caption')    #第一種圖片標籤
        content1 = sel.xpath('./img/@src').extract()

        sel = response.css('div.post-content')  #第二種圖片標籤
        content2 = sel.xpath('./p/img/@src').extract()
        
        if len(content1) != 0:                  #如果有爬到第一種圖片標籤
            topic['image_url'] = content1[0]
        elif len(content2) != 0:                #如果有爬到第二種圖片標籤
            topic['image_url'] = content2[0]
        else:
            topic['image_url'] = 'http://disable.yam.org.tw/wp-content/uploads/2018/10/a.jpg'

        #if(len(data) != 0):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        r = requests.get(url = topic['image_url'], headers=headers, timeout=4)
        with open('D:\\Android\\AndroidStudioProjects\\topic\\app\\src\\main\\res\\drawable-xxhdpi\\image' + str(x) + '.jpg', 'wb') as f:
            f.write(r.content)
        x = x + 1 
        yield topic


