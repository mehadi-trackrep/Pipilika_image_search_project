import scrapy
from project_01_PoductScraper.items import ProductItem

class PickabooSpider(scrapy.Spider):
    name = "pickaboo"
    allowed_domains = ["pickaboo.com"]
    start_urls = ['https://www.pickaboo.com/']

    def parse(self, response):
        urls_categories = response.xpath('//h5/a/@href').extract()
        for url in urls_categories:
            yield scrapy.Request(url=url, callback=self.parse_categories)


    def parse_categories(self, response):
        urls_items = response.xpath('//a[@class="product-image"]/@href').extract()	
        for url_indiv in urls_items:
            yield scrapy.Request(url=url_indiv, callback=self.parse_items)

        # follow pagination link
        next_page_url = response.xpath('//a[@class="next i-next" and @title="Next"]/@href').extract_first()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse_categories)

    def parse_items(self, response):
        item = ProductItem()
        item['title'] = response.xpath('//h1[@class="product-productname"]/text()').extract_first()
        item['product_url'] = response.url
        list = response.xpath('//span[@itemprop="title"]/text()').extract()
        item['category'] = ""
        if len(list) > 1:
            item['category'] = response.xpath('//span[@itemprop="title"]/text()')[1].extract()
        item['img_url'] = response.xpath('//*[@id="owl-demo"]//img/@src').extract_first() #[0].extract()
        item['price'] = response.xpath('//span[@class="price" and @itemprop="price"]/@content').extract_first() #[0].extract()
        item['domain'] = "pickaboo.com"
        yield item