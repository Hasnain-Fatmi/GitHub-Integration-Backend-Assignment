import uvicorn
from github_integration_api.src.server import app

if __name__ == "__main__":
    uvicorn.run(
        "github_integration_api.src.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
