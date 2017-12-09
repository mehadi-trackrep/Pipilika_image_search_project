import scrapy
from ecommerce import items
import datetime


class EasyshoppingSpider(scrapy.Spider): 

    name = "easyshopping"
    allowed_domains = ["easyshoppingbd.com"]

    start_urls = [
        'https://easyshoppingbd.com/'
    ]

    def start_requests(self):

        for url in self.start_urls:
            request = scrapy.Request(url=url, callback=self.parse_category)
            request.meta['depth'] = 1
            yield request

    def parse_category(self, response):

        category_tags = response.selector.xpath('//div[@class="itemMenu level1"]/a/@href').extract()

        for tag in category_tags:
            request = scrapy.Request(url=tag, callback=self.parse_product_list)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request

    def parse_product_list(self, response):

        product_list_urls =  response.selector.xpath('//div[@class="products-inner"]/a/@href').extract()

        for url in product_list_urls:
            request = scrapy.Request(url=url, callback=self.parse_product_detail)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request
           

    def parse_product_detail(self, response):

        product = items.Ecommerce_product_items()
        product['domain_name'] = 'easyshoppingbd.com'
        product['url'] = response.url
        product['title'] = response.selector.xpath('//h1[@itemprop="name"]/text()').extract_first()

        a = response.selector.xpath('//span[@itemprop="title"]/text()').extract()
        product['categories'] = a
        product['currency'] ='BDT'

        s = response.selector.xpath('//span[@id="our_price_display"]/text()').extract_first()
        s = s.replace(' ','')
        s = s.replace(',','')
        s = s.replace('Tk.','')
        s = s[1:]
        num = float(s)
        product['price'] = num
        print num

        img1 = response.selector.xpath('//ul[@id="thumbs_list_frame"]//li/a/@href').extract()
        img2 = response.selector.xpath('//img[@id="bigpic" and @itemprop="image"]/@src').extract()
        product['images'] = img1 + img2
        product['last_updated'] = datetime.datetime.now()

        yield product

