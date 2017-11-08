import scrapy
from ..items import GupiaospiderItem


class GupiaoSpider(scrapy.Spider):
    name = 'gupiao'
    start_urls = ['http://stock.10jqka.com.cn/']

    def parse(self, response):
        a_list = response.xpath("//div[@id='rzrq']/table[@class='m-table']//td[2]/a")
        for a in a_list:
            url = a.xpath('./@href').extract()[0]
            # 存在并发直接定义类属性传参只能是最后一个
            gp_name = a.xpath('./text()').extract()[0]
            gp_num = url.rsplit('/', 2)[1]
            yield scrapy.Request(url, callback=self.download_data,
                                 meta={'gp_name': gp_name, 'gp_num': gp_num, 'page': 1})

    def download_data(self, response):
        gp_num = response.meta.get('gp_num')
        gp_name = response.meta.get('gp_name')
        print(gp_name)
        next_page = response.meta.get('page') + 1
        tr_list = response.xpath("//table[@class='m-table']/tbody/tr")
        page_start_end = response.xpath("//div[@class='m-page J-ajax-page']/span/text()").extract()[0]
        page_max = int(page_start_end.split('/')[1])
        if tr_list == []:
            return
        for tr in tr_list:
            td_list = tr.xpath(".//td/text()").extract()
            td_list[1] = td_list[1].strip()
            item = GupiaospiderItem()
            item['name'] = gp_name
            item['number'] = td_list[0]
            item['time'] = td_list[1]
            item['balance'] = self.change_num(td_list[2])
            item['buy'] = self.change_num(td_list[3])
            item['repay'] = self.change_num(td_list[4])
            item['net_financing'] = self.change_num(td_list[5])
            item['margin'] = td_list[6]
            item['sale'] = td_list[7]
            item['reimbursed'] = td_list[8]
            item['short_selling'] = td_list[9]
            item['allowance_short'] = self.change_num(td_list[10])
            yield item
        if page_max >= next_page:
            yield scrapy.Request(self.nexturl(gp_num, next_page), callback=self.download_data,
                                 meta={'gp_num': gp_num, 'gp_name': gp_name, 'page': next_page})
        return

    def nexturl(self, gnum, page):
        url = "http://data.10jqka.com.cn/market/rzrqgg/code/518880/order/desc/page/1/ajax/1/"
        url_list = url.rsplit('/', 8)
        url_list[1] = gnum
        url_list[5] = str(page)
        next_url = '/'.join(url_list)
        return next_url
        # ajax
        # http://data.10jqka.com.cn/market/rzrqgg/code/518880/order/desc/page/2/ajax/1/

    def change_num(self, number):
        try:
            new_num = float(number)
        except:
            if number[-1:] == '万':
                new_num = int(float(number[:-1]) * 100000)
            else:
                new_num = int(float(number[:-1]) * 1000000000)
        return new_num

class TestSpider(scrapy.Spider):
    name = 'test'
    start_urls = ['http://data.10jqka.com.cn/market/rzrqgg/code/518880/']
    def parse(self, response):
        a = response.xpath('//*[@id="J-ajax-main"]/div[2]/a[1]').extract()
        print(a)