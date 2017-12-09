import scrapy
from ecommerce import items
import datetime

class DarazSpider(scrapy.Spider):

    name = "daraz"
    allowed_domains = ["www.daraz.com.bd"]

    start_urls = [
        'https://www.daraz.com.bd/'
        #'https://www.daraz.com.bd/mens-western-clothing/'
    ]

    def start_requests(self):

        for url in self.start_urls:
            request = scrapy.Request(url=url, callback=self.parse_category)
            request.meta['depth'] = 1
            yield request

    def parse_category(self, response):

        category_tags = response.selector.xpath('//nav[@id="menuFixed"]//div[@class="categories"]/a[@class="category"]/@href').extract()

        for tag in category_tags:
            #tag=https://www.daraz.com.bd/mens-western-clothing/
            request = scrapy.Request(url=tag, callback=self.parse_product_list)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request

    def parse_product_list(self, response):

        product_list_urls = response.selector.xpath('//div[@class="sku -gallery -validate-size "]/a[@class="link"]/@href').extract()

        for url in product_list_urls:
            #url=https://www.daraz.com.bd/bd-exclusive-black-and-ash-cotton-t-shirt-for-men-337172.html
            request = scrapy.Request(url=url, callback=self.parse_product_detail)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request
        next_page = response.selector.xpath('//li[@class="item"]/a[@title="Next"]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_product_list)
           

    def parse_product_detail(self, response):

        product = items.Ecommerce_product_items()
        product['url'] = response.url
        product['domain_name']="www.daraz.com.bd"
        product['title'] = response.selector.xpath('//div[@class="details -validate-size"]/span/h1[@class="title"]/ text()').extract_first()

        a = response.selector.xpath('//nav[@class="osh-breadcrumb"]/ul//li/a/text()').extract()
        l = len(a)-1
        a = a[1:l]
        
        product['categories'] = a
        product['currency'] ='BDT'
        
        p =  response.selector.xpath('//span[@dir="ltr"]/text()').extract_first()
        p = p.replace(' ','')
        p = p.replace(',','')
        
        num = float(p)
        product['price'] = num
        print num

        #product['images'] = response.selector.xpath(u'//div[@class="product-preview"]/img/@data-zoom').extract() #one image
        product['images'] = response.selector.xpath('//div[@class="thumbs-wrapper"]/div[@id="thumbs-slide"]//a/@href').extract() #image list
        product['last_updated'] = datetime.datetime.now()
        #'https://bd.daraz.io/EtGrdRLf6i5cz3R7boLgMrApIF4=/fit-in/680x680/filters:fill(white)/product/27/1733/1.jpg?6043', 
        #u'https://bd.daraz.io/zGz4XrWyA2iB8ZpGhYLM7Wilt0I=/fit-in/680x680/filters:fill(white)/product/27/1733/2.jpg?6043'
        yield product

