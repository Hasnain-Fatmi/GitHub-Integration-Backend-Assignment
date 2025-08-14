from fastapi import HTTPException, Query
from ..helpers.database import find_many, count_documents, search_across_collections
from typing import Dict, Any, Optional
import json

class DataController:
    
    ALLOWED_COLLECTIONS = [
        "github_organizations",
        "github_repos", 
        "github_commits",
        "github_pulls",
        "github_issues",
        "github_changelogs",
        "github_users"
    ]
    
    @staticmethod
    async def get_collection_data(
        collection: str,
        page: int = 1,
        limit: int = 20,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
        filter_json: Optional[str] = None,
        search: Optional[str] = None
    ):
        if collection not in DataController.ALLOWED_COLLECTIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Collection '{collection}' not allowed. Allowed collections: {DataController.ALLOWED_COLLECTIONS}"
            )
        
        # Validate pagination
        if page < 1:
            page = 1
        if limit < 1 or limit > 100:
            limit = 20
        
        # Calculate skip
        skip = (page - 1) * limit
        
        # Parse filter
        filter_dict = {}
        if filter_json:
            try:
                filter_dict = json.loads(filter_json)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid filter JSON format")
        
        # search functionality
        if search:
            search_conditions = {
                "$or": [
                    {"name": {"$regex": search, "$options": "i"}},
                    {"title": {"$regex": search, "$options": "i"}},
                    {"description": {"$regex": search, "$options": "i"}},
                    {"login": {"$regex": search, "$options": "i"}},
                    {"full_name": {"$regex": search, "$options": "i"}},
                    {"body": {"$regex": search, "$options": "i"}}
                ]
            }
            
            if filter_dict:
                filter_dict = {"$and": [filter_dict, search_conditions]}
            else:
                filter_dict = search_conditions
        
        sort_order_int = 1 if sort_order.lower() == "asc" else -1
        
        documents = await find_many(
            collection_name=collection,
            filter_dict=filter_dict,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order_int
        )
        
        total_count = await count_documents(collection, filter_dict)
        
        # Calculate pagination info
        total_pages = (total_count + limit - 1) // limit
        has_next = page < total_pages
        has_prev = page > 1
        
        return {
            "data": documents,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_items": total_count,
                "items_per_page": limit,
                "has_next": has_next,
                "has_previous": has_prev
            },
            "meta": {
                "collection": collection,
                "filters_applied": bool(filter_dict),
                "search_applied": bool(search),
                "sort_by": sort_by,
                "sort_order": sort_order
            }
        }
    
    @staticmethod
    async def global_search(keyword: str):
        if not keyword or len(keyword.strip()) < 2:
            raise HTTPException(status_code=400, detail="Search keyword must be at least 2 characters long")
        
        results = await search_across_collections(keyword, DataController.ALLOWED_COLLECTIONS)
        
        total_results = sum(len(items) for items in results.values())
        
        return {
            "keyword": keyword,
            "total_results": total_results,
            "results": results,
            "collections_searched": DataController.ALLOWED_COLLECTIONS
        }
