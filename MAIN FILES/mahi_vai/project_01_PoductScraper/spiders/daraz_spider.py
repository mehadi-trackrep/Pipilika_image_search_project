import scrapy
from project_01_PoductScraper.items import ProductItem

class DarazSpider(scrapy.Spider):
    name = "daraz"
    allowed_domains = ["daraz.com.bd"]
    start_urls = ['http://www.daraz.com.bd/']

    def parse(self, response):
        urls_categories = response.xpath('//div[@class="submenu"]/div[@class="column"]/div[@class="categories"]/a[@class="category"]/@href').extract()
        for url in urls_categories:
            yield scrapy.Request(url=url, callback=self.parse_categories)


    def parse_categories(self, response):
        urls_items = response.xpath('//a[@class="link"]/@href').extract()
        for url_indiv in urls_items:
            yield scrapy.Request(url=url_indiv, callback=self.parse_items)

        # follow pagination link
        next_page_url = response.xpath('//a[@title="Next" and @rel="follow"]/@href').extract_first()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse_categories)

    def parse_items(self, response):
        item = ProductItem()
        item['title'] = response.xpath('//span/h1[@class="title"]/text()').extract_first()
        item['product_url'] = response.url
        item['category'] = response.xpath('/html/body/main/nav/ul/li[2]/a/@title').extract_first()
        item['img_url'] = response.xpath('//*[@id="productImage"]/@data-src').extract_first()
        item['price'] = response.xpath('//span[@class="price" or @class="price -no-special"]/span[@dir="ltr"]/text()').extract_first()
        item['domain'] = "daraz.com.bd"
        yield item