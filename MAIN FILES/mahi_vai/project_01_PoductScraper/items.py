# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
	title = scrapy.Field()
	product_url = scrapy.Field()
	category = scrapy.Field()
	img_url = scrapy.Field()
	price = scrapy.Field()
	domain = scrapy.Field()