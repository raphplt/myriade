from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from gkiller.spiders.main import MainSpider
from gkiller.items import URLItem
from pymongo import MongoClient
from gkiller.settings import MONGODB_COLLECTION_URLS, MONGODB_DB, MONGODB_URI

# Function to check if the URL collection is empty
def is_url_collection_empty():
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    collection = db[MONGODB_COLLECTION_URLS]
    return collection.count_documents({}) == 0

# Function to add a base URL if the collection is empty
def add_base_url_if_empty():
    if is_url_collection_empty():
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DB]
        collection = db[MONGODB_COLLECTION_URLS]
        base_url = "https://www.francetvinfo.fr/meteo/secheresse/reportage-on-prie-pour-avoir-de-l-eau-dans-les-pyrenees-orientales-la-secheresse-historique-etouffe-des-agriculteurs-maudits-des-dieux_6355207.html"
        url_item = URLItem(url=base_url)
        collection.insert_one(dict(url_item))

# Add base URL if URL collection is empty
add_base_url_if_empty()

runner = CrawlerRunner(get_project_settings())

# Start the spider
d = runner.crawl(MainSpider)

# Shutdown the reactor when the spider is finished
d.addBoth(lambda _: reactor.stop())

# Start the reactor loop
reactor.run()
