from pymongo import MongoClient

from items import URLItem

from settings import MONGODB_URI, MONGODB_DB, MONGODB_COLLECTION_URLS

class MongoDBPipeline(object):
    def open_spider(self, spider):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[MONGODB_DB]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, URLItem):
            print("Inserting URL")
            self.db[MONGODB_COLLECTION_URLS].insert_one(dict(item))
        else:
            print("Unknown item type:", type(item))
        return item
