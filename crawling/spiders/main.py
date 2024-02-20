import scrapy
from urllib.parse import urljoin, urlparse
from pymongo import MongoClient
from settings import MONGODB_COLLECTION_ALL_INFO, MONGODB_COLLECTION_URLS, MONGODB_DB, MONGODB_URI
from items import AllInfoItem, URLItem

class MainSpider(scrapy.Spider):
    name = "main_spider"
    
    def remove_newlines_and_multiple_spaces(self, content):
        content_without_newlines = content.replace('\n', '')
        content_without_multiple_spaces = ' '.join(content_without_newlines.split())
        return content_without_multiple_spaces

    def start_requests(self):
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DB]
        collection = db[MONGODB_COLLECTION_URLS]

        # Fetch only URLs that are not marked as 'done'
        urls = collection.find({'done': {'$exists': False}}, {'url': 1})

        for url_doc in urls:
            url = url_doc['url']
            if self.is_valid_url(url):
                yield scrapy.Request(url, callback=self.parse, meta={'url_doc_id': url_doc['_id']})
            else:
                self.logger.warning(f"Skipping invalid URL: {url}")

    def parse(self, response):
        
        if response.headers.get('Content-Type') == b'application/pdf':
            self.logger.info(f"Ignoring PDF document: {response.url}")
            return 
        
        all_info_item = AllInfoItem()

        if response.css('title::text'):
            all_info_item['title'] = response.css('title::text').get()

        if response.css('p::text'):
            content = response.css('p::text').getall()
            cleaned_content = self.remove_newlines_and_multiple_spaces(' '.join(content)) if content else ''
            all_info_item['content'] = cleaned_content

        all_info_item['url'] = response.url


        links = response.css('a::attr(href)').getall()

        # Delete links starting with #
        links = [link for link in links if not link.startswith("#")]
        links = [link for link in links if not link.startswith("mailto:")]
        links = [link for link in links if not link.startswith("javascript")]
        links = [link for link in links if not link.startswith("tel:")]
        links = [link for link in links if not link.startswith("whatsapp:")]
        links = [link for link in links if not link.startswith("sms:")]
        links = [link for link in links if not link.startswith("callto:")]
        links = [link for link in links if not link.startswith("skype:")]
        links = [link for link in links if not link.startswith("facetime:")]
        links = [link for link in links if not link.startswith("tg:")]
        links = [link for link in links if not link.startswith("viber:")]
        links = [link for link in links if not link.startswith("fb-messenger:")]
        links = [link for link in links if not link.startswith("line:")]
        links = [link for link in links if not link.startswith("weixin:")]
        links = [link for link in links if not link.startswith("whatsapp:")]
        links = [link for link in links if not link.startswith("skype:")]
        links = [link for link in links if not link.startswith("mailto:")]
        
        # Make all links absolute
        links = [urljoin(response.url, link) for link in links]

        all_info_item['links'] = list(set(links))

        # Save document details to MongoDB
        self.save_document_details(all_info_item)

        yield all_info_item

        # Update 'done' field for the processed URL
        url_doc_id = response.meta['url_doc_id']
        self.mark_url_as_done(url_doc_id)

        # Parsing for URLItem
        for link in all_info_item['links'] or []:
            if self.is_valid_url(link):
                url_item = URLItem()
                url_item['url'] = link
                yield url_item
            else:
                self.logger.warning(f"Skipping invalid URL found in document: {link}")

    def mark_url_as_done(self, url_doc_id):
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DB]
        collection = db[MONGODB_COLLECTION_URLS]
        collection.update_one({'_id': url_doc_id}, {'$set': {'done': True}})

    def save_document_details(self, all_info_item):
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DB]
        collection = db[MONGODB_COLLECTION_ALL_INFO]
        collection.insert_one(dict(all_info_item))

    def is_valid_url(self, url):
        return bool(urlparse(url).scheme)
