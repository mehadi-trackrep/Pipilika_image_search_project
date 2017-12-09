import scrapy
from ecommerce import items
import datetime

class NanarokomSpider(scrapy.Spider): 

    name = "nanarokom"

    start_urls = [
        'https://www.nanarokom.com'
    ]

    def start_requests(self):

        for url in self.start_urls:
            request = scrapy.Request(url=url, callback=self.parse_category)
            request.meta['depth'] = 1
            yield request

    def parse_category(self, response):

        category_tags = response.selector.xpath('//ul[@class="menu"]//li/a/@href').extract()

        for tag in category_tags:
            request = scrapy.Request(url=tag, callback=self.parse_product_list)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request

    def parse_product_list(self, response):

        product_list_urls =  response.selector.xpath('//h3[@class="product-name short"]/a/@href').extract()

        for url in product_list_urls:
            request = scrapy.Request(url=url, callback=self.parse_product_detail)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request
           
    def parse_product_detail(self, response):

        product = items.Ecommerce_product_items()
        product['domain_name'] = 'www.nanarokom.com'
        product['url'] = response.url
        product['title'] = response.selector.xpath('//h1[@class="product_title entry-title"]/text()').extract_first()
        
        a = response.selector.xpath('//nav[@class="woocommerce-breadcrumb"]//a/text()').extract()

        l = len(a)-1
        category_name = a[1:l]
        product['categories'] = category_name

        product['currency'] ='BDT'

        a = response.selector.xpath('//p[@class="price"]/ins/span[@class="woocommerce-Price-amount amount"]/text()').extract_first()
        if a is not None:
            s = a
        else:
            s = response.selector.xpath('//p[@class="price"]/span[@class="woocommerce-Price-amount amount"]/text()').extract_first()

        s = s.replace(' ','')
        s = s.replace(',','')
        
        print " ssssssssssssssssss      "
        print s
        num = float(s)
        product['price'] = num
        print num

        img1 = response.selector.xpath('//figure[@class="woocommerce-product-gallery__wrapper"]//div//a/@href').extract()
        img2 = response.selector.xpath('//a[@itemprop="image"]/@href').extract()
        s = img1 + img2

        product['images'] = s

        product['last_updated'] = datetime.datetime.now()

        yield product

