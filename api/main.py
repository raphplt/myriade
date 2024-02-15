from typing import List, Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import json
import uvicorn


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = FastAPI()

# Ajouter le middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vous pouvez spécifier les origines autorisées ici
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
    document = await collection_details.find_one({ "url": url})
    if document:
        return {
            "title": document.get("title", ""),
            "content": document.get("content", "")[:100],
            "url": document.get("url", "")
        }
    else:
        return None


@app.get("/search/")
async def search(query: str = None):
    if query is None:
        return {"error": "Aucune requête de recherche spécifiée."}
    
    search_results = await search_index(query)
    detailed_results = []
    
    for result in search_results:
        documents = result["documents"]
        detailed_documents = []
        
        for doc in documents:
            for url in doc:
                details = await get_document_details(url)
                if details:
                    detailed_documents.append({
                        "url": url,
                        "details": details
                    })
        
        if detailed_documents:  
            detailed_results.append({
                "word": result["word"],
                "documents": detailed_documents
            })
    
    return {"results": detailed_results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
