# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):

	domain_name = scrapy.Field()
	categories = scrapy.Field()
	url = scrapy.Field()
	title = scrapy.Field()
	price = scrapy.Field()
	currency = scrapy.Field()
	images = scrapy.Field()
	last_updated = scrapy.Field()

class Ecommerce_product_items(Product):
 	pass



