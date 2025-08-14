import asyncio
import aiohttp
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
TEST_USER_ID = "12345"

async def inspect_endpoint_data(session: aiohttp.ClientSession, endpoint: str, description: str, limit: int = 3):

    try:
        print(f"\n{'='*60}")
        print(f" INSPECTING: {description}")
        print(f" Endpoint: {endpoint}")
        print(f"{'='*60}")
        
        async with session.get(f"{BASE_URL}{endpoint}") as response:
            if response.status == 200:
                data = await response.json()
                print(f" Status: {response.status}")
                
                # Handle different response structures
                if isinstance(data, dict):
                    if "data" in data and "pagination" in data:
                        # Standard collection response
                        print(f"\n PAGINATION INFO:")
                        pagination = data['pagination']
                        print(f"   • Total items: {pagination['total_items']}")
                        print(f"   • Current page: {pagination['current_page']}")
                        print(f"   • Total pages: {pagination['total_pages']}")
                        print(f"   • Items per page: {pagination['items_per_page']}")
                        print(f"   • Has next: {pagination['has_next']}")
                        
                        print(f"\n META INFO:")
                        meta = data['meta']
                        print(f"   • Collection: {meta['collection']}")
                        print(f"   • Filters applied: {meta['filters_applied']}")
                        print(f"   • Search applied: {meta['search_applied']}")
                        print(f"   • Sort by: {meta.get('sort_by', 'None')}")
                        
                        # Show actual data records
                        records = data['data'][:limit] 
                        print(f"\n SAMPLE DATA ({min(len(data['data']), limit)} of {len(data['data'])} records):")
                        
                        for i, record in enumerate(records, 1):
                            print(f"\n   🔸 Record {i}:")
                            
                            if 'name' in record:
                                print(f"      Name: {record['name']}")
                            if 'title' in record:
                                print(f"      Title: {record['title']}")
                            if 'login' in record:
                                print(f"      Login: {record['login']}")
                            if 'full_name' in record:
                                print(f"      Full Name: {record['full_name']}")
                            if 'description' in record:
                                desc = record['description']
                                if desc and len(desc) > 80:
                                    desc = desc[:80] + "..."
                                print(f"      Description: {desc}")
                            if 'sha' in record:
                                print(f"      SHA: {record['sha'][:12]}...")
                            if 'commit' in record and 'message' in record['commit']:
                                msg = record['commit']['message']
                                if len(msg) > 60:
                                    msg = msg[:60] + "..."
                                print(f"      Commit: {msg}")
                            if 'state' in record:
                                print(f"      State: {record['state']}")
                            if 'created_at' in record:
                                print(f"      Created: {record['created_at']}")
                            if 'stargazers_count' in record:
                                print(f"      Stars: {record['stargazers_count']}")
                            if 'primary_language' in record:
                                print(f"      Language: {record['primary_language']}")
                            
                            print(f"      Available fields: {', '.join(record.keys())}")
                    
                    elif "status" in data:

                        print(f"\n INTEGRATION STATUS:")
                        print(f"   • Status: {data['status']}")
                        if "user" in data and data['user']:
                            user = data['user']
                            print(f"   • User ID: {user.get('id')}")
                            print(f"   • Username: {user.get('login')}")
                            print(f"   • Name: {user.get('name')}")
                            print(f"   • Email: {user.get('email')}")
                            print(f"   • Company: {user.get('company')}")
                            print(f"   • Location: {user.get('location')}")
                            print(f"   • Public repos: {user.get('public_repos')}")
                        if "connected_at" in data:
                            print(f"   • Connected at: {data['connected_at']}")
                        if "last_sync" in data:
                            print(f"   • Last sync: {data['last_sync']}")
                    
                    elif "keyword" in data and "results" in data:
                        # Search response
                        print(f"\n SEARCH RESULTS:")
                        print(f"   • Keyword: {data['keyword']}")
                        print(f"   • Total results: {data['total_results']}")
                        print(f"   • Collections searched: {', '.join(data['collections_searched'])}")
                        
                        print(f"\n RESULTS BY COLLECTION:")
                        for collection, items in data['results'].items():
                            print(f"   • {collection}: {len(items)} items")
                            if items:
                                # Show first item from each collection
                                item = items[0]
                                if 'name' in item:
                                    print(f"     Example: {item['name']}")
                                elif 'title' in item:
                                    print(f"     Example: {item['title']}")
                                elif 'login' in item:
                                    print(f"     Example: {item['login']}")
                    
                    else:
                    
                        print(f"\n RESPONSE DATA:")
                        for key, value in data.items():
                            if isinstance(value, (str, int, float, bool)):
                                print(f"   • {key}: {value}")
                            elif isinstance(value, list):
                                print(f"   • {key}: [{len(value)} items]")
                            elif isinstance(value, dict):
                                print(f"   • {key}: {{...}} (nested object)")
                
                return {"success": True, "data": data, "status": response.status}
            else:
                error_text = await response.text()
                print(f" Status: {response.status}")
                print(f" Error: {error_text}")
                return {"success": False, "error": error_text, "status": response.status}
                
    except Exception as e:
        print(f" Exception: {str(e)}")
        return {"success": False, "error": str(e), "status": None}

async def main():

    print(" GitHub Integration API - Detailed Data Inspector")
    print("=" * 60)
    print("This will show you exactly what data the API has fetched and stored.")
    print("=" * 60)
    
    # Test endpoints with detailed inspection
    test_cases = [
        {
            "endpoint": f"/integration/status?user_id={TEST_USER_ID}",
            "description": "Integration Status & User Info"
        },
        {
            "endpoint": "/data/github_organizations",
            "description": "GitHub Organizations"
        },
        {
            "endpoint": "/data/github_repos?limit=5",
            "description": "GitHub Repositories"
        },
        {
            "endpoint": "/data/github_commits?limit=3",
            "description": "GitHub Commits"
        },
        {
            "endpoint": "/data/github_pulls?limit=3",
            "description": "GitHub Pull Requests"
        },
        {
            "endpoint": "/data/github_issues?limit=3",
            "description": "GitHub Issues"
        },
        {
            "endpoint": "/data/github_users?limit=5",
            "description": "GitHub Users/Members"
        },
        {
            "endpoint": "/data/github_changelogs?limit=3",
            "description": "GitHub Issue Events/Changelogs"
        },
        {
            "endpoint": "/search?q=python",
            "description": "Global Search Results"
        }
    ]
    
    async with aiohttp.ClientSession() as session:
        for test_case in test_cases:
            await inspect_endpoint_data(
                session, 
                test_case["endpoint"], 
                test_case["description"]
            )
            await asyncio.sleep(0.1) 
    
    print(f"\n{'='*60}")
    print(" INSPECTION COMPLETE")
    print(f"{'='*60}")
    print(" This shows you the actual structure and content of your test data.")
    print(" You now have a comprehensive view of what your API contains!")

if __name__ == "__main__":
    asyncio.run(main())
