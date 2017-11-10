import scrapy


class ErrorSpider(scrapy.Spider):
    name = 'espider'
    start_urls =['http://www.baidu.com/sdsf']
    handle_httpstatus_list = [404]

    def parse(self, response):
        print(response.meta)
        print(response.status)