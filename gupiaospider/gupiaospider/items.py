# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GupiaospiderItem(scrapy.Item):
    name = scrapy.Field()
    number = scrapy.Field()
    time = scrapy.Field()
    balance = scrapy.Field()
    buy = scrapy.Field()
    repay = scrapy.Field()
    net_financing = scrapy.Field()
    margin = scrapy.Field()
    sale = scrapy.Field()
    reimbursed = scrapy.Field()
    short_selling = scrapy.Field()
    allowance_short = scrapy.Field()
