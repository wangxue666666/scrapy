import scrapy

class WbtcItem(scrapy.Item):
    title = scrapy.Field()
    room = scrapy.Field()
    money = scrapy.Field()
    addr_end = scrapy.Field()
