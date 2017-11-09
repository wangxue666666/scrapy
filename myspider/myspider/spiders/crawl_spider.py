from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Spider
#http://www.quanwenyuedu.io/
#http://aoshidanshen.quanwenyuedu.io/
#/1.html
#/2.html
import os

class BookSpider(CrawlSpider):
    name = 'booker'
    start_urls = ['http://www.quanwenyuedu.io/']
    book_path = os.path.abspath(os.path.dirname(__file__)) + '\\file\\'
    book_link = LinkExtractor(allow=r'aoshidanshen.quanwenyuedu.io$',deny=(r'big5'))
    text_link = LinkExtractor(allow='/(\d+).html$',deny=(r'big5'))
    rules = (
        #callback是字符串，生成Rule对象
        Rule(book_link, callback='get_book',follow=True),
        Rule(text_link,callback='get_text',follow=False),
    )

    def get_book(self,response):
        book_name = response.xpath("//h1/text()").extract()[0]
        with open(self.book_path+book_name+'.txt','a') as f:
            pass

    def get_text(self,response):
        print(response.text)
        # book_name = response.xpath("//div[@class='book']/a/text()").re('《(\w*)》')[0]
        # print(book_name)
        # book_text = '\n'.join(response.xpath("//div[@id='content']//text()").extract())
        # print(book_text)
        # with open(self.book_path + book_name + '.txt', 'a',encoding='utf-8') as f:
        #     f.write(book_text)
class JianDan(Spider):
    name = 'jiandan'
    start_urls = ['http://jiandan.net']


    def parse(self, response):
        img = response.xpath("//div[@class='thumbs_b']//img/@src").extract()
        for   i in img:
            print(i)

