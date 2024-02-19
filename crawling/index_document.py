import logging
from settings import MONGODB_COLLECTION_INDEX, MONGODB_DB, MONGODB_URI 
from pymongo import MongoClient

class Indexation():
    
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[MONGODB_DB]
        self.index = self.db[MONGODB_COLLECTION_INDEX]
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        
    def index_document(self, document):
        try:
            document_url = document['url']
            document_title = document['title']
            document_content = document.get('content', '')

            # Vérifier si le document est déjà indexé
            if self.index.find_one({'documents.url': document_url}):
                self.logger.info(f"Document already indexed: {document_url}")
                return

            unique_words = set(document_title.split() + document_content.split())

            for word in unique_words:
                word = word.lower().strip(".,;:!?()[]{}-_")
                existing_entry = self.index.find_one({'word': word})
                if existing_entry:
                    document_entry = next((entry for entry in existing_entry['documents'] if document_url in entry), None)
                    if document_entry:
                        document_entry[document_url] += 1
                    else:
                        existing_entry['documents'].append({document_url: 1})
                        self.index.update_one({'_id': existing_entry['_id']}, {'$set': {'documents': existing_entry['documents']}})
                else:
                    self.index.insert_one({'word': word, 'documents': [{document_url: 1}]})
            
            self.logger.info(f"Document indexed: {document_url}")

        except KeyError as e:
            self.logger.error(f"Error indexing document {document['url']}: {e}")
        except Exception as e:
            self.logger.error(f"Error indexing document {document['url']}: {e}")
            raise
