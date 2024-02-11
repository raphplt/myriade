from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from gkiller.spiders.main import MainSpider


runner = CrawlerRunner(get_project_settings())

# Start the spider
d = runner.crawl(MainSpider)

# Shutdown the reactor when the spider is finished
d.addBoth(lambda _: reactor.stop())

# Start the reactor loop
reactor.run()
