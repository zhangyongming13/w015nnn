# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class W015NnnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tiezi_name = scrapy.Field()
    tiezi_link = scrapy.Field()
    tiezi_link_postfix = scrapy.Field()
    image_urls = scrapy.Field()
    # image_results = scrapy.Field()
    # images = scrapy.Field()
    tupian_data = scrapy.Field()
    tiezi_date = scrapy.Field()
