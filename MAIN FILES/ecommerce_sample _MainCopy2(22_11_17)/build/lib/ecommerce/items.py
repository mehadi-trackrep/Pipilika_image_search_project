# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime


class Product(scrapy.Item):

    title = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    images = scrapy.Field()
    categories = scrapy.Field()
    url = scrapy.Field()
    last_updated = scrapy.Field()


class Daraz(Product):
    pass


