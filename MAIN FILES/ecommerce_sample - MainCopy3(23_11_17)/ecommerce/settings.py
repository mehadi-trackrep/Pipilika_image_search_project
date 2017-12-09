# -*- coding: utf-8 -*-

# Scrapy settings for ecommerce project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ecommerce'

SPIDER_MODULES = ['ecommerce.spiders']
NEWSPIDER_MODULE = 'ecommerce.spiders'


ROBOTSTXT_OBEY = True

ITEM_PIPELINES = ['ecommerce.pipelines.MongoDBPipeline']

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "ecommerce_data"     #  NAME of database in MONGO_DB

MONGODB_COLLECTION = "rokomari1"
#MONGODB_COLLECTION = "ecommerce_product_collection"

ITEM_PIPELINES = {
   #'stack.pipelines.StackPipeline': 300,
   'ecommerce.pipelines.MongoDBPipeline': 300,
}

DOWNLOAD_FAIL_ON_DATALOSS = False