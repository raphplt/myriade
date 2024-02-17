from typing import List, Union
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import uvicorn
import logging
import time
import unidecode
from fuzzywuzzy import fuzz

logging.basicConfig(level=logging.DEBUG)

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

def normalize_text(text: str) -> str:
    return unidecode.unidecode(text).lower()

async def perform_search(query: str) -> List[dict]:
    similar_words = []
    normalized_query = normalize_text(query)
    async for document in collection_index.find():
        word = document["word"]
        normalized_word = normalize_text(word)
        similarity_ratio = fuzz.ratio(normalized_query, normalized_word)
        if similarity_ratio > 80:
            documents = await collection_details.find({
                "$or": [
                    {"title": {"$regex": f".*{word}.*", "$options": "i"}},
                    {"content": {"$regex": f".*{word}.*", "$options": "i"}}
                ]
            }).to_list(None)
            
            occurrences = sum(1 for doc in documents if word.lower() in doc["title"].lower() or word.lower() in doc["content"].lower())
            
            similar_words.append({
                "word": word,
                "similarity_ratio": similarity_ratio,
                "documents": documents,
                "occurrences": occurrences
            })
    return similar_words

async def calculate_tfidf_scores(query: str, urls: List[str]) -> dict:
    documents = [await collection_details.find_one({"url": url}) for url in urls]
    document_texts = [doc["content"] for doc in documents if doc and "content" in doc]
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(document_texts)
    term_index = tfidf_vectorizer.vocabulary_.get(query)
    if term_index is None:
        return {}
    tfidf_scores = {url: score for url, score in zip(urls, tfidf_matrix[:, term_index].toarray().flatten())}
    return tfidf_scores

async def search_with_tfidf(query: str, tfidf_scores: dict) -> List[dict]:
    search_results = await perform_search(query)
    detailed_results = []
    for result in search_results:
        word = result["word"]
        documents = result["documents"]
        detailed_documents = []
        for doc in documents:
            url = doc.get("url")  
            if url:
                tfidf_score = tfidf_scores.get(url, 0)
                details = doc  
                detailed_documents.append({
                    "url": url,
                    "details": details,
                    "tfidf_score": tfidf_score
                })
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
    tfidf_scores_combined = {}
    combined_results = {}
    
    for keyword in keywords:
        search_results = await perform_search(keyword)
        print("search_results", search_results)
        relevant_urls = []
        for result in search_results:
            documents = result["documents"]
            for doc in documents:
                url = doc.get("url") 
                if url:
                    relevant_urls.append(url)
        relevant_urls = list(set(relevant_urls))
        tfidf_scores = await calculate_tfidf_scores(keyword, relevant_urls)
        tfidf_scores_combined.update(tfidf_scores)
        search_results_with_tfidf = await search_with_tfidf(keyword, tfidf_scores)
        for result in search_results_with_tfidf:
            word = result["word"]
            if word not in combined_results:
                combined_results[word] = {"documents": []}
            combined_results[word]["documents"].extend(result["documents"])
    
    for word, data in combined_results.items():
        data["documents"].sort(key=lambda x: x["tfidf_score"], reverse=True)
    
    end_time = time.time()
    duration = end_time - start_time
    
    for result in combined_results.values():
        result["time"] = duration
    
    return {"results": list(combined_results.values())}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
