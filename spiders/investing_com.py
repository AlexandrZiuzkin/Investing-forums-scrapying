# -*- coding: utf-8 -*-
import scrapy
import requests
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http.request import Request
from MVID.settings import ANY_URL_REGEX_NEW
import re
from math import ceil
import json


from MVID.items import MvidItem

# def make_request():
#     domen = 'https://ru.investing.com'
#     url = "https://ru.investing.com/stock-screener/Service/SearchStocks"
#     referrer = [
#         #"https://ru.investing.com/stock-screener/?sp=country::5|sector::a|industry::a|equityType::a|exchange::a%3Ceq_market_cap;1",
#         "https://ru.investing.com/stock-screener/?sp=country::56|sector::a|industry::a|equityType::a%3Ceq_market_cap;1",
#     ]

#     bodies = [
#         #'country%5B%5D=56&sector=6%2C11%2C12%2C8%2C5%2C7%2C4%2C10%2C2%2C1%2C3%2C9&industry=72%2C51%2C88%2C56%2C8%2C19%2C67%2C43%2C89%2C15%2C80%2C59%2C41%2C37%2C55%2C52%2C2%2C93%2C48%2C57%2C1%2C22%2C71%2C82%2C76%2C46%2C94%2C95%2C102%2C58%2C101%2C30%2C29%2C35%2C53%2C16%2C34%2C47%2C12%2C66%2C90%2C14%2C49%2C17%2C44%2C68%2C27%2C11%2C74%2C85%2C63%2C83%2C84%2C26%2C21%2C79%2C36%2C64%2C62%2C60%2C24%2C20%2C54%2C33%2C4%2C81%2C40%2C98%2C70%2C99%2C42%2C39%2C92%2C65%2C18%2C73%2C77%2C25%2C7%2C10%2C78%2C86%2C87%2C38%2C31%2C6%2C91%2C61%2C97%2C45%2C13%2C100%2C23%2C96%2C9%2C69%2C32%2C75%2C5%2C28%2C50%2C3&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC%2CETN&exchange%5B%5D=40&pn={}&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d',
#         'country%5B%5D=5&sector=6%2C11%2C12%2C8%2C5%2C7%2C4%2C10%2C2%2C1%2C3%2C9&industry=72%2"C51%2C88%2C56%2C8%2C19%2C67%2C43%2C89%2C15%2C80%2C59%2C41%2C37%2C55%2C52%2C2%2C93%2C48%2C57%2C1%2C22%2C71%2C82%2C76%2C46%2C94%2C95%2C102%2C58%2C101%2C30%2C29%2C35%2C53%2C16%2C34%2C47%2C12%2C66%2C90%2C14%2C49%2C17%2C44%2C68%2C27%2C11%2C74%2C85%2C63%2C83%2C84%2C26%2C21%2C79%2C36%2C64%2C62%2C60%2C24%2C20%2C54%2C33%2C4%2C81%2C40%2C98%2C70%2C99%2C42%2C39%2C92%2C65%2C18%2C73%2C77%2C25%2C7%2C10%2C78%2C86%2C87%2C38%2C31%2C6%2C91%2C61%2C97%2C45%2C13%2C100%2C23%2C96%2C9%2C69%2C32%2C75%2C5%2C28%2C50%2C3&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC%2CETN&exchange%5B%5D=2&exchange%5B%5D=95&exchange%5B%5D=1&pn={}&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d',
#     ]

#     headers = {
#         "Host": "ru.investing.com",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0",
#         "Accept": "application/json, text/javascript, */*; q=0.01",
#         "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Referer": "{}",
#         "Content-Type": "application/x-www-form-urlencoded",
#         "X-Requested-With": "XMLHttpRequest",
#     }

#     #scrapy.FormRequest( url = url, headers= headers, method= "POST", body = bodies)
    
#     links = []
#     for b , r in zip(bodies, referrer):
#         i = 1
#         while True:
#                 headers['Refferer'] = r
#                 req = requests.post( url = url, headers = headers, data= b.format(i))
#                 data = req.json()
#                 if 'error' in data  :
#                     break
#                 numPages = ceil(data['totalCount'] / 50) - 1

#                 print(data['pageNumber'],'/',numPages)
#                 for d in data['hits']:
#                     link = d['viewData']['link']
#                     if '?' in link:
#                         redirect_link = domen + link.replace('?', '-commentary?') + '\n'
#                     else:
#                         redirect_link = domen + link + '-commentary' + '\n'
#                     #print(redirect_link)
#                     links.append(redirect_link)
#                 if data['pageNumber'] == numPages:
#                     break

#                 i = i + 1
#     return links


# def change_link(value):
#     return value + "-commentary/"


class InvestingComSpider(CrawlSpider):
    name = 'investing_com'
    allowed_domains = ['ru.investing.com']
    #my_urls = make_request()
    #start_urls =  my_urls
    # ['https://ru.investing.com/stock-screener/?sp=country::56|sector::a|industry::a|equityType::a|exchange::40%3Ceq_market_cap;1',
    #               #'https://ru.investing.com/stock-screener/?sp=country::5|sector::a|industry::a|equityType::a%3Ceq_market_cap;1',
    #             ]
    rules = (
        #Rule(LinkExtractor( restrict_xpaths= ("//div[@class = 'resultsContainer stockScreener']"), process_value= change_link, allow='/equities/', unique=True), follow=True), 
		Rule(LinkExtractor( restrict_xpaths= ("//div[@class = 'midDiv inlineblock']"), unique= True), callback='parse_page', follow=True),   #//div[contains(@class , 'sideDiv inlineblock text_align_lang_base_2')]//a[contains(.,@href])]
	)

    def parse_start_url(self, response):
        return self.parse_page(response)

    # def parse(self, response):
    #     headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
    #     self.parse_item(response)
    #     #yield Request(self.start_urls[0], headers=headers, callback= self.parse_item)

    def parse_page(self, response):

        
        sel = Selector(response)

        comment_set = sel.xpath("//div[@class = 'comment js-comment']")
        for comment in comment_set:
            item = MvidItem()
            item['position'] = sel.xpath("//div[@class = 'instrumentHead']/h1/text()").extract_first()
            item['source'] = self.allowed_domains[0]
            main_comment = comment.xpath(".//div[@class = 'mainComment js-content']")
            item['main_comment_id'] = comment.xpath("./@data-comment-id").extract_first()
            item['comment_text'] = main_comment.xpath(".//span[@class = 'js-text']/text()").extract()
            item['comment_id'] = comment.xpath("./@data-comment-id").extract_first() 
            item['user_id'] = comment.xpath("./@data-user-id").extract_first()
            item['user_name'] = main_comment.xpath(".//a[@class = 'js-user-link']//@alt").extract_first() 
            item['date'] = main_comment.xpath(".//span[@class = 'js-date']/@comment-date-formatted").extract_first()
            item['selfurl'] = response.url
            if not item['comment_id'] or not item['user_name'] or not item['comment_text']:
                continue
            item['link'] = re.findall(ANY_URL_REGEX_NEW, main_comment.xpath(".//span[@class = 'js-text']/text()").extract()[0])

            reply_comments = comment.xpath(".//div[@class = 'commentReply js-comment js-comment-reply']")
            for reply in reply_comments:
                 self.parse_details(reply, item['comment_id'], item['position'], item['selfurl']) # comment.xpath("./@data-comment-id/text()")
            yield item
        
        
    
    def parse_details(self, response, main_comment_id, position, url):

        
        sel = response
        item = MvidItem()

        item['position'] = position
        item['source'] = self.allowed_domains[0]
        item['main_comment_id'] = main_comment_id                         
        item['comment_text'] = sel.xpath(".//span[@class = 'js-text']/text()").extract_first()
        item['comment_id'] = sel.xpath("./@data-comment-id").extract_first() 
        item['user_id'] = sel.xpath("./@data-user-id").extract_first()
        item['user_name'] = sel.xpath(".//a[@class = 'js-user-link']//@alt").extract_first()
        item['date'] = sel.xpath(".//span[@class = 'js-date']/@comment-date-formatted").extract_first()
        item['selfurl'] = url
        if not item['comment_id'] or not item['user_name'] or not item['comment_text']:
            return
        item['link'] = re.findall(ANY_URL_REGEX_NEW, sel.xpath(".//span[@class = 'js-text']/text()").extract()[0]) #r'(https?://[^\s]+)'
        

        itemproc = self.crawler.engine.scraper.itemproc
        itemproc.process_item(item, self)

        return item
        
