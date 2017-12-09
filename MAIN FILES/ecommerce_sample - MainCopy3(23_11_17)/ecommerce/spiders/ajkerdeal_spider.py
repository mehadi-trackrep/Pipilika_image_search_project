#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from ecommerce import items
import datetime

class AjkerdealSpider(scrapy.Spider): ## V.V.I. ekhane site er kicu problem ace :( 

    name = "ajkerdeal"
    allowed_domains = ["ajkerdeal.com"]

    start_urls = [
        'https://ajkerdeal.com/en/'
        #'https://www.daraz.com.bd/mens-western-clothing/'
    ]

    def start_requests(self):

        for url in self.start_urls:
            request = scrapy.Request(url=url, callback=self.parse_category)
            request.meta['depth'] = 1
            yield request

    def parse_category(self, response):

        category_tags = response.selector.xpath('//span[@class="title-subcategory-span"]/a/@href').extract()

        for tag in category_tags:
            request = scrapy.Request(url=tag, callback=self.parse_product_list)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request

    def parse_product_list(self, response):

        product_list_urls = response.selector.xpath('//div[@class="deal-image-container"]/a/@href').extract()

        for url in product_list_urls:
            request = scrapy.Request(url=url, callback=self.parse_product_detail)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request

    def parse_product_detail(self, response):

        product = items.Ecommerce_product_items()

        product['domain_name'] = 'ajkerdeal.com'
        product['categories'] =  response.selector.xpath('//ul[@id="navC"]//li//a/text()').extract()
        product['url'] = response.url
        str_title = response.selector.xpath('//span[@id="DealTitleLabel"]/text()').extract_first()
        product['title'] = str_title #unicode(str_title, 'utf-8').encode('utf-8')
        product['currency'] ='BDT'
        s = response.selector.xpath('//span[@id="ProductPriceLabel"]/text()').extract_first()

        s = s.replace(',','')
        s = s.replace(' ','')
        num = float(s)
        product['price'] = num

        product['images'] = response.selector.xpath('//div[@id="thumbsImageDiv"]//a/@href').extract()
        product['last_updated'] = datetime.datetime.now()
        
        yield product

