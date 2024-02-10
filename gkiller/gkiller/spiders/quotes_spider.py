import scrapy
from . import collection  # 

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
        "https://fr.wikipedia.org/wiki/Jaime_Villegas"
    ]

    def parse(self, response):
        title = response.css('title::text').get()
        description = response.css('meta[name="description"]::attr(content)').get()
        content = response.css('body::text').getall()
        links = response.css('a::attr(href)').getall()

        data = {
            'title': title,
            'description': description,
            'content': content,
            'links': links,
            'url': response.url
        }

        collection.insert_one(data)
