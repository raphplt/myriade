# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['kgkiller']
collection = db['documents']
