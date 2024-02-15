import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient
from spiders.main import MainSpider
from settings import MONGODB_COLLECTION_URLS, MONGODB_DB, MONGODB_URI, CONCURRENT_REQUESTS, CONCURRENT_REQUESTS_PER_DOMAIN

def check_urls_collection_empty():
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    collection = db[MONGODB_COLLECTION_URLS]
    return collection.count_documents({}) == 0

def fetch_urls_from_database():
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    collection = db[MONGODB_COLLECTION_URLS]
    urls = [doc['url'] for doc in collection.find({'done': {'$exists': False}}, {'url': 1})]
    return urls

def run_spiders():
    process = CrawlerProcess(get_project_settings())
    process.crawl(MainSpider, concurrent_requests=CONCURRENT_REQUESTS, concurrent_requests_per_domain=CONCURRENT_REQUESTS_PER_DOMAIN)
    process.start()

def main():
    urls = fetch_urls_from_database()
    while urls:
        process = CrawlerProcess(get_project_settings())
        for url in urls:
            process.crawl(MainSpider, start_urls=[url])
        process.start()
        time.sleep(5)
        urls = fetch_urls_from_database()

if __name__ == "__main__":
    main()
