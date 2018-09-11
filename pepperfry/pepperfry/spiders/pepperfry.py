import scrapy
import os
from scrapy.utils.python import to_native_str
from six.moves.urllib.parse import urljoin
from scrapy.utils.response import open_in_browser as view


class PepperSpider(scrapy.Spider):
    name = 'pepperfry'
    search_url = 'https://www.pepperfry.com/site_product/search?q='
    handle_httpstatus_list = [301, 302]

    def start_requests(self):
        search_keywords = {'bench', 'two seater sofa', 'book case', 'coffee table', 'dining set',
                           'queen bed', 'arm chair', 'chest drawer', 'garden chair', 'bean bag', 'king bed'}
        folder_map = {'bench': 'bench', 'two seater sofa': '2-seater-sofa', 'book case': 'book-cases', 'coffee table': 'coffee-table', 'dining set': 'dining-set',
                      'queen bed': 'queen-beds', 'arm chair': 'arm-chairs', 'chest drawer': 'chest-drawers', 'garden chair': 'garden-seating', 'bean bag': 'bean-bags', 'king bed': 'king-beds'}
        for kw in search_keywords:
            query = '%7B'+kw+'%7D'
            request = scrapy.Request(url='{}{}'.format(
                self.search_url, query), callback=self.parse)
            folder = folder_map[kw]
            os.makedirs('../data/{}'.format(folder), exist_ok=True)
            request.meta['folder'] = folder
            yield request

    def parse(self, response):
        if response.status >= 300 and response.status < 400:

            # HTTP header is ascii or latin1, redirected url will be percent-encoded utf-8
            location = to_native_str(
                response.headers['location'].decode('latin1'))

            # get the original request
            request = response.request
            # and the URL we got redirected to
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
            # view(response)
            link = response.xpath('//a[@title]').extract_first()
            print('PARSING', link)
            yield {'link': link}
