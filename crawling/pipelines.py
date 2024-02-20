from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient
from index_document import Indexation
from items import AllInfoItem, URLItem

from settings import MONGODB_URI, MONGODB_DB, MONGODB_COLLECTION_URLS

class MongoDBPipeline(object):
    def open_spider(self, spider):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[MONGODB_DB]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, URLItem):
            print("Inserting URL", item["url"])
            self.db[MONGODB_COLLECTION_URLS].insert_one(dict(item))

        if isinstance(item, AllInfoItem):
            self.index_document(item)
            print("Document indexed:", item["url"])
        
        return item

    def index_document(self, item):
        with ThreadPoolExecutor() as executor:
            executor.submit(Indexation().index_document, item)