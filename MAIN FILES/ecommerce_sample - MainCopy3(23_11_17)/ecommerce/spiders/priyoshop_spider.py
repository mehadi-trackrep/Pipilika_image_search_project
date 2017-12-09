import scrapy
from ecommerce import items
import datetime

class PriyoshopSpider(scrapy.Spider): 

    name = "priyoshop"

    start_urls = [
       
        'http://www.priyoshop.com'
    ]

    def start_requests(self):

        for url in self.start_urls:
            request = scrapy.Request(url=url, callback=self.parse_category)
            request.meta['depth'] = 1
            yield request

    def parse_category(self, response):

        category_tags = response.selector.xpath('//ul[@class="list goo-collapsible"]//ul[@class="sublist"]/li/a/@href').extract()

        for tag in category_tags:
            mystring = 'http://www.priyoshop.com'
            tag = mystring + tag
            request = scrapy.Request(url=tag, callback=self.parse_product_list)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request

    def parse_product_list(self, response):
      
        product_list_urls = response.xpath('//div[@class="product-item"]/div[@class="picture"]/a/@href').extract()

        for url in product_list_urls:
            url = 'http://www.priyoshop.com' + url
            request = scrapy.Request(url=url, callback=self.parse_product_detail)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request

    def parse_product_detail(self, response):

        product = items.Ecommerce_product_items() ## this name is same as class name in items.py
        product['domain_name'] = 'www.priyoshop.com'
        product['url'] = response.url
        title = response.selector.xpath('//div[@class="product-name"]/h1[@itemprop="name"]/text()').extract_first()
        product['title'] = title[33:]

        a = response.selector.xpath('//div[@class="breadcrumb"]/ul//li/span/a/span/text()').extract()
        category_name = a[1:]
        product['categories'] = category_name
        product['currency'] ='BDT'
        
        s =  response.selector.xpath('//span[@itemprop="price"]/text()').extract_first()
        s = s.replace(' ','')
        s = s.replace(',','')
        s = s.replace('Tk','')
        num = float(s)
        product['price'] = num
        print num            

        img1 = response.selector.xpath('//div[@class="picture-thumbs"]//a/@href').extract()
        img2 = response.selector.xpath('//img[@itemprop="image"]/@src').extract()
        s = img1 + img2

        product['images'] = s
        product['last_updated'] = datetime.datetime.now()

        yield product

