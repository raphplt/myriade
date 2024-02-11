import scrapy
from urllib.parse import urljoin
from pymongo import MongoClient
from gkiller.settings import MONGODB_COLLECTION_URLS, MONGODB_DB, MONGODB_URI
from gkiller.items import AllInfoItem, URLItem

class MainSpider(scrapy.Spider):
    name = "main_spider"

    def start_requests(self):
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DB]
        collection = db[MONGODB_COLLECTION_URLS]
        urls = collection.find({}, {'url': 1})

        for url_doc in urls:
            yield scrapy.Request(url_doc['url'], callback=self.parse)


    def parse(self, response):
        # Parsing for AllInfoItem
        all_info_item = AllInfoItem()
        all_info_item['title'] = response.css('title::text').get()
        all_info_item['content'] = response.css('p::text').getall()
        all_info_item['url'] = response.url

        links = response.css('a::attr(href)').getall()
        
        # Delete links starting with #
        links = [link for link in links if not link.startswith("#")]

        # Make all links absolute
        links = [urljoin(response.url, link) for link in links]

        all_info_item['links'] = list(set(links))

        yield all_info_item

        # Parsing for URLItem
        for link in all_info_item['links']:
            url_item = URLItem()
            url_item['url'] = link
            yield url_item
