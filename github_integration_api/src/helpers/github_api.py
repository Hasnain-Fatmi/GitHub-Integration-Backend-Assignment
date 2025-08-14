import httpx
from typing import Dict, List, Any, Optional
from ..config import settings

class GitHubAPI:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Integration-API"
        }

    async def make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}{endpoint}",
                    headers=self.headers,
                    params=params or {}
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Error making request to {endpoint}: {e}")
                return None

    async def get_user_info(self) -> Optional[Dict[str, Any]]:
        return await self.make_request("/user")

    async def get_user_organizations(self) -> List[Dict[str, Any]]:
        result = await self.make_request("/user/orgs")
        return result if result else []

    async def get_organization_repos(self, org: str, page: int = 1, per_page: int = 100) -> List[Dict[str, Any]]:
        params = {"page": page, "per_page": per_page}
        result = await self.make_request(f"/orgs/{org}/repos", params)
        return result if result else []

    async def get_user_repos(self, page: int = 1, per_page: int = 100) -> List[Dict[str, Any]]:
        params = {"page": page, "per_page": per_page}
        result = await self.make_request("/user/repos", params)
        return result if result else []

    async def get_repository_commits(self, owner: str, repo: str, page: int = 1, per_page: int = 100) -> List[Dict[str, Any]]:
        params = {"page": page, "per_page": per_page}
        result = await self.make_request(f"/repos/{owner}/{repo}/commits", params)
        return result if result else []

    async def get_repository_pulls(self, owner: str, repo: str, state: str = "all", page: int = 1, per_page: int = 100) -> List[Dict[str, Any]]:
        params = {"state": state, "page": page, "per_page": per_page}
        result = await self.make_request(f"/repos/{owner}/{repo}/pulls", params)
        return result if result else []

    async def get_repository_issues(self, owner: str, repo: str, state: str = "all", page: int = 1, per_page: int = 100) -> List[Dict[str, Any]]:
        params = {"state": state, "page": page, "per_page": per_page}
        result = await self.make_request(f"/repos/{owner}/{repo}/issues", params)
        return result if result else []

    async def get_repository_issue_events(self, owner: str, repo: str, page: int = 1, per_page: int = 100) -> List[Dict[str, Any]]:
        params = {"page": page, "per_page": per_page}
        result = await self.make_request(f"/repos/{owner}/{repo}/issues/events", params)
        return result if result else []

    async def get_organization_members(self, org: str, page: int = 1, per_page: int = 100) -> List[Dict[str, Any]]:
        params = {"page": page, "per_page": per_page}
        result = await self.make_request(f"/orgs/{org}/members", params)
        return result if result else []

async def exchange_code_for_token(code: str) -> Optional[str]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://github.com/login/oauth/access_token",
                data={
                    "client_id": settings.github_client_id,
                    "client_secret": settings.github_client_secret,
                    "code": code,
                    "redirect_uri": settings.github_redirect_uri
                },
                headers={"Accept": "application/json"}
            )
            response.raise_for_status()
            data = response.json()
            return data.get("access_token")
        except Exception as e:
            print(f"Error exchanging code for token: {e}")
            return None
