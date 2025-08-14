import motor.motor_asyncio
from typing import Dict, List, Any, Optional
import json
from bson import ObjectId
from ..config import settings

class Database:
    client: motor.motor_asyncio.AsyncIOMotorClient = None
    database: motor.motor_asyncio.AsyncIOMotorDatabase = None

db = Database()

async def connect_to_mongo():
    db.client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url)
    db.database = db.client[settings.database_name]

async def close_mongo_connection():
    if db.client:
        db.client.close()

async def get_collection(collection_name: str):
    return db.database[collection_name]

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

async def insert_one(collection_name: str, document: Dict[str, Any]) -> str:
    collection = await get_collection(collection_name)
    result = await collection.insert_one(document)
    return str(result.inserted_id)

async def insert_many(collection_name: str, documents: List[Dict[str, Any]]) -> List[str]:
    collection = await get_collection(collection_name)
    result = await collection.insert_many(documents)
    return [str(id) for id in result.inserted_ids]

async def find_one(collection_name: str, filter_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    collection = await get_collection(collection_name)
    document = await collection.find_one(filter_dict)
    if document:
        document['_id'] = str(document['_id'])
    return document

async def find_many(
    collection_name: str,
    filter_dict: Dict[str, Any] = None,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = None,
    sort_order: int = 1
) -> List[Dict[str, Any]]:
    collection = await get_collection(collection_name)
    
    query = collection.find(filter_dict or {})
    
    if sort_by:
        query = query.sort(sort_by, sort_order)
    
    query = query.skip(skip).limit(limit)
    
    documents = []
    async for document in query:
        document['_id'] = str(document['_id'])
        documents.append(document)
    
    return documents

async def count_documents(collection_name: str, filter_dict: Dict[str, Any] = None) -> int:
    collection = await get_collection(collection_name)
    return await collection.count_documents(filter_dict or {})

async def update_one(collection_name: str, filter_dict: Dict[str, Any], update_dict: Dict[str, Any]) -> bool:
    collection = await get_collection(collection_name)
    result = await collection.update_one(filter_dict, {"$set": update_dict})
    return result.modified_count > 0

async def delete_one(collection_name: str, filter_dict: Dict[str, Any]) -> bool:
    collection = await get_collection(collection_name)
    result = await collection.delete_one(filter_dict)
    return result.deleted_count > 0

async def delete_many(collection_name: str, filter_dict: Dict[str, Any] = None) -> int:
    collection = await get_collection(collection_name)
    result = await collection.delete_many(filter_dict or {})
    return result.deleted_count

async def search_across_collections(keyword: str, collections: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    results = {}
    
    for collection_name in collections:
        collection = await get_collection(collection_name)
        
        query = {"$text": {"$search": keyword}}
        
        try:
            documents = []
            async for doc in collection.find(query).limit(50):
                doc['_id'] = str(doc['_id'])
                documents.append(doc)
            results[collection_name] = documents
        except:
    
            regex_query = {
                "$or": [
                    {"name": {"$regex": keyword, "$options": "i"}},
                    {"title": {"$regex": keyword, "$options": "i"}},
                    {"description": {"$regex": keyword, "$options": "i"}},
                    {"login": {"$regex": keyword, "$options": "i"}},
                    {"full_name": {"$regex": keyword, "$options": "i"}},
                    {"body": {"$regex": keyword, "$options": "i"}}
                ]
            }
            
            documents = []
            async for doc in collection.find(regex_query).limit(50):
                doc['_id'] = str(doc['_id'])
                documents.append(doc)
            results[collection_name] = documents
    
    return results
