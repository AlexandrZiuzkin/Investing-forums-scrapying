# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http.request import Request
from MVID.settings import ANY_URL_REGEX_NEW
import re


from MVID.items import MvidItem


class InvestingComSpider(CrawlSpider):
    name = 'mfd_ru'
    allowed_domains = ['forum.mfd.ru']

    start_urls = ['http://forum.mfd.ru/forum/subforum/?id=1&page=0']

    rules = (
        Rule(LinkExtractor( restrict_xpaths= ("//td[@class = 'mfd-item-subject']"), unique= True),  follow=True),
		Rule(LinkExtractor( restrict_xpaths= ("//div[@class = 'mfd-paginator']"), unique= True), callback='parse_page', follow=True),   #//div[contains(@class , 'sideDiv inlineblock text_align_lang_base_2')]//a[contains(.,@href])]
	)
  

    def parse_start_url(self, response):
        return self.parse_page(response)

    def parse_page(self, response):

        if bytes('Анонимный доступ к форуму с вашего адреса запрещен.', 'utf-8') in response.body:
            open('bad_mfd.txt','a+',).write(response.url + "\n")
            return

        sel = Selector(response)

        comment_set = sel.xpath("//div[@class = 'mfd-post']")

        for comment in comment_set:

            item = MvidItem()
            item['position'] = sel.xpath(".//div[@class = 'mfd-header']/h1/text()").extract()
            item['source'] = self.allowed_domains[0]
            item['main_comment_id'] = comment.xpath(".//div[@class = 'mfd-post-top-0']/@id").extract() 
            item['comment_text'] = comment.xpath(".//div[@class = 'mfd-quote-text']/text()").extract()
            item['comment_id'] = comment.xpath(".//div[@class = 'mfd-post-top-0']/@id").extract() 
            item['user_id'] = comment.xpath(".//a[@class = 'mfd-anonymous-link']/@title").extract()
            item['user_name'] = comment.xpath(".//div[@class = 'mfd-post-top-0']/a/text()").extract() 
            item['date'] = comment.xpath(".//div[@class = 'mfd-post-top-1']/a/text()").extract()
            item['link'] = comment.xpath(".//div[@class = 'mfd-quote-text']/a/@href").extract()
            item['selfurl'] = response.url

            yield item

        

