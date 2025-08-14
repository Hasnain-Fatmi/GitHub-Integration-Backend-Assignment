from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .routes import auth_routes, integration_routes, data_routes
from .helpers.database import connect_to_mongo, close_mongo_connection
from .config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):

    try:

        settings.validate_required_settings()
        print(" Environment configuration validated")
        
        await connect_to_mongo()
        print(" Connected to MongoDB")
        
    except Exception as e:
        print(f" Startup failed: {e}")
        raise
        
    yield
    
    await close_mongo_connection()
    print(" Disconnected from MongoDB")

app = FastAPI(
    title="GitHub Integration API",
    description="FastAPI backend for GitHub OAuth integration and data management",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(integration_routes.router)
app.include_router(data_routes.router)

@app.get("/")
async def root():

    return {
        "message": "GitHub Integration API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():

    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.server:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )
