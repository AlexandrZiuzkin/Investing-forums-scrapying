# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http.request import Request
#from MVID.settings import ANY_URL_REGEX
import re


from MVID.items import MvidItem


class InvestingComSpider(CrawlSpider):
    name = 'smart_lab_en'
    allowed_domains = ['smart-lab.ru']
    start_urls = ['https://smart-lab.ru/q/usa/']

    rules = (
        Rule(LinkExtractor( restrict_xpaths= ("//table[@class = 'simple-little-table trades-table']"), allow='/forum/', unique=True),  follow=True),
		Rule(LinkExtractor( restrict_xpaths= ("//div[@class = 'pagination1']"), unique=True), callback='parse_page', follow=True),   #//div[contains(@class , 'sideDiv inlineblock text_align_lang_base_2')]//a[contains(.,@href])]
	)
    def parse_start_url(self, response):
        return self.parse_page(response)


    def parse_page(self, response):

        sel = Selector(response)

        comment_set = sel.xpath("//li[@data-type = 'comment']")
        for comment in comment_set:
            item = MvidItem()
            item['source'] = self.allowed_domains[0]
            item['position'] = sel.xpath(".//div[@class = 'nocenter']/h1/text()").extract()
            item['main_comment_id'] = comment.xpath("./@data-id").extract()
            item['comment_text'] = comment.xpath(".//div[@class = 'text']/text()").extract()
            item['comment_id'] = comment.xpath("./@data-id").extract() 
            item['user_id'] = comment.xpath(".//a[@class = 'a_name trader_other']/@href").extract()
            item['user_name'] = comment.xpath(".//a[@class = 'a_name trader_other']/text()").extract() 
            item['date'] = comment.xpath(".//a[@class = 'a_time']/time/@datetime").extract()
          
            item['link'] = comment.xpath(".//div[@class = 'text']//@href").extract()
            item['selfurl'] = response.url


            yield item
        
        
