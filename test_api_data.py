import asyncio
import aiohttp
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
TEST_USER_ID = "12345"

async def test_endpoint(session: aiohttp.ClientSession, endpoint: str, description: str) -> Dict[str, Any]:

    try:
        print(f"\nTesting: {description}")
        print(f"Endpoint: {endpoint}")
        
        async with session.get(f"{BASE_URL}{endpoint}") as response:
            if response.status == 200:
                data = await response.json()
                print(f" Status: {response.status}")
                
                # Pretty print key information
                if isinstance(data, dict):
                    if "total" in data and "data" in data:
                        print(f"Total records: {data['total']}")
                        print(f"Records returned: {len(data['data'])}")
                        if data['data']:
                            print(f"Sample record keys: {list(data['data'][0].keys())}")
                    elif "status" in data:
                        print(f"Integration status: {data['status']}")
                        if "user_info" in data:
                            print(f"User: {data['user_info']['login']}")
                    else:
                        print(f"Response keys: {list(data.keys())}")
                        
                return {"success": True, "data": data, "status": response.status}
            else:
                error_text = await response.text()
                print(f"Status: {response.status}")
                print(f"Error: {error_text}")
                return {"success": False, "error": error_text, "status": response.status}
                
    except Exception as e:
        print(f"Exception: {str(e)}")
        return {"success": False, "error": str(e), "status": None}

async def main():

    print("GitHub Integration API - Testing with Generated Data")
    print("=" * 60)
    
    # Test endpoints
    test_cases = [
        {
            "endpoint": f"/integration/status?user_id={TEST_USER_ID}",
            "description": "Integration Status"
        },
        {
            "endpoint": "/data/github_repos?limit=10",
            "description": "Repositories (limited to 10)"
        },
        {
            "endpoint": "/data/github_commits?limit=5",
            "description": "Commits (limited to 5)"
        },
        {
            "endpoint": "/data/github_pulls?limit=5",
            "description": "Pull Requests (limited to 5)"
        },
        {
            "endpoint": "/data/github_issues?limit=5",
            "description": "Issues (limited to 5)"
        },
        {
            "endpoint": "/data/github_organizations",
            "description": "Organizations"
        },
        {
            "endpoint": "/data/github_users?limit=5",
            "description": "Users (limited to 5)"
        },
        {
            "endpoint": "/data/github_changelogs?limit=5",
            "description": "Changelogs (limited to 5)"
        },
        {
            "endpoint": "/search?q=python",
            "description": "Global Search for 'python'"
        }
    ]
    
    results = []
    
    async with aiohttp.ClientSession() as session:
        for test_case in test_cases:
            result = await test_endpoint(
                session, 
                test_case["endpoint"], 
                test_case["description"]
            )
            results.append(result)
            await asyncio.sleep(0.1)
    
    print("\n" + "=" * 60)
    print("TESTING SUMMARY")
    print("=" * 60)
    
    successful_tests = sum(1 for r in results if r["success"])
    total_tests = len(results)
    
    print(f"Successful tests: {successful_tests}/{total_tests}")
    
    if successful_tests == total_tests:
        print("ALL TESTS PASSED!")
    else:
        print("Some tests failed. Check the detailed output above.")

if __name__ == "__main__":
    asyncio.run(main())
