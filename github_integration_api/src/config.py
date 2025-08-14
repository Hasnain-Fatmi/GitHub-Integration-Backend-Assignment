import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "github_integration"
    
    github_client_id: str = ""
    github_client_secret: str = ""
    github_redirect_uri: str = "http://localhost:8000/auth/github/callback"
    
    secret_key: str = ""
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        
    def validate_required_settings(self):
        """Validate that all required settings are provided"""
        missing = []
        
        if not self.github_client_id:
            missing.append("GITHUB_CLIENT_ID")
        if not self.github_client_secret:
            missing.append("GITHUB_CLIENT_SECRET")
        if not self.secret_key:
            missing.append("SECRET_KEY")
            
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}. "
                f"Please copy .env.example to .env and fill in the required values."
            )

settings = Settings()
