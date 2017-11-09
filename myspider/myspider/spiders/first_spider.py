
from scrapy import Spider,Request
from scrapy_splash import SplashRequest


from ..items import WbtcItem

# 新建爬虫类继承自Spdier

class FirstSpider(Spider):
    # 定义爬虫名称
    name = 'firstspider'
    # 域名限定
    allowed_domains  =['http://www.baidu.com']
    # 添加请求url
    start_urls = ['http://www.baidu.com']
    #局域设置项
    custom_settings = {
        'ITEM_PIPELINES': {
            #可以设置为空
        }
    }

    # 默认情况下scrapy会以get的方式发送start_urls中的url
    # 定义处理响应函数
    def parse(self, response):
        print(response.text)




class WbtcSpider(Spider):
    name = 'wbtcspider'
    start_urls = ['http://bj.58.com/chuzu/?PGTID=0d100000-0000-1282-f5a5-00429889f74a&ClickID=1']

    def parse(self, response):
        title_list = response.xpath("// div[ @class ='des']/h2/a[1]/text()").extract()
        addr_list = response.xpath("// div[ @class ='des']/p[@class='add']")
        room_list = response.xpath("// div[ @class ='des']/p[@class='room']/text()").extract()
        money_list = response.xpath("// div[ @class ='listliright']/div[@class='money']")

        for index, addr in enumerate(addr_list):
            midd_addr = addr.xpath('string(.)').re('\w*')
            midd_addr_end = list(set(midd_addr))
            midd_addr_end.sort(key = midd_addr.index)
            addr_end = ','.join(midd_addr_end[1:])
            title = title_list[index].split('|')[0].strip()
            room = ''.join(room_list[index].split())
            money = ''.join(money_list[index].xpath("string(.)").extract()[0].split())
            item = WbtcItem()
            item['title'] = title
            item['addr_end'] = addr_end
            item['room'] = room
            item['money'] = money
            yield item
        next_url = response.xpath("//li[@id='bottom_ad_li']//a[@class='next']/@href").extract()
        try:
            print(next_url[0])
            yield Request(next_url[0],callback=self.parse)
        except IndexError:
            print("爬虫爬取完成")