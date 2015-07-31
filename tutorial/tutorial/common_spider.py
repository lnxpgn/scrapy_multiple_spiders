# -*- coding: utf-8 -*-
import urlparse
from scrapy import Request
from scrapy.log import INFO
from scrapy.spider import Spider


class CommonSpider(Spider):
    """
        This is a common spider, including common functions which child spiders can inherit or overwrite
    """
    name = ''
    allowed_domains = []
    start_urls = []

    # must add "kwargs", otherwise can't run in scrapyd
    def __init__(self, settings, **kwargs):
        super(CommonSpider, self).__init__(**kwargs)

        self._start_urls = []
        self._start_urls.extend(settings.get('START_URLS', []))
        if not self._start_urls:
            raise Exception('no urls to crawl')

    @classmethod
    def from_settings(cls, settings, **kwargs):
        return cls(settings, **kwargs)

    @classmethod
    def from_crawler(cls, crawler, **kwargs):
        return cls.from_settings(crawler.settings, **kwargs)

    def start_requests(self):
        for url in self._start_urls:
            # must append these hosts, otherwise OffsiteMiddleware will filter them
            parsed_url = urlparse.urlparse(url)
            parsed_url.hostname and self.allowed_domains.append(parsed_url.hostname)

            # open('file name', 'a+') is different between OS X and Linux, read an empty filter list from <JOBDIR>/requests.seen when launche the spider on OS X, be careful "dont_filter"
            yield Request(url, callback=self.parse, method='GET', dont_filter=True)

    def parse(self, response):
        self.log('response url: %s, status: %d' % (response.url, response.status), INFO)
