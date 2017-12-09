import scrapy
from ecommerce import items
import datetime



class DamSpider(scrapy.Spider):  ##V.V.I. next page a jhamela ace :( 

    name = "dam"
    allowed_domains = ["dam.com.bd"]

    start_urls = [
        'https://dam.com.bd/'
        #'https://dam.com.bd/product/762'
    ]

    def start_requests(self):

        for url in self.start_urls:
            request = scrapy.Request(url=url, callback=self.parse_category)
            request.meta['depth'] = 1
            yield request

    def parse_category(self, response):

        category_tags = response.selector.xpath('//ul[@class="dropdown-menu submenu-menu"]/li/a/@href').extract()

        for tag in category_tags:
            request = scrapy.Request(url=tag, callback=self.parse_product_list)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request

    def parse_product_list(self, response):

        product_list_urls =  response.selector.xpath('//td[@width="125"]/a/@href').extract()

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
        product['domain_name'] = 'dam.com.bd'
        product['url'] = response.url
        product['title'] = response.selector.xpath('//h2[@itemprop="name"]/text()').extract_first()

        a = response.selector.xpath('//div[@id="breadcrumbs"]/ul//li/a/span/text()').extract()
        l = len(a)-1
        product['categories'] = a[1:l]
        
        product['currency'] ='BDT'

        s = response.selector.xpath('//span[@itemprop="lowPrice"]/text()').extract_first()
        s = s.replace(' ','')
        s = s.replace(',','')
        s = s.replace('Tk.','')

        num = float(s)
        product['price'] = num

        img1 = response.selector.xpath('//div[@class="clearfix padder-v-sm"]//img/@src').extract()
        img2 = response.selector.xpath('//img[@itemprop="image"]/@src').extract()
        s = img1 + img2

        product['images'] = s

        product['last_updated'] = datetime.datetime.now()

        yield product

