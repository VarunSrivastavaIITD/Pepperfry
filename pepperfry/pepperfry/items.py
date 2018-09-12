# -*- coding: utf-8 -*-
import scrapy


class PepperfryImage(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    item_dir = scrapy.Field()
