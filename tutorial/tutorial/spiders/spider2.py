from scrapy.log import INFO
from ..common_spider import CommonSpider


class Spider2(CommonSpider):
    name = 'spider2'

    # must add "kwargs", otherwise can't run in scrapyd
    def __init__(self, settings, **kwargs):
        super(Spider2, self).__init__(settings, **kwargs)

        self._title_path = settings.get('TITLE_PATH', '')

    def parse_other_info(self, response):
        title = response.css(self._title_path).extract()[0]
        self.log('title: %s' % title, INFO)

    def parse(self, response):
        self.parse_other_info(response)

        super(Spider2, self).parse(response)
