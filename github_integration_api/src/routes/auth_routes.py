from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from ..controllers.auth_controller import AuthController

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/github/login")
async def github_login():
    github_url = AuthController.get_github_login_url()
    return RedirectResponse(url=github_url)

@router.get("/github/callback")
async def github_callback(code: str = None, error: str = None):
   
    if error:
        raise HTTPException(status_code=400, detail=f"GitHub authorization error: {error}")
    
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")
    
    result = await AuthController.handle_github_callback(code)
    return result
