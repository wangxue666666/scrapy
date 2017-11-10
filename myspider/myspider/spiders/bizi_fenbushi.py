from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request, signals
from scrapy_redis.spiders import RedisCrawlSpider
import os
from pydispatch import dispatcher

class BizhiSpider(RedisCrawlSpider):
    name = 'bizhi'
    #start_urls = ['http://desk.zol.com.cn/']
    redis_key = 'bizhi_key'
    img_path = os.path.abspath(os.path.dirname(__file__)) + '\\file\\'
    bizhi_link = LinkExtractor(allow=r'bizhi/.*html$')
    rules = (
        Rule(bizhi_link,callback='download_img',follow=True),
    )

    def download_img(self,response):
        img_url = response.xpath("//img[@id='bigImg']/@src").extract()[0]
        yield Request(img_url,callback=self.download)

    def download(self,response):
        print(response)


