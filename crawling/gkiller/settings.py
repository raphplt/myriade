BOT_NAME = "gkiller"
SPIDER_MODULES = ["gkiller.spiders"]
NEWSPIDER_MODULE = "gkiller.spiders"
ROBOTSTXT_OBEY = True
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
MONGODB_URI = 'mongodb://localhost:27017/'
MONGODB_DB = 'gkiller'
MONGODB_COLLECTION_ALL_INFO = 'documents_details'
MONGODB_COLLECTION_URLS = 'urls'
ITEM_PIPELINES = {
    'gkiller.pipelines.MongoDBPipeline': 300,
}
