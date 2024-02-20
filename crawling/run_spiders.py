from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient

from settings import MONGODB_COLLECTION_URLS, MONGODB_DB, MONGODB_URI, CONCURRENT_REQUESTS, CONCURRENT_REQUESTS_PER_DOMAIN
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
    else:
        print(f"Collection {MONGODB_COLLECTION_URLS} already exists")

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
    
    # while True:
        
    create_urls_collection()
    urls = [
        "https://www.francetvinfo.fr/",
        "https://www.lemonde.fr/",
        "https://www.lefigaro.fr/",
        "https://www.liberation.fr/",
        "https://www.20minutes.fr/",
        "https://www.la-croix.com/",
        "https://www.leparisien.fr/",
        "https://www.lci.fr/",
        "https://www.bfmtv.com/",
        "https://www.cnews.fr/",
        "https://www.rtl.fr/",
        "https://www.europe1.fr/",
        "https://www.franceinter.fr/",
        "https://www.franceinfo.fr/",
        "https://www.rfi.fr/",
        "https://www.lesechos.fr/",
        "https://stackoverflow.com/questions",
        "https://www.reddit.com/r/Python/",
        "https://www.reddit.com/r/learnpython/",
        "https://www.reddit.com/r/programming/",
        "https://www.reddit.com/r/technology/",
        "https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal",
        "https://github.com/",
        "https://gitlab.com/",
        "https://bitbucket.org/",
        "https://www.python.org/",
    ]

    if check_urls_collection_empty():
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DB]
        collection = db[MONGODB_COLLECTION_URLS]
        collection.insert_many([{'url': url} for url in urls])

    run_spiders()

        # time.sleep(5)
        
if __name__ == "__main__":
    main()
