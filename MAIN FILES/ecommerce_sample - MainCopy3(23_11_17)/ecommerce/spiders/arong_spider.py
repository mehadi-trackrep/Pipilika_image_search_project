import scrapy
from ecommerce import items
import datetime

class AarongSpider(scrapy.Spider): ## V.V.I. ekhane site er kicu problem ace :( 

    name = "aarong"
    allowed_domains = ["www.aarong.com"]

    start_urls = [
        'http://www.aarong.com/'
    ]

    def start_requests(self):

        for url in self.start_urls:

            request = scrapy.Request(url=url, callback=self.parse_category)
            request.meta['depth'] = 1
            yield request

    def parse_category(self, response):

        category_tags = response.selector.xpath('//ul[@class="desktop menu-level1"]//li/ul//li/a/@href').extract()

        for tag in category_tags:
            request = scrapy.Request(url=tag, callback=self.parse_product_list)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request

    def parse_product_list(self, response):

        product_list_urls = response.selector.xpath('//a[@class="product-image"]/@href').extract()

        for url in product_list_urls:
            request = scrapy.Request(url=url, callback=self.parse_product_detail)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request
        #print '==========================>nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn=> '
        next_page = response.selector.xpath('//a[@class="aarongicon-page-right"]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_product_list)
           

    def parse_product_detail(self, response):

        product = items.Ecommerce_product_items()
        product['domain_name'] = 'www.aarong.com'
        product['url'] = response.url
        product['title'] = response.selector.xpath('//div[@class="productHeadLeft" ]/h1[@class="hidden-phone"]/text()').extract_first()
        a = response.selector.xpath('//div[@class="breadcrumb"]//a/text()').extract()
        category_name = a[1:]
        product['categories'] = category_name        
        product['currency'] ='BDT'

        s = response.selector.xpath('//span[@class="price"]/text()').extract_first()
        
        s = s.replace(' ','')
        s = s.replace(',','')
        s = s.replace('Tk','')

        num = float(s)
        product['price'] = num
        
        product['images'] = response.selector.xpath('//div[@class="showcase-thumbnail"]/a/@href').extract()
        product['last_updated'] = datetime.datetime.now()

        yield product

