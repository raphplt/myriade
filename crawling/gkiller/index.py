from gkiller.settings import MONGODB_COLLECTION_URLS, MONGODB_COLLECTION_ALL_INFO, MONGODB_DB, MONGODB_URI
from pymongo import MongoClient

class Indexation():
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[MONGODB_DB]
        
        