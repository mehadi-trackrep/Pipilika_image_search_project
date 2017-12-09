import scrapy
from ecommerce import items
import datetime

class BagdoomSpider(scrapy.Spider): 

    name = "bagdoom"
    allowed_domains = ["www.bagdoom.com"]

    start_urls = [
        'https://www.bagdoom.com/'
        #'https://www.bagdoom.com/kids-corner/toys.html'
    ]

    def start_requests(self):

        for url in self.start_urls:
            request = scrapy.Request(url=url, callback=self.parse_category)
            request.meta['depth'] = 1
            yield request

    def parse_category(self, response):

        category_tags = response.selector.xpath('//li[@class="sub_category level2"]/a/@href').extract()

        for tag in category_tags:
            request = scrapy.Request(url=tag, callback=self.parse_product_list)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request

    def parse_product_list(self, response):

        product_list_urls =  response.selector.xpath('//h2[@class="product-name"]/a/@href').extract()

        for url in product_list_urls:
            request = scrapy.Request(url=url, callback=self.parse_product_detail)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request
        #print '==========================>nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn=> '
        next_page = response.selector.xpath('//li/a[@class="next i-next"]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_product_list)
           

    def parse_product_detail(self, response):

        product = items.Ecommerce_product_items()
        product['domain_name'] = 'www.bagdoom.com'
        product['url'] = response.url
        product['title'] = response.selector.xpath('//div[@class="product-name"]/h1/text()').extract_first()
        a = response.selector.xpath('//div[@class="breadcrumbs"]/ul//li/a/text()').extract()
        category_name = a[1:]    
        product['categories'] = category_name
       
        product['currency'] ='BDT'

        price = response.selector.xpath('//p [@class="special-price"]/span [@class="price"]/text()').extract_first()
        if price is not None:
            s = price
        else:
            s = response.selector.xpath('//span[@class="price"]/text()').extract_first()

        if s is not None:
            s = s.replace(' ','')
            s = s.replace(',','')
            s = s.replace('Tk.','') # where 'Tk.' is substring
            num = float(s)
            product['price'] = num
        else:
            product['price'] = 0       

        product['images'] = response.selector.xpath('//div[@class="more-views"]/ul//li/a/@href').extract()
        product['last_updated'] = datetime.datetime.now()

        yield product

