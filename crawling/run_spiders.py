import time
from indexation import Indexation
from settings import MONGODB_COLLECTION_URLS, MONGODB_DB, MONGODB_URI, CONCURRENT_REQUESTS, CONCURRENT_REQUESTS_PER_DOMAIN
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient
from spiders.main import MainSpider

def check_urls_collection_empty():
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    collection = db[MONGODB_COLLECTION_URLS]
    return collection.count_documents({}) == 0

def create_urls_collection():
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    if MONGODB_COLLECTION_URLS not in db.list_collection_names():
        db.create_collection(MONGODB_COLLECTION_URLS)

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

def run_indexing():
    indexer = Indexation()
    indexer.index_documents()

def main():
    create_urls_collection()
    
    if check_urls_collection_empty():
        predefined_url = "https://www.bfmtv.com/"  
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DB]
        collection = db[MONGODB_COLLECTION_URLS]
        collection.insert_one({'url': predefined_url})

    run_spiders()  
    
    while True:
        run_indexing()
        time.sleep(5)


if __name__ == "__main__":
    main()
