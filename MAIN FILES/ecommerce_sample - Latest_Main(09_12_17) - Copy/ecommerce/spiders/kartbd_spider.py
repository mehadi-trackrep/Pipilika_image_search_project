import scrapy
from ecommerce import items
import datetime


class KartbdSpider(scrapy.Spider):     ## TestSpider so class name in items.py will be Test 

    name = "kartbd"

    start_urls = [
       
        'http://kartbd.com/'
    ]

    def start_requests(self):

        for url in self.start_urls:
            request = scrapy.Request(url=url, callback=self.parse_category)
            request.meta['depth'] = 1
            yield request

    def parse_category(self, response):

        category_tags = response.selector.xpath('//li[@class="has-child parent"]/a/@href').extract()

        for tag in category_tags:
            mystring = 'http:'
            tag = mystring + tag
            request = scrapy.Request(url=tag, callback=self.parse_product_list)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request

    def parse_product_list(self, response):

        product_list_urls = response.selector.xpath('//div[@class="image-box"]/a/@href').extract()

        for url in product_list_urls:
            url = 'http://kartbd.com'+url
            request = scrapy.Request(url=url, callback=self.parse_product_detail)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request
        next_page = response.selector.xpath('//li[@class="i-next"]/a/@href').extract_first()
        if next_page is not None:
            next_page = 'http://kartbd.com' + next_page
            yield response.follow(next_page, callback=self.parse_product_list)
           

    def parse_product_detail(self, response):

        product = items.Ecommerce_product_items()
        product['url'] = response.url
        product['domain_name']="kartbd.com"
        product['title'] = response.selector.xpath('//div[@class="col-md-5 col-sm-6 product-info"]/h2[@class="title"]/text()').extract_first()
        
        a = response.selector.xpath('//nav[@class="breadcrumb"]/ul//li/a/text()').extract()
        category_name = a[1:]
        product['categories'] = category_name

        product['currency'] ='BDT'
        
        p = response.selector.xpath('//div[@class="col-xs-7"]/text()').extract_first()
        #tk
        #'\n                tk1,490.00'
        p = p.replace(' ','')
        p = p.replace(',','')
        p = p.replace('tk','') # where 'Tk.' is substring
        p = p.replace('\n','')
        
        num = float(p)
        product['price'] = num
        
        img = 'http://kartbd.com'
        img1 = response.selector.xpath('//a[@class="f-box"]/@href').extract()
        img1 =  [img + ck for ck in img1]

        img2 = response.selector.xpath('//div[@id="thumbRails"]//div/a/img/@src').extract()
        img2 =  [img + ck for ck in img2]

        product['images'] = img1 + img2

        product['last_updated'] = datetime.datetime.now()

        yield product

