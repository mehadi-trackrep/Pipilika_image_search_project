import scrapy
from ecommerce import items
import datetime



class OthobaSpider(scrapy.Spider):

    name = "othoba"
    allowed_domains = ["www.othoba.com"]

    start_urls = [
        'https://www.othoba.com/'
    ]

    def start_requests(self):

        for url in self.start_urls:
            request = scrapy.Request(url=url, callback=self.parse_category)
            request.meta['depth'] = 1
            yield request

    def parse_category(self, response):

        category_tags = response.selector.xpath('//li[@class="lnkHeading"]/a/@href').extract()

        for tag in category_tags:
            tag1 = 'https://www.othoba.com' + tag
            request = scrapy.Request(url=tag1, callback=self.parse_product_list)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request

    def parse_product_list(self, response):

        product_list_urls = response.selector.xpath('//div[@class="picture"]/a/@href').extract()

        for url in product_list_urls:
            url1 = 'https://www.othoba.com'+url
            request = scrapy.Request(url=url1, callback=self.parse_product_detail)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request
           
    def parse_product_detail(self, response):

        product = items.Ecommerce_product_items()
        product['domain_name'] = 'www.othoba.com'
        product['url'] = response.url
        product['title'] = response.selector.xpath('//h2/span[@itemprop="name"]/text()').extract_first()

        a = response.selector.xpath('//ol[@class="breadcrumb"]//li/a/text()').extract()
        category_name = a[1:]
        product['categories'] = category_name

        product['currency'] ='BDT'

        s = response.selector.xpath('//span[@itemprop="price"]/text()').extract_first()
        if s is not None:
            s = s.replace(' ','')
            s = s.replace(',','')
            num = float(s)
            product['price'] = num
        else:
            product['price'] = 0          

        img1 = response.selector.xpath('//div[@style="margin-top: 10px;text-align: left;"]//div/a/@href').extract()
        img2 = response.selector.xpath('//a[@itemprop="image"]/@href').extract()

        product['images'] = img1 + img2
        product['last_updated'] = datetime.datetime.now()

        yield product

