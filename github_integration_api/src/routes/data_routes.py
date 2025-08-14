from fastapi import APIRouter, Query
from ..controllers.data_controller import DataController
from typing import Optional

router = APIRouter(tags=["Data Management"])

@router.get("/data/{collection}")
async def get_collection_data(
    collection: str,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: Optional[str] = Query(None, description="Field name to sort by"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Sort order: asc or desc"),
    filter: Optional[str] = Query(None, description="JSON object of filters"),
    search: Optional[str] = Query(None, description="Keyword search across all fields")
):

    return await DataController.get_collection_data(
        collection=collection,
        page=page,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        filter_json=filter,
        search=search
    )

@router.get("/search")
async def global_search(q: str = Query(..., min_length=2, description="Search keyword")):
    return await DataController.global_search(q)
