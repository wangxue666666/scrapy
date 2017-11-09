from  scrapy.linkextractors import LinkExtractor
import scrapy
from scrapy_splash import SplashRequest

class SinaSpider(scrapy.Spider):
    name = 'sina'
    start_urls = ['http://news.sina.com.cn/']




    def parse(self, response):
        #new_list = LinkExtractor(allow=r'news.sina.com').extract_links(response)
        new_list = LinkExtractor(allow=r'sports.sina.com.cn/nba/').extract_links(response)
        for new in new_list:
            print(new.url,new.text)

class IfengSpider(scrapy.Spider):
    name = 'ifeng'
    start_urls = ['http://www.ifeng.com/']

    def parse(self, response):
        new_list = LinkExtractor(allow=r'news.ifeng.com').extract_links(response)
        for new in new_list:
            print(new.url, new.text)


class JsSpider(scrapy.Spider):
    name = 'jsspider'
    start_urls = ['http://data.10jqka.com.cn/market/rzrqgg/code/518880/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,self.parse,args={'wait':0.5})

    def parse(self, response):
        a = response.xpath('//*[@id="J-ajax-main"]/div[2]/a[1]').extract()
        print(a)
