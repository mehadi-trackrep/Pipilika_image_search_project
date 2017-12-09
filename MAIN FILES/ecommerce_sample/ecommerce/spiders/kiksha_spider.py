import scrapy
from ecommerce import items
import datetime

class KikshaSpider(scrapy.Spider): 

    name = "kiksha"
    
    start_urls = [
        'https://kiksha.com'
    ]

    def start_requests(self):

        for url in self.start_urls:
            request = scrapy.Request(url=url, callback=self.parse_category)
            request.meta['depth'] = 1
            yield request

    def parse_category(self, response):

        category_tags = response.selector.xpath('//ul[@class="level0"]/li[@class="level1 nav-6-1 parent item"]/a/@href').extract()

        for tag in category_tags:
            request = scrapy.Request(url=tag, callback=self.parse_product_list)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request

    def parse_product_list(self, response):

        product_list_urls =  response.selector.xpath('//div[@class="product-image"]/a/@href').extract()

        for url in product_list_urls:
            #url=https://kiksha.com/de-longhi-coffee-maker-kg49
            
            request = scrapy.Request(url=url, callback=self.parse_product_detail)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request
        #print '==========================>nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn=> '
        next_page = response.selector.xpath('//a[@class="button next i-next"]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_product_list)
           

    def parse_product_detail(self, response):

        product = items.Ecommerce_product_items()
        product['url'] = response.url
        product['domain_name']="www.kiksha.com"
        
        t = response.selector.xpath('//h1[@itemprop="name"]/text()').extract_first()
        l = len(t)
        t = t[65:l]
        product['title'] = t

        product['currency'] ='BDT'

        price = response.selector.xpath('//p[@class="special-price"]//span[@class="price"]/text()').extract_first()
        if price is not None:
            p = price
        else:
            p = response.selector.xpath('//span[@class="price"]/text()').extract_first()
        p = p.replace(' ','')
        p = p.replace(',','')
        p = p.replace('BDT','')
        num = float(p)
        product['price'] = num

        img1 = response.selector.xpath('//a[@class="thumb-link"]/img/@src').extract()
        img2 = response.selector.xpath('//img[@id="image-main"]/@src').extract()
        product['images'] = img1 + img2
        
        product['last_updated'] = datetime.datetime.now()

        yield product

