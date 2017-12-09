import scrapy
from ecommerce import items
import datetime


class PickabooSpider(scrapy.Spider): 

    name = "pickaboo"
    allowed_domains = ["www.pickaboo.com"]

    start_urls = [
        'https://www.pickaboo.com'
    ]

    def start_requests(self):

        for url in self.start_urls:
            request = scrapy.Request(url=url, callback=self.parse_category)
            request.meta['depth'] = 1
            yield request

    def parse_category(self, response):

        category_tags =  response.selector.xpath('//ul[@class="menu-container"]/li[@class="menu-item-text menu-item-depth-3  "]/h5/a/@href').extract()

        for tag in category_tags:
            request = scrapy.Request(url=tag, callback=self.parse_product_list)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request

    def parse_product_list(self, response):

        product_list_urls =  response.selector.xpath('//h2[@class="product-name newname"]/a/@href').extract()

        for url in product_list_urls:
            request = scrapy.Request(url=url, callback=self.parse_product_detail)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request
        #print '==========================>nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn=> '
        next_page = response.selector.xpath('//a[@class="next i-next"]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_product_list)
           

    def parse_product_detail(self, response):

        product = items.Ecommerce_product_items()
        product['domain_name'] = 'www.pickaboo.com'
        product['url'] = response.url
        
        a = response.selector.xpath('//div[@class="breadcrumbs"]/ul//li/a/span/text()').extract()
        category_name = a[1:]
        product['categories'] = category_name

        product['title'] = response.selector.xpath('//h1[@itemprop="name"]/text()').extract_first()
        product['currency'] ='BDT'

        price = response.selector.xpath('//span[@class="regular-price"]//span[@class="price"]/text()').extract_first()
        if price is not None:
            s = price
        else:
            s = response.selector.xpath('//p[@class="special-price"]//span[@class="price"]/text()').extract_first()

        s = s.replace(' ','')
        s = s.replace(',','')
        s = s[1:]

        num = float(s)
        product['price'] = num
        print num            

        img1 =  response.selector.xpath('//a[@class="magnify-zoom-gallery"]/img/@src').extract()
        img2 = response.selector.xpath('//img[@id="magnify-small"]/@src').extract()

        product['images'] = img1 + img2
        product['last_updated'] = datetime.datetime.now()

        yield product

