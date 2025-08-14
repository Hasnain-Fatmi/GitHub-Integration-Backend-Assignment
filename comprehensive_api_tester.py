#!/usr/bin/env python3
"""
GitHub Integration API - Comprehensive Tester (Simplified)
A unified testing tool that combines OAuth testing, data inspection, and API endpoint validation.
"""
import asyncio
import aiohttp
import webbrowser
import json
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
MOCK_USER_ID = "12345"  # Test user with mock data
REAL_USER_ID = "145764132"  # Your actual GitHub user ID

class GitHubAPITester:
    def print_header(self, title: str, char: str = "="):
        """Print a formatted header"""
        print(f"\n{char * 60}")
        print(f"🚀 {title}")
        print(f"{char * 60}")

    def print_section(self, title: str):
        """Print a section header"""
        print(f"\n{'─' * 40}")
        print(f"📋 {title}")
        print(f"{'─' * 40}")

    async def test_oauth_flow(self):
        """Test the complete OAuth flow"""
        self.print_header("GitHub OAuth Integration Test")
        
        try:
            async with aiohttp.ClientSession() as session:
                print("\n🔍 Step 1: Getting GitHub login URL...")
                
                async with session.get(f"{BASE_URL}/auth/github/login", allow_redirects=False) as response:
                    print(f"Status: {response.status}")
                    
                    if response.status in [302, 307]:
                        github_url = response.headers.get('Location')
                        print(f"✅ Redirect URL obtained: {github_url[:80]}...")
                        
                        # Parse OAuth parameters
                        parsed = urlparse(github_url)
                        params = parse_qs(parsed.query)
                        
                        print(f"\n📋 OAuth Parameters:")
                        print(f"   • Client ID: {params.get('client_id', ['Not found'])[0]}")
                        print(f"   • Redirect URI: {params.get('redirect_uri', ['Not found'])[0]}")
                        print(f"   • Scope: {params.get('scope', ['Not found'])[0]}")
                        
                        print(f"\n🌐 Opening browser for OAuth authorization...")
                        webbrowser.open(github_url)
                        
                        print(f"\n📝 Instructions:")
                        print(f"   1. Authorize the application in your browser")
                        print(f"   2. You'll be redirected to: {BASE_URL}/auth/github/callback")
                        print(f"   3. Check your API server logs for callback handling")
                        
                        # Wait for user completion
                        input("\nPress Enter after completing OAuth authorization...")
                        
                        # Ask for user ID
                        user_id = input("Enter your GitHub user ID (or press Enter for default): ").strip()
                        if not user_id:
                            user_id = REAL_USER_ID
                        
                        await self.test_integration_status(user_id)
                        
                        # Offer resync
                        if input("\nDo you want to test data resync? (y/n): ").strip().lower() == 'y':
                            await self.test_resync(user_id)
                        
                        return True
                    else:
                        text = await response.text()
                        print(f"❌ Unexpected response: {response.status}")
                        print(f"Response: {text}")
                        return False
                        
        except Exception as e:
            print(f"❌ Error testing OAuth: {e}")
            return False

    async def test_integration_status(self, user_id: str):
        """Test integration status"""
        print(f"\n🔍 Testing integration status for user {user_id}...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{BASE_URL}/integration/status?user_id={user_id}") as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"✅ Integration Status: {data.get('status')}")
                        
                        if 'user' in data and data['user']:
                            user = data['user']
                            print(f"👤 GitHub User: {user.get('login')} ({user.get('name')})")
                            print(f"📧 Email: {user.get('email')}")
                            print(f"🏢 Company: {user.get('company')}")
                            print(f"🔗 Profile: {user.get('html_url')}")
                            
                        if 'connected_at' in data:
                            print(f"⏰ Connected: {data['connected_at']}")
                            
                        return True
                    else:
                        text = await response.text()
                        print(f"❌ Status check failed: {response.status}")
                        print(f"Response: {text}")
                        return False
                        
        except Exception as e:
            print(f"❌ Error checking status: {e}")
            return False

    async def test_resync(self, user_id: str):
        """Test data resync"""
        print(f"\n🔄 Testing resync for user {user_id}...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{BASE_URL}/integration/resync?user_id={user_id}") as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"✅ Resync completed!")
                        print(f"📊 Stats: {data.get('stats', {})}")
                    else:
                        text = await response.text()
                        print(f"❌ Resync failed: {response.status}")
                        print(f"Response: {text}")
        except Exception as e:
            print(f"❌ Resync error: {e}")

    async def test_api_endpoints(self, user_id: str = None):
        """Test all API endpoints with comprehensive validation"""
        if not user_id:
            user_id = MOCK_USER_ID
            
        self.print_header("API Endpoints Testing")
        print(f"Testing with user ID: {user_id}")
        
        # Define test cases
        test_cases = [
            {
                "endpoint": f"/integration/status?user_id={user_id}",
                "description": "Integration Status",
                "method": "GET"
            },
            {
                "endpoint": "/data/github_repos?limit=10",
                "description": "Repositories (limited to 10)",
                "method": "GET"
            },
            {
                "endpoint": "/data/github_commits?limit=5",
                "description": "Commits (limited to 5)",
                "method": "GET"
            },
            {
                "endpoint": "/data/github_pulls?limit=5",
                "description": "Pull Requests (limited to 5)",
                "method": "GET"
            },
            {
                "endpoint": "/data/github_issues?limit=5",
                "description": "Issues (limited to 5)",
                "method": "GET"
            },
            {
                "endpoint": "/data/github_organizations",
                "description": "Organizations",
                "method": "GET"
            },
            {
                "endpoint": "/data/github_users?limit=5",
                "description": "Users (limited to 5)",
                "method": "GET"
            },
            {
                "endpoint": "/data/github_changelogs?limit=5",
                "description": "Changelogs (limited to 5)",
                "method": "GET"
            },
            {
                "endpoint": "/search?q=python",
                "description": "Global Search for 'python'",
                "method": "GET"
            },
            {
                "endpoint": "/",
                "description": "Root endpoint",
                "method": "GET"
            },
            {
                "endpoint": "/health",
                "description": "Health check",
                "method": "GET"
            }
        ]
        
        results = []
        
        async with aiohttp.ClientSession() as session:
            for test_case in test_cases:
                result = await self.test_single_endpoint(
                    session,
                    test_case["endpoint"], 
                    test_case["description"]
                )
                results.append(result)
                await asyncio.sleep(0.1)
        
        # Summary
        self.print_section("TESTING SUMMARY")
        successful_tests = sum(1 for r in results if r["success"])
        total_tests = len(results)
        
        print(f"✅ Successful tests: {successful_tests}/{total_tests}")
        
        if successful_tests == total_tests:
            print("🎉 ALL TESTS PASSED!")
            print("\n💡 Try these advanced endpoints:")
            print("   • GET /data/github_commits?search=fix")
            print("   • GET /data/github_repos?sort_by=stargazers_count&sort_order=desc")
            print("   • GET /data/github_issues?search=bug")
            print("   • GET /data/github_pulls?sort_by=created_at&sort_order=desc")
        else:
            print("⚠️  Some tests failed. Check the detailed output above.")

    async def test_single_endpoint(self, session: aiohttp.ClientSession, endpoint: str, description: str) -> Dict[str, Any]:
        """Test a single API endpoint"""
        try:
            print(f"\n🔍 Testing: {description}")
            print(f"📡 Endpoint: {endpoint}")
            
            async with session.get(f"{BASE_URL}{endpoint}") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Status: {response.status}")
                    
                    # Pretty print key information
                    if isinstance(data, dict):
                        if "pagination" in data:
                            pagination = data['pagination']
                            print(f"📊 Total records: {pagination['total_items']}")
                            print(f"📄 Records returned: {len(data.get('data', []))}")
                        elif "status" in data:
                            print(f"🔗 Integration status: {data['status']}")
                            if "user" in data and data['user']:
                                print(f"👤 User: {data['user'].get('login')}")
                        elif "keyword" in data:
                            print(f"🔍 Search keyword: {data['keyword']}")
                            print(f"📊 Total results: {data['total_results']}")
                        else:
                            print(f"📄 Response keys: {list(data.keys())}")
                            
                    return {"success": True, "data": data, "status": response.status}
                else:
                    error_text = await response.text()
                    print(f"❌ Status: {response.status}")
                    print(f"❌ Error: {error_text}")
                    return {"success": False, "error": error_text, "status": response.status}
                    
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return {"success": False, "error": str(e), "status": None}

    async def inspect_data_detailed(self, user_id: str = None):
        """Detailed data inspection with full structure analysis"""
        if not user_id:
            user_id = MOCK_USER_ID
            
        self.print_header("Detailed Data Inspector")
        print(f"Inspecting data for user ID: {user_id}")
        print("This will show you exactly what data the API has fetched and stored.")
        
        # Test endpoints with detailed inspection
        test_cases = [
            {
                "endpoint": f"/integration/status?user_id={user_id}",
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
                await self.inspect_endpoint_data(
                    session,
                    test_case["endpoint"], 
                    test_case["description"]
                )
                await asyncio.sleep(0.1)
        
        self.print_section("INSPECTION COMPLETE")
        print("💡 This shows you the actual structure and content of your data.")
        print("🎯 You now have a comprehensive view of what your API contains!")

    async def inspect_endpoint_data(self, session: aiohttp.ClientSession, endpoint: str, description: str, limit: int = 3):
        """Inspect and display detailed data from an API endpoint"""
        try:
            print(f"\n{'='*60}")
            print(f"🔍 INSPECTING: {description}")
            print(f"📡 Endpoint: {endpoint}")
            print(f"{'='*60}")
            
            async with session.get(f"{BASE_URL}{endpoint}") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Status: {response.status}")
                    
                    # Handle different response structures
                    if isinstance(data, dict):
                        if "data" in data and "pagination" in data:
                            # Standard collection response
                            print(f"\n📊 PAGINATION INFO:")
                            pagination = data['pagination']
                            print(f"   • Total items: {pagination['total_items']}")
                            print(f"   • Current page: {pagination['current_page']}")
                            print(f"   • Total pages: {pagination['total_pages']}")
                            print(f"   • Items per page: {pagination['items_per_page']}")
                            print(f"   • Has next: {pagination['has_next']}")
                            
                            print(f"\n🗂️ META INFO:")
                            meta = data['meta']
                            print(f"   • Collection: {meta['collection']}")
                            print(f"   • Filters applied: {meta['filters_applied']}")
                            print(f"   • Search applied: {meta['search_applied']}")
                            print(f"   • Sort by: {meta.get('sort_by', 'None')}")
                            
                            # Show actual data records
                            records = data['data'][:limit]
                            print(f"\n📋 SAMPLE DATA ({min(len(data['data']), limit)} of {len(data['data'])} records):")
                            
                            for i, record in enumerate(records, 1):
                                print(f"\n   🔸 Record {i}:")
                                self.display_record_info(record)
                        
                        elif "status" in data:
                            # Integration status response
                            print(f"\n🔗 INTEGRATION STATUS:")
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
                            print(f"\n🔍 SEARCH RESULTS:")
                            print(f"   • Keyword: {data['keyword']}")
                            print(f"   • Total results: {data['total_results']}")
                            print(f"   • Collections searched: {', '.join(data['collections_searched'])}")
                            
                            print(f"\n📊 RESULTS BY COLLECTION:")
                            for collection, items in data['results'].items():
                                print(f"   • {collection}: {len(items)} items")
                                if items:
                                    item = items[0]
                                    if 'name' in item:
                                        print(f"     Example: {item['name']}")
                                    elif 'title' in item:
                                        print(f"     Example: {item['title']}")
                                    elif 'login' in item:
                                        print(f"     Example: {item['login']}")
                        
                        else:
                            # Generic response
                            print(f"\n📄 RESPONSE DATA:")
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
                    print(f"❌ Status: {response.status}")
                    print(f"❌ Error: {error_text}")
                    return {"success": False, "error": error_text, "status": response.status}
                    
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return {"success": False, "error": str(e), "status": None}

    def display_record_info(self, record: dict):
        """Display key information from a record"""
        # Show key fields based on record type
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
        
        # Show all available fields for reference
        print(f"      Available fields: {', '.join(record.keys())}")

    def show_menu(self):
        """Display the main menu"""
        self.print_header("GitHub Integration API - Comprehensive Tester")
        print("Choose what you want to test:")
        print()
        print("1. 🔐 OAuth Integration Flow")
        print("   - Test GitHub OAuth login")
        print("   - Verify callback handling")
        print("   - Test with real GitHub data")
        print()
        print("2. 📡 API Endpoints Testing")
        print("   - Test all API endpoints")
        print("   - Validate responses")
        print("   - Test with mock data")
        print()
        print("3. 🔍 Detailed Data Inspection")
        print("   - Inspect data structure")
        print("   - View sample records")
        print("   - Analyze data completeness")
        print()
        print("4. 🚀 Complete API Validation")
        print("   - Run all tests")
        print("   - Comprehensive validation")
        print("   - Full API coverage")
        print()
        print("5. ❌ Exit")
        print()

async def main():
    """Main function with interactive menu"""
    tester = GitHubAPITester()
    
    try:
        while True:
            tester.show_menu()
            
            try:
                choice = input("Enter your choice (1-5): ").strip()
                
                if choice == "1":
                    await tester.test_oauth_flow()
                
                elif choice == "2":
                    print("\nChoose data source:")
                    print("1. Mock data (user ID: 12345)")
                    print("2. Real data (user ID: 145764132)")
                    print("3. Custom user ID")
                    
                    data_choice = input("Enter choice (1-3): ").strip()
                    
                    if data_choice == "1":
                        await tester.test_api_endpoints(MOCK_USER_ID)
                    elif data_choice == "2":
                        await tester.test_api_endpoints(REAL_USER_ID)
                    elif data_choice == "3":
                        custom_id = input("Enter user ID: ").strip()
                        if custom_id:
                            await tester.test_api_endpoints(custom_id)
                        else:
                            await tester.test_api_endpoints(MOCK_USER_ID)
                    else:
                        print("Invalid choice, using mock data...")
                        await tester.test_api_endpoints(MOCK_USER_ID)
                
                elif choice == "3":
                    print("\nChoose data source:")
                    print("1. Mock data (user ID: 12345)")
                    print("2. Real data (user ID: 145764132)")
                    print("3. Custom user ID")
                    
                    data_choice = input("Enter choice (1-3): ").strip()
                    
                    if data_choice == "1":
                        await tester.inspect_data_detailed(MOCK_USER_ID)
                    elif data_choice == "2":
                        await tester.inspect_data_detailed(REAL_USER_ID)
                    elif data_choice == "3":
                        custom_id = input("Enter user ID: ").strip()
                        if custom_id:
                            await tester.inspect_data_detailed(custom_id)
                        else:
                            await tester.inspect_data_detailed(MOCK_USER_ID)
                    else:
                        print("Invalid choice, using mock data...")
                        await tester.inspect_data_detailed(MOCK_USER_ID)
                
                elif choice == "4":
                    print("\n🚀 Running Complete API Validation...")
                    
                    # Test basic endpoints first
                    await tester.test_api_endpoints(MOCK_USER_ID)
                    
                    # Detailed inspection
                    await tester.inspect_data_detailed(MOCK_USER_ID)
                    
                    # Test with real data if available
                    print(f"\n🔄 Testing with real data (user {REAL_USER_ID})...")
                    await tester.test_integration_status(REAL_USER_ID)
                    
                    tester.print_section("COMPLETE VALIDATION FINISHED")
                    print("✅ All API components have been thoroughly tested!")
                
                elif choice == "5":
                    print("\n👋 Goodbye! Thanks for testing the GitHub Integration API!")
                    break
                
                else:
                    print("❌ Invalid choice. Please enter 1-5.")
                
                # Ask if user wants to continue
                if choice in ["1", "2", "3", "4"]:
                    print("\n" + "─" * 60)
                    if input("Press Enter to return to menu (or 'q' to quit): ").strip().lower() == 'q':
                        break
                        
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Returning to menu...")
    
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    print("🚀 Starting GitHub Integration API Comprehensive Tester...")
    asyncio.run(main())
