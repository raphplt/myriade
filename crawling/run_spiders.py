import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient
from spiders.main import MainSpider
from settings import MONGODB_COLLECTION_URLS, MONGODB_DB, MONGODB_URI

def check_urls_collection_empty():
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    collection = db[MONGODB_COLLECTION_URLS]
    return collection.count_documents({}) == 0

def run_spiders():
    process = CrawlerProcess(get_project_settings())
    process.crawl(MainSpider)
    process.start()

def main():
    while not check_urls_collection_empty():
        print("Running spiders...")
        run_spiders()
        print("Waiting for 5 seconds before checking again...")
        time.sleep(5)

if __name__ == "__main__":
    main()
