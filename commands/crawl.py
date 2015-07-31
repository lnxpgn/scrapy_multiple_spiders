from scrapy.commands.crawl import Command
from scrapy.exceptions import UsageError


class CustomCrawlCommand(Command):
    def run(self, args, opts):
        if len(args) < 1:
            raise UsageError()
        elif len(args) > 1:
            raise UsageError("running 'scrapy crawl' with more than one spider is no longer supported")
        spname = args[0]

        # added new code
        spider_settings_path = self.settings.getdict('SPIDER_SETTINGS', {}).get(spname, None)
        if spider_settings_path is not None:
            self.settings.setmodule(spider_settings_path, priority='cmdline')
        # end

        crawler = self.crawler_process.create_crawler()
        spider = crawler.spiders.create(spname, **opts.spargs)
        crawler.crawl(spider)
        self.crawler_process.start()
