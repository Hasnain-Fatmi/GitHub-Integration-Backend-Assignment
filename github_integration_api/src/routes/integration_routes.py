from fastapi import APIRouter, HTTPException
from ..controllers.integration_controller import IntegrationController

router = APIRouter(prefix="/integration", tags=["Integration Management"])

@router.get("/status")
async def get_integration_status(user_id: int):
    
    return await IntegrationController.get_integration_status(user_id)

@router.post("/remove")
async def remove_integration(user_id: int):
    
    return await IntegrationController.remove_integration(user_id)

@router.post("/resync")
async def resync_integration_data(user_id: int):
    
    return await IntegrationController.resync_data(user_id)
