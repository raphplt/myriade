
from typing import List, Union
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import json
import uvicorn
from sklearn.feature_extraction.text import TfidfVectorizer
import logging
import time

logging.basicConfig(level=logging.DEBUG)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["gkiller"]
collection_index = db["index"]
collection_details = db["documents_details"]

async def search_index(query: str) -> List[dict]:
    cursor = collection_index.find({"word": query})
    results = [document async for document in cursor]
    return results

async def get_document_details(url: str) -> Union[dict, None]:
    document = await collection_details.find_one({"url": url})
    if document:
        return {
            "title": document.get("title", ""),
            "content": document.get("content", "")[:200],
        }
    else:
        return None

async def calculate_tfidf_scores(query: str, urls: List[str]) -> dict:

    documents = [await collection_details.find_one({"url": url}) for url in urls]
    document_texts = [doc["content"] for doc in documents if doc and "content" in doc]
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(document_texts)
    # terms = tfidf_vectorizer.get_feature_names_out()
    term_index = tfidf_vectorizer.vocabulary_.get(query)
    if term_index is None:
        return {}
    tfidf_scores = {url: score for url, score in zip(urls, tfidf_matrix[:, term_index].toarray().flatten())}

    return tfidf_scores

async def search_with_tfidf(query: str, tfidf_scores: dict) -> List[dict]:

    search_results = await search_index(query)
    detailed_results = []
    
    for result in search_results:
        word = result["word"]
        documents = result["documents"]
        detailed_documents = []
        
        for doc in documents:
            for url in doc:
                details = await get_document_details(url)
                if details:
                    tfidf_score = tfidf_scores.get(url, 0)
                    detailed_documents.append({
                        "url": url,
                        "details": details,
                        "tfidf_score": tfidf_score
                    })
        
        detailed_documents.sort(key=lambda x: x["tfidf_score"], reverse=True)
        
        if detailed_documents:  
            detailed_results.append({
                "word": word,
                "documents": detailed_documents
            })
    
    logging.info(f"Search with TF-IDF done for query: {query}")
    return detailed_results

@app.get("/search/")
async def search_api(query: str = Query(...)):
    if query is None:
        return {"error": "Aucune requête de recherche spécifiée."}
    
    start_time = time.time()
    
    keywords = query.split()
    combined_results = []
    
    for keyword in keywords:
        search_results = await search_index(keyword)
        relevant_urls = []
        
        for result in search_results:
            documents = result["documents"]
            for doc in documents:
                relevant_urls.extend(doc.keys())
        
        relevant_urls = list(set(relevant_urls))
        tfidf_scores = await calculate_tfidf_scores(keyword, relevant_urls)
        search_results = await search_with_tfidf(keyword, tfidf_scores)
        combined_results.extend([item["documents"] for item in search_results])
    
    combined_results = [item for sublist in combined_results for item in sublist]
    
    combined_results.sort(key=lambda x: x["tfidf_score"], reverse=True)
    
    end_time = time.time()
    duration = end_time - start_time
    
    response = {"results": combined_results, "time": duration}
    
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
