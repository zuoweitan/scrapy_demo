# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SZHomeSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    field = scrapy.Field()
    address = scrapy.Field()
    category = scrapy.Field()
    number = scrapy.Field()
    parking_number = scrapy.Field()
    developer = scrapy.Field()
    # debug_info = scrapy.Field()



