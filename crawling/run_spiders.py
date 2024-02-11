from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

# Start multiple spiders
process.crawl('main_spider', start_url="https://fr.wikipedia.org/wiki/Paremoremo")

process.start()