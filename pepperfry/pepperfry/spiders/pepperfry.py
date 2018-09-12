import scrapy
import os
from scrapy.utils.python import to_native_str
from six.moves.urllib.parse import urljoin
from scrapy.utils.response import open_in_browser as view
from scrapy.selector import Selector
from pepperfry.items import PepperfryImage
import json


class PepperSpider(scrapy.Spider):
    name = 'pepperfry'
    search_url = 'https://www.pepperfry.com/site_product/search?q='
    handle_httpstatus_list = [301, 302]
    base_dir = 'Pepperfry_data'
    max_items = 20
    metadata_filename = 'metadata.txt'

    def start_requests(self):
        search_keywords = {'bench', 'two seater sofa', 'book case', 'coffee table', 'dining set',
                           'queen bed', 'arm chair', 'chest drawer', 'garden chair', 'bean bag',
                           'king bed'}
        folder_map = {'bench': 'bench', 'two seater sofa': '2-seater-sofa', 'book case': 'book-cases',
                      'coffee table': 'coffee-table', 'dining set': 'dining-set', 'queen bed': 'queen-beds',
                      'arm chair': 'arm-chairs', 'chest drawer': 'chest-drawers',
                      'garden chair': 'garden-seating', 'bean bag': 'bean-bags', 'king bed': 'king-beds'}
        for kw in search_keywords:
            query = '%7B'+kw+'%7D'
            request = scrapy.Request(url='{}{}'.format(
                self.search_url, query), callback=self.parse)
            folder = folder_map[kw]
            folder_path = os.path.join('..', self.base_dir, folder)
            os.makedirs(folder_path, exist_ok=True)
            request.meta['folder_path'] = folder_path
            yield request

    def parse(self, response):
        if response.status >= 300 and response.status < 400:

            location = to_native_str(
                response.headers['location'].decode('latin1'))
            request = response.request
            redirected_url = urljoin(request.url, location)
            if response.status in (301, 307) or request.method == 'HEAD':
                redirected = request.replace(url=redirected_url)
                yield redirected
            else:
                redirected = request.replace(
                    url=redirected_url, method='GET', body='')
                redirected.headers.pop('Content-Type', None)
                redirected.headers.pop('Content-Length', None)
                yield redirected

        if response.status == 200:
            folder_path = response.meta['folder_path']
            os.makedirs(folder_path, exist_ok=True)
            links = response.xpath(
                '//a[@title][@onclick]').extract()[:self.max_items]
            for link in links:
                sel = Selector(text=link)
                url = sel.xpath('//@href').extract_first()
                yield scrapy.Request(url=url, callback=self.parse_item, meta={'folder_path': folder_path})

    def parse_item(self, response):
        if response.status >= 300 and response.status < 400:
            location = to_native_str(
                response.headers['location'].decode('latin1'))
            request = response.request
            redirected_url = urljoin(request.url, location)

            if response.status in (301, 307) or request.method == 'HEAD':
                redirected = request.replace(url=redirected_url)
                yield redirected
            else:
                redirected = request.replace(
                    url=redirected_url, method='GET', body='')
                redirected.headers.pop('Content-Type', None)
                redirected.headers.pop('Content-Length', None)
                yield redirected

        if response.status == 200:
            item_title = response.xpath('//h1/text()').extract_first()
            folder_title = '_'.join(item_title.split(' '))
            item_folder_path = os.path.join(
                response.meta['folder_path'], folder_title)
            os.makedirs(item_folder_path, exist_ok=True)
            metadata_file = os.path.join(
                item_folder_path, self.metadata_filename)

            metadata = {'title': item_title,
                        'category': os.path.split(response.meta['folder_path'])[-1],
                        'mrp': response.xpath('//span[contains(@class,"vip-old-price-amt")]/text()').extract_first().strip(),
                        'offer_price': response.xpath('//b[@class="pf-orange-color pf-large font-20 pf-primary-color"]/text()').extract_first().strip(),
                        'brand': response.xpath('//span[@itemprop="brand"]/text()').extract_first().strip(),
                        'description': ''.join(response.xpath('//div[@itemprop="description"]//p/text()').extract()),
                        'sku': response.xpath('//span[@itemprop="sku"]/text()').extract_first()}
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f)

            image = PepperfryImage()
            image['image_urls'] = response.xpath(
                '//img[@alt="' + item_title + '"]/../..//a/@data-img').extract()
            image['item_dir'] = item_folder_path
            yield image
