import scrapy
from scrapy.item import Item, Field
from urllib.parse import urljoin
from pymongo import MongoClient

class AllInfoItem(Item):
    title = Field()
    content = Field()
    links = Field()
    url = Field()

class URLItem(Item):
    url = Field()

class QuotesSpider(scrapy.Spider):
    name = "main_spider"
    start_urls = [
        "https://fr.wikipedia.org/wiki/Jaime_Villegas"
    ]

    def __init__(self, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]

    def parse(self, response):
        # Parsing for AllInfoItem
        all_info_item = AllInfoItem()
        all_info_item['title'] = response.css('title::text').get()
        all_info_item['content'] = response.css('p::text').getall()
        all_info_item['url'] = response.url

        links = response.css('a::attr(href)').getall()
        
        # base_url = response.url.split("/")[2]

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
