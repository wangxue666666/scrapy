from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
#http://www.quanwenyuedu.io/
#http://aoshidanshen.quanwenyuedu.io/
#/1.html
#/2.html


class BookSpider(CrawlSpider):
    name = 'booker'
    start_urls = ['http://www.quanwenyuedu.io/']
    book_link = LinkExtractor(allow=r'quanwenyuedu.io$',deny='big5')
    text_link = LinkExtractor(allow=r'/(\d+).html$')
    rules = (
        #callback是字符串，生成Rule对象
        Rule(book_link, callback='get_book',follow=False),
        Rule(text_link,callback='get_text',follow=False),
    )

    def get_book(self,response):
        print(response.url)

    def get_text(self,response):
        print(response.url)
