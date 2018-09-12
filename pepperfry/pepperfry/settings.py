# -*- coding: utf-8 -*-
BOT_NAME = 'pepperfry'
SPIDER_MODULES = ['pepperfry.spiders']
NEWSPIDER_MODULE = 'pepperfry.spiders'

USER_AGENT = 'Mozilla/5.0'
ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    'pepperfry.pipelines.PepperfryImagesPipeline': 1,
}
# IMAGES_MIN_HEIGHT = 100
# IMAGES_MIN_WIDTH = 100
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'
IMAGES_STORE = 'images_store'
IMAGES_URLS_FIELD = 'image_urls'
IMAGES_RESULT_FIELD = 'images'
MEDIA_ALLOW_REDIRECTS = True
