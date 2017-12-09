#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from ecommerce import items
import datetime

class RokomariSpider(scrapy.Spider):

    name = "rokomari"
    allowed_domains = ["www.rokomari.com"]

    start_urls = [
        #'https://www.rokomari.com/'
        'https://www.rokomari.com/book/author/5717/%e0%a6%b8%e0%a6%be%e0%a6%a6%e0%a6%be%e0%a6%a4-%e0%a6%b9%e0%a7%8b%e0%a6%b8%e0%a6%be%e0%a6%87%e0%a6%a8?ref=mm_p8'
    ]

    def start_requests(self):

        for url in self.start_urls:
            #request = scrapy.Request(url=url, callback=self.parse_category)
            request = scrapy.Request(url=url, callback=self.parse_product_list)
            request.meta['depth'] = 1
            yield request

    def parse_category(self, response):

        category_tags = response.selector.xpath('//div[@class="mega_menu"]/ul//li/a/@href').extract()

        for tag in category_tags:
            tag = response.urljoin(tag)
            request = scrapy.Request(url=tag, callback=self.parse_product_list)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request

    def parse_product_list(self, response):

        product_list_urls = response.selector.xpath('//div[@class="bookListItem"]/a/@href').extract()

        for url in product_list_urls:
            url = response.urljoin(url)
            url = url.encode('utf-8')
            request = scrapy.Request(url=url, callback=self.parse_product_detail)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request
        a = response.selector.xpath('//div[@class="pagination"]//a/@href').extract()
        l = len(a)
        if l>1 :
            l = l-1
            lis = a[l:]
            next_page = lis[0].encode('utf-8')
            print 'hurrae ================================> '
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield response.follow(next_page, callback=self.parse_product_list)
           

    def parse_product_detail(self, response):

        product = items.Ecommerce_product_items()
        product['url'] = response.url
        product['domain_name'] = "www.rokomari.com"
        product['title'] = response.selector.xpath('//div[@class="buyArea"]/h2/text()').extract_first()

        cat = response.selector.xpath('//ol[@class="breadcrumb"]//li/a/text()').extract() 
        product['categories'] = cat[1:]
        product['currency'] = 'BDT'

        #PRICE OUTPUT FORMAT='Tk. 284'
        p = response.selector.xpath('//span[@class="mainPrice"]/text()').extract_first()
        
        p = p.replace(' ','')
        p = p.replace(',','')
        p = p.replace('Tk.','') # where 'Tk.' is substring
        p = p.replace('BDT','')
        l = len(p)

        num = float(p)
        product['price'] = num
       
        a = response.selector.xpath('//div[@class="bookImgArea"]//img/@src').extract()
        a = a[1:]
        img_others = response.selector.xpath('//ul[@class="list-unstyled"]//li/@hovermax').extract()

        sum_img = a + img_others
        product['images'] = sum_img
        product['last_updated'] = datetime.datetime.now()
        
        yield product

