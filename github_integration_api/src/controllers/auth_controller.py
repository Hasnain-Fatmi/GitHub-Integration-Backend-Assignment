from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from ..config import settings
from ..helpers.github_api import GitHubAPI, exchange_code_for_token
from ..helpers.database import insert_one, find_one, update_one
from ..models.github_models import GitHubIntegration, GitHubUser
from datetime import datetime
import urllib.parse

class AuthController:
    
    @staticmethod
    def get_github_login_url():
        params = {
            "client_id": settings.github_client_id,
            "redirect_uri": settings.github_redirect_uri,
            "scope": "user:email,read:org,repo",
            "prompt": "consent"
        }
        query_string = urllib.parse.urlencode(params)
        return f"https://github.com/login/oauth/authorize?{query_string}"

    @staticmethod
    async def handle_github_callback(code: str):
        if not code:
            raise HTTPException(status_code=400, detail="Authorization code is required")
        
        access_token = await exchange_code_for_token(code)
        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to get access token")
        
        github_api = GitHubAPI(access_token)
        user_info = await github_api.get_user_info()
        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to get user info from GitHub")
        
        existing_integration = await find_one("github_integration", {"user_id": user_info["id"]})
        
        github_user = GitHubUser(**user_info)
        integration_data = {
            "user_id": user_info["id"],
            "access_token": access_token,
            "user_info": github_user.model_dump(),
            "integration_status": "active",
            "connected_at": datetime.utcnow(),
            "last_sync": None
        }
        
        if existing_integration:
            await update_one(
                "github_integration", 
                {"user_id": user_info["id"]}, 
                integration_data
            )
        else:
            await insert_one("github_integration", integration_data)
        
        return {
            "message": "GitHub integration successful",
            "user": github_user.model_dump(),
            "status": "connected"
        }
