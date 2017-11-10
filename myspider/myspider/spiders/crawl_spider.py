import os
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Spider,Request
# http://www.quanwenyuedu.io/
# http://aoshidanshen.quanwenyuedu.io/
# /1.html
# /2.html


class BookSpider(CrawlSpider):
    name = 'booker'
    start_urls = ['http://mayishensuanzi.quanwenyuedu.io/']
    section = 0
    book_path = os.path.abspath(os.path.dirname(__file__)) + '\\file\\'
    # book_link = LinkExtractor(allow=r'mayishensuanzi.quanwenyuedu.io$', deny=(r'big5'))
    text_link = LinkExtractor(allow='/(\d+).html$', deny=(r'big5'))


    rules = (
        # callback是字符串，生成Rule对象
        # Rule(book_link, callback='get_book', follow=True),
        Rule(text_link, callback='get_text', follow=True),
    )
    def get_book(self, response):
        book_name = response.xpath("//h1/text()").extract()[0]
        with open(self.book_path + book_name + '.txt', 'a') as f:
                pass

    def get_text(self, response):
        self.section += 1
        print(self.section)
        book_name = response.xpath("//div[@class='book']/a/text()").re('《(\w*)》')[0]
        book_text = '\n'.join(response.xpath("//div[@id='content']//text()").extract())
        with open(self.book_path + book_name + '.txt', 'a',encoding='utf-8') as f:
            f.write('\n'+str(self.section)+'\n'+book_text)


class JianDan(Spider):
    name = 'jiandan'
    start_urls = ['http://jiandan.net']

    def parse(self, response):
        img = response.xpath("//div[@class='thumbs_b']//img/@src").extract()
        for i in img:
            print(i)
