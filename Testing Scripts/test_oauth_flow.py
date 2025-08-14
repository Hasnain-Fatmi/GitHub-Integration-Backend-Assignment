import asyncio
import aiohttp
import webbrowser
from urllib.parse import urlparse, parse_qs

BASE_URL = "http://localhost:8000"

async def test_oauth_flow():

    print("GitHub OAuth Integration Test")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
  
        print("\nStep 1: Getting GitHub login URL...")
        
        try:
            async with session.get(f"{BASE_URL}/auth/github/login", allow_redirects=False) as response:
                print(f"Status: {response.status}")
                
                if response.status == 302 or response.status == 307:
                    github_url = response.headers.get('Location')
                    print(f"Redirect URL obtained: {github_url[:80]}...")
                    
                    parsed = urlparse(github_url)
                    params = parse_qs(parsed.query)
                    
                    print(f"\nOAuth Parameters:")
                    print(f"   • Client ID: {params.get('client_id', ['Not found'])[0]}")
                    print(f"   • Redirect URI: {params.get('redirect_uri', ['Not found'])[0]}")
                    print(f"   • Scope: {params.get('scope', ['Not found'])[0]}")
                    
                    print(f"\nOpening browser for OAuth authorization...")
                    print(f"   URL: {github_url}")
                    
                    webbrowser.open(github_url)
                    
                    print(f"\nInstructions:")
                    print(f"   1. Authorize the application in your browser")
                    print(f"   2. You'll be redirected to: {BASE_URL}/auth/github/callback")
                    print(f"   3. Check your API server logs to see the callback handling")
                    print(f"   4. After authorization, test with your real user ID")
                    
                    return True
                    
                else:
                    text = await response.text()
                    print(f"Unexpected response: {response.status}")
                    print(f"Response: {text}")
                    return False
                    
        except Exception as e:
            print(f"Error testing OAuth: {e}")
            return False

async def test_integration_status_after_oauth(user_id: str):

    print(f"\nTesting integration status for user {user_id}...")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/integration/status?user_id={user_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"Integration Status: {data.get('status')}")
                    
                    if 'user' in data and data['user']:
                        user = data['user']
                        print(f"GitHub User: {user.get('login')} ({user.get('name')})")
                        print(f"Email: {user.get('email')}")
                        print(f"Company: {user.get('company')}")
                        print(f"Profile: {user.get('html_url')}")
                        
                    if 'connected_at' in data:
                        print(f"Connected: {data['connected_at']}")
                        
                    return True
                else:
                    text = await response.text()
                    print(f"Status check failed: {response.status}")
                    print(f"Response: {text}")
                    return False
                    
        except Exception as e:
            print(f"Error checking status: {e}")
            return False

async def main():
 
    print("Testing GitHub OAuth Integration")
    print("=" * 50)
 
    oauth_success = await test_oauth_flow()
    
    if oauth_success:
        print(f"\n" + "=" * 50)
        print("NEXT STEPS:")
        print("=" * 50)
        print("1. Complete the OAuth flow in your browser")
        print("2. After authorization, find your GitHub user ID")
        print("3. Test integration status with your real user ID")
        print("4. Use resync to fetch your real GitHub data")
        
        input("\nPress Enter after completing OAuth authorization...")
        
        user_id = input("Enter your GitHub user ID: ").strip()
        
        if user_id:
            await test_integration_status_after_oauth(user_id)
            
            resync = input("\nDo you want to test data resync? (y/n): ").strip().lower()
            if resync == 'y':
                print(f"\nTesting resync for user {user_id}...")
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.post(f"{BASE_URL}/integration/resync?user_id={user_id}") as response:
                            if response.status == 200:
                                data = await response.json()
                                print(f"Resync completed!")
                                print(f"Stats: {data.get('stats', {})}")
                            else:
                                text = await response.text()
                                print(f"Resync failed: {response.status}")
                                print(f"Response: {text}")
                    except Exception as e:
                        print(f"Resync error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
