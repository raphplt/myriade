from pymongo import MongoClient

from gkiller.settings import MONGODB_COLLECTION_URLS, MONGODB_DB, MONGODB_URI

class URLManager:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[MONGODB_DB]

    def get_urls_to_crawl(self):
        collection = self.db[MONGODB_COLLECTION_URLS]
        return collection.find({}, {'url': 1})

url_manager = URLManager()
urls_to_crawl = url_manager.get_urls_to_crawl()
