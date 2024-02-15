BOT_NAME = "gkiller" # Name of the bot
SPIDER_MODULES = ["spiders"] # List of modules where the spiders are located
NEWSPIDER_MODULE = "spiders" # Module where the new spiders are located
ROBOTSTXT_OBEY = True # Obey the robots.txt file
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7" # Fingerprinting implementation
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor" # Twisted reactor
FEED_EXPORT_ENCODING = "utf-8" # Export encoding
MONGODB_URI = 'mongodb://localhost:27017/' # MongoDB URI
MONGODB_DB = 'gkiller' # MongoDB database
MONGODB_COLLECTION_ALL_INFO = 'documents_details' # MongoDB collection for documents details
MONGODB_COLLECTION_INDEX = 'index' # MongoDB collection for index
MONGODB_COLLECTION_URLS = 'urls' # MongoDB collection for URLs
ITEM_PIPELINES = { # Item pipelines
    'pipelines.MongoDBPipeline': 300,
}
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'