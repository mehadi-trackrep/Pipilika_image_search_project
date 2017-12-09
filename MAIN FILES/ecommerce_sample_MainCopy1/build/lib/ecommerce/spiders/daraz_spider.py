import scrapy
from ecommerce import items
import datetime

class DarazSpider(scrapy.Spider):

    name = "daraz"

    start_urls = [
        'https://www.daraz.com.bd/'
    ]

    def start_requests(self):

        for url in self.start_urls:

            request = scrapy.Request(url=url, callback=self.parse_category)
            request.meta['depth'] = 1
            yield request

    def parse_category(self, response):

        category_tags = response.xpath('//nav[@id="menuFixed"]//div[@class="categories"]//a[@href]').extract()

        for tag in category_tags:

            category_tag = scrapy.Selector(text=tag)
            request = scrapy.Request(url=category_tag.xpath("//@href").extract()[0], callback=self.parse_product_list)
            request.meta['category'] = category_tag.xpath("//text()").extract()[0]
            request.meta['depth'] = response.meta['depth'] + 1
            yield request

    def parse_product_list(self, response):

        category = response.meta['category']
        product_list_urls = response.xpath('//div[@class="sku -gallery"]//a/@href').extract()

        for url in product_list_urls:

            request = scrapy.Request(url=url, callback=self.parse_product_detail)
            request.meta['depth'] = response.meta['depth'] + 1
            yield request


    def parse_product_detail(self, response):

        product = items.Daraz()
        product['url'] = response.url
        product['title'] = response.xpath('//div[@class="details-wrapper"]//h1[@class="title"]//text()').extract()[0]
        product['categories'] = []
        product['currency'] = response.xpath('//div[@class="price-box"]//span//@data-currency-iso').extract()[0]
        product['price'] = response.xpath('//div[@class="price-box"]//span//@data-price').extract()[0]
        product['images'] = response.xpath('//div[@class="media"]//a//@href').extract()
        product['last_updated'] = datetime.datetime.now()

        yield product




