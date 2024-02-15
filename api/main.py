from typing import List, Union
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import json

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = FastAPI()

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["gkiller"]
collection = db["index"]

async def search_index(query: str) -> List[dict]:
    cursor = collection.find({"word": query})
    
    results = [document async for document in cursor]
    
    return results

@app.get("/search/")
async def search(query: str):
    search_results = await search_index(query)
    documents = [result["documents"] for result in search_results]
    return {"results": documents}
