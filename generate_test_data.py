import asyncio
import motor.motor_asyncio
import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json

# Test Configuration
TEST_ORG_NAME = "test-organization-api"
TEST_USER_ID = 12345
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "github_integration"

class GitHubTestDataGenerator:
    def __init__(self):
        self.client = None
        self.db = None
        self.stats = {
            "organizations": 0,
            "repositories": 0,
            "commits": 0,
            "pulls": 0,
            "issues": 0,
            "users": 0,
            "changelogs": 0
        }

    async def connect(self):

        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
        self.db = self.client[DATABASE_NAME]
        print(" Connected to MongoDB")

    async def disconnect(self):

        if self.client:
            self.client.close()
        print(" Disconnected from MongoDB")

    def generate_sha(self) -> str:

        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=40))

    def generate_realistic_commit_message(self, index: int) -> str:
      
        messages = [
            f"Fix bug in authentication module (#{index})",
            f"Add new feature for user management (#{index})",
            f"Update documentation for API endpoints (#{index})",
            f"Refactor database connection logic (#{index})",
            f"Improve error handling in controllers (#{index})",
            f"Add unit tests for integration module (#{index})",
            f"Update dependencies to latest versions (#{index})",
            f"Fix memory leak in data processing (#{index})",
            f"Optimize query performance for large datasets (#{index})",
            f"Add validation for input parameters (#{index})",
            f"Implement caching for frequently accessed data (#{index})",
            f"Fix race condition in async operations (#{index})",
            f"Add logging for better debugging (#{index})",
            f"Update configuration management (#{index})",
            f"Improve security for API endpoints (#{index})",
            f"Add support for new GitHub API features (#{index})",
            f"Fix pagination issues in data retrieval (#{index})",
            f"Optimize memory usage in large data processing (#{index})",
            f"Add error recovery mechanisms (#{index})",
            f"Update API documentation with examples (#{index})"
        ]
        return random.choice(messages)

    def generate_random_date(self, start_date: datetime, end_date: datetime) -> str:

        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        random_hours = random.randint(0, 23)
        random_minutes = random.randint(0, 59)
        random_seconds = random.randint(0, 59)
        
        result_date = start_date + timedelta(
            days=random_days,
            hours=random_hours,
            minutes=random_minutes,
            seconds=random_seconds
        )
        return result_date.isoformat() + "Z"

    async def create_test_integration(self):

        print("\n Creating test integration...")
        
        integration_data = {
            "user_id": TEST_USER_ID,
            "access_token": "test_token_for_comprehensive_testing",
            "user_info": {
                "id": TEST_USER_ID,
                "login": "test-api-user",
                "name": "Test API User",
                "email": "test@github-integration-api.com",
                "avatar_url": "https://github.com/avatars/u/12345",
                "html_url": "https://github.com/test-api-user",
                "type": "User",
                "company": "GitHub Integration API Testing",
                "location": "Test Environment",
                "bio": "Test user for GitHub Integration API comprehensive testing",
                "public_repos": 15,
                "followers": 50,
                "following": 30,
                "created_at": "2020-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            },
            "integration_status": "active",
            "connected_at": datetime.utcnow(),
            "last_sync": datetime.utcnow()
        }

        await self.db["github_integration"].delete_many({"user_id": TEST_USER_ID})
        await self.db["github_integration"].insert_one(integration_data)
        
        print(" Test integration created")

    async def create_test_organization(self):

        print("\n Creating test organization...")
        
        org_data = {
            "id": 100001,
            "login": TEST_ORG_NAME,
            "name": "Test Organization for API Testing",
            "description": "A comprehensive test organization for GitHub Integration API testing with large datasets",
            "html_url": f"https://github.com/{TEST_ORG_NAME}",
            "avatar_url": f"https://github.com/avatars/u/100001",
            "location": "Test Environment",
            "email": "contact@test-organization-api.com",
            "public_repos": 25,
            "followers": 150,
            "following": 75,
            "created_at": "2020-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "type": "Organization",
            "integration_user_id": TEST_USER_ID
        }
        
        await self.db["github_organizations"].delete_many({"integration_user_id": TEST_USER_ID})
        await self.db["github_organizations"].insert_one(org_data)
        self.stats["organizations"] = 1
        
        print(f" Created organization: {TEST_ORG_NAME}")

    async def create_test_repositories(self) -> List[Dict[str, Any]]:

        print("\n Creating test repositories...")
        
        repositories = [
            {
                "name": "awesome-python-api",
                "description": "A comprehensive Python API with advanced features and 2000+ commits",
                "language": "Python",
                "topics": ["python", "api", "fastapi", "async", "testing"]
            },
            {
                "name": "react-typescript-dashboard",
                "description": "Modern React TypeScript dashboard with extensive commit history",
                "language": "TypeScript", 
                "topics": ["react", "typescript", "dashboard", "frontend", "ui"]
            },
            {
                "name": "golang-microservice",
                "description": "High-performance Go microservice with comprehensive testing",
                "language": "Go",
                "topics": ["go", "microservice", "kubernetes", "docker", "api"]
            },
            {
                "name": "nodejs-backend-service",
                "description": "Node.js backend service with extensive development history",
                "language": "JavaScript",
                "topics": ["nodejs", "express", "mongodb", "backend", "rest"]
            },
            {
                "name": "rust-performance-library",
                "description": "High-performance Rust library with detailed development history",
                "language": "Rust",
                "topics": ["rust", "performance", "library", "systems", "async"]
            }
        ]
        
        repo_documents = []
        start_id = 200001
        
        for i, repo_info in enumerate(repositories):
            repo_data = {
                "id": start_id + i,
                "name": repo_info["name"],
                "full_name": f"{TEST_ORG_NAME}/{repo_info['name']}",
                "owner": {
                    "login": TEST_ORG_NAME,
                    "id": 100001,
                    "type": "Organization"
                },
                "private": False,
                "html_url": f"https://github.com/{TEST_ORG_NAME}/{repo_info['name']}",
                "description": repo_info["description"],
                "fork": False,
                "created_at": self.generate_random_date(
                    datetime(2021, 1, 1), 
                    datetime(2022, 1, 1)
                ),
                "updated_at": self.generate_random_date(
                    datetime(2024, 1, 1), 
                    datetime(2024, 8, 1)
                ),
                "pushed_at": self.generate_random_date(
                    datetime(2024, 7, 1), 
                    datetime(2024, 8, 13)
                ),
                "size": random.randint(5000, 50000),
                "stargazers_count": random.randint(100, 2000),
                "watchers_count": random.randint(50, 500),
                "primary_language": repo_info["language"],
                "forks_count": random.randint(10, 200),
                "open_issues_count": random.randint(5, 50),
                "default_branch": "main",
                "archived": False,
                "disabled": False,
                "topics": repo_info["topics"],
                "integration_user_id": TEST_USER_ID
            }
            repo_documents.append(repo_data)
        
        # Clean existing and insert new
        await self.db["github_repos"].delete_many({"integration_user_id": TEST_USER_ID})
        await self.db["github_repos"].insert_many(repo_documents)
        self.stats["repositories"] = len(repo_documents)
        
        print(f" Created {len(repo_documents)} repositories")
        return repo_documents

    async def create_commits_for_repo(self, repo: Dict[str, Any], commit_count: int = 2500):
        
        print(f" Creating {commit_count} commits for {repo['name']}...")
        
        commits = []
        developers = [
            {"name": "Alice Johnson", "email": "alice@test-org.com"},
            {"name": "Bob Smith", "email": "bob@test-org.com"},
            {"name": "Charlie Brown", "email": "charlie@test-org.com"},
            {"name": "Diana Prince", "email": "diana@test-org.com"},
            {"name": "Ethan Hunt", "email": "ethan@test-org.com"},
            {"name": "Fiona Apple", "email": "fiona@test-org.com"},
            {"name": "George Lucas", "email": "george@test-org.com"},
            {"name": "Hannah Montana", "email": "hannah@test-org.com"}
        ]
        
        start_date = datetime.fromisoformat(repo["created_at"].replace("Z", ""))
        end_date = datetime.fromisoformat(repo["updated_at"].replace("Z", ""))
        
        batch_size = 500  # Insert in batches to avoid memory issues
        batch = []
        
        for i in range(commit_count):
            author = random.choice(developers)
            committer = random.choice(developers)
            commit_date = self.generate_random_date(start_date, end_date)
            
            commit_data = {
                "sha": self.generate_sha(),
                "commit": {
                    "author": {
                        "name": author["name"],
                        "email": author["email"],
                        "date": commit_date
                    },
                    "committer": {
                        "name": committer["name"],
                        "email": committer["email"],
                        "date": commit_date
                    },
                    "message": self.generate_realistic_commit_message(i + 1)
                },
                "author": {
                    "login": author["name"].lower().replace(" ", ""),
                    "id": random.randint(300001, 300100),
                    "avatar_url": f"https://github.com/avatars/u/{random.randint(300001, 300100)}"
                },
                "committer": {
                    "login": committer["name"].lower().replace(" ", ""),
                    "id": random.randint(300001, 300100),
                    "avatar_url": f"https://github.com/avatars/u/{random.randint(300001, 300100)}"
                },
                "parents": [{"sha": self.generate_sha()}] if i > 0 else [],
                "html_url": f"https://github.com/{repo['full_name']}/commit/{self.generate_sha()}",
                "repository": repo["full_name"],
                "integration_user_id": TEST_USER_ID
            }
            
            batch.append(commit_data)
            
            # Insert batch when it reaches batch_size
            if len(batch) >= batch_size:
                await self.db["github_commits"].insert_many(batch)
                batch = []
                if i % 1000 == 0:
                    print(f" Progress: {i}/{commit_count} commits created")
        
        # Insert remaining commits
        if batch:
            await self.db["github_commits"].insert_many(batch)
        
        self.stats["commits"] += commit_count
        print(f" Created {commit_count} commits for {repo['name']}")

    async def create_pull_requests_for_repo(self, repo: Dict[str, Any], pr_count: int = 12):
        
        print(f" Creating {pr_count} pull requests for {repo['name']}...")
        
        pr_titles = [
            "Add comprehensive API documentation",
            "Implement user authentication system", 
            "Fix critical security vulnerability",
            "Add unit tests for core functionality",
            "Optimize database query performance",
            "Implement real-time notifications",
            "Add support for multiple languages",
            "Fix memory leak in data processing",
            "Add monitoring and health checks",
            "Implement advanced search functionality",
            "Add data export capabilities",
            "Improve error handling and logging"
        ]
        
        developers = ["alice-dev", "bob-coder", "charlie-eng", "diana-arch", "ethan-lead"]
        states = ["open", "closed", "merged"]
        
        pull_requests = []
        start_date = datetime.fromisoformat(repo["created_at"].replace("Z", ""))
        end_date = datetime.fromisoformat(repo["updated_at"].replace("Z", ""))
        
        for i in range(pr_count):
            developer = random.choice(developers)
            state = random.choice(states)
            created_date = self.generate_random_date(start_date, end_date)
            
            pr_data = {
                "id": 400001 + i + (repo["id"] * 100),
                "number": i + 1,
                "state": state,
                "title": pr_titles[i % len(pr_titles)],
                "user": {
                    "login": developer,
                    "id": random.randint(300001, 300100),
                    "avatar_url": f"https://github.com/avatars/u/{random.randint(300001, 300100)}"
                },
                "body": f"This pull request implements {pr_titles[i % len(pr_titles)].lower()} with comprehensive testing and documentation. "
                       f"Addresses issue #{random.randint(1, 50)} and includes performance improvements.",
                "created_at": created_date,
                "updated_at": self.generate_random_date(
                    datetime.fromisoformat(created_date.replace("Z", "")),
                    end_date
                ),
                "closed_at": self.generate_random_date(
                    datetime.fromisoformat(created_date.replace("Z", "")),
                    end_date
                ) if state in ["closed", "merged"] else None,
                "merged_at": self.generate_random_date(
                    datetime.fromisoformat(created_date.replace("Z", "")),
                    end_date
                ) if state == "merged" else None,
                "merge_commit_sha": self.generate_sha() if state == "merged" else None,
                "head": {
                    "ref": f"feature/pr-{i+1}",
                    "sha": self.generate_sha()
                },
                "base": {
                    "ref": "main", 
                    "sha": self.generate_sha()
                },
                "html_url": f"https://github.com/{repo['full_name']}/pull/{i+1}",
                "repository": repo["full_name"],
                "integration_user_id": TEST_USER_ID
            }
            pull_requests.append(pr_data)
        
        await self.db["github_pulls"].insert_many(pull_requests)
        self.stats["pulls"] += pr_count
        print(f" Created {pr_count} pull requests for {repo['name']}")

    async def create_issues_for_repo(self, repo: Dict[str, Any], issue_count: int = 15):
        print(f" Creating {issue_count} issues for {repo['name']}...")
        
        issue_titles = [
            "API response time is too slow for large datasets",
            "Memory leak in data processing module",
            "Authentication fails for certain user types", 
            "Database connection pool exhaustion",
            "Inconsistent error messages across endpoints",
            "Missing validation for input parameters",
            "Performance degradation with concurrent requests",
            "Improper handling of edge cases in search",
            "Security vulnerability in file upload",
            "Race condition in async operations",
            "Incorrect pagination for filtered results",
            "Cache invalidation not working properly",
            "Logging system missing important events",
            "Configuration changes require server restart",
            "Data export functionality is broken"
        ]
        
        labels_options = [
            [{"name": "bug", "color": "d73a4a"}],
            [{"name": "enhancement", "color": "a2eeef"}],
            [{"name": "documentation", "color": "0075ca"}],
            [{"name": "good first issue", "color": "7057ff"}],
            [{"name": "help wanted", "color": "008672"}],
            [{"name": "priority: high", "color": "d93f0b"}],
            [{"name": "priority: medium", "color": "fbca04"}],
            [{"name": "priority: low", "color": "0e8a16"}]
        ]
        
        reporters = ["user-reporter", "qa-tester", "product-manager", "developer-intern", "external-contributor"]
        states = ["open", "closed"]
        
        issues = []
        start_date = datetime.fromisoformat(repo["created_at"].replace("Z", ""))
        end_date = datetime.fromisoformat(repo["updated_at"].replace("Z", ""))
        
        for i in range(issue_count):
            reporter = random.choice(reporters)
            state = random.choice(states)
            created_date = self.generate_random_date(start_date, end_date)
            
            issue_data = {
                "id": 500001 + i + (repo["id"] * 100),
                "number": i + 1,
                "title": issue_titles[i % len(issue_titles)],
                "user": {
                    "login": reporter,
                    "id": random.randint(400001, 400100),
                    "avatar_url": f"https://github.com/avatars/u/{random.randint(400001, 400100)}"
                },
                "labels": random.choice(labels_options),
                "state": state,
                "assignee": {
                    "login": random.choice(["alice-dev", "bob-coder", "charlie-eng"]),
                    "id": random.randint(300001, 300100)
                } if random.choice([True, False]) else None,
                "assignees": [],
                "milestone": None,
                "comments": random.randint(0, 25),
                "created_at": created_date,
                "updated_at": self.generate_random_date(
                    datetime.fromisoformat(created_date.replace("Z", "")),
                    end_date
                ),
                "closed_at": self.generate_random_date(
                    datetime.fromisoformat(created_date.replace("Z", "")),
                    end_date
                ) if state == "closed" else None,
                "body": f"**Issue Description:**\n\n{issue_titles[i % len(issue_titles)]}\n\n"
                       f"**Steps to Reproduce:**\n1. Navigate to the problematic functionality\n"
                       f"2. Perform the action that triggers the issue\n3. Observe the unexpected behavior\n\n"
                       f"**Expected Behavior:**\nThe system should handle this case gracefully.\n\n"
                       f"**Actual Behavior:**\nThe issue manifests as described in the title.",
                "html_url": f"https://github.com/{repo['full_name']}/issues/{i+1}",
                "repository": repo["full_name"],
                "integration_user_id": TEST_USER_ID
            }
            issues.append(issue_data)
        
        await self.db["github_issues"].insert_many(issues)
        self.stats["issues"] += issue_count
        print(f" Created {issue_count} issues for {repo['name']}")

    async def create_organization_members(self):
       
        print("\n Creating organization members...")
        
        members = [
            {"login": "alice-johnson", "name": "Alice Johnson", "role": "admin"},
            {"login": "bob-smith", "name": "Bob Smith", "role": "member"},
            {"login": "charlie-brown", "name": "Charlie Brown", "role": "member"},
            {"login": "diana-prince", "name": "Diana Prince", "role": "member"},
            {"login": "ethan-hunt", "name": "Ethan Hunt", "role": "member"},
            {"login": "fiona-apple", "name": "Fiona Apple", "role": "member"},
            {"login": "george-lucas", "name": "George Lucas", "role": "member"},
            {"login": "hannah-montana", "name": "Hannah Montana", "role": "member"}
        ]
        
        user_documents = []
        for i, member in enumerate(members):
            user_data = {
                "id": 600001 + i,
                "login": member["login"],
                "name": member["name"],
                "email": f"{member['login']}@{TEST_ORG_NAME}.com",
                "avatar_url": f"https://github.com/avatars/u/{600001 + i}",
                "html_url": f"https://github.com/{member['login']}",
                "type": "User",
                "company": "Test Organization API",
                "location": "Test Environment",
                "bio": f"Software developer at {TEST_ORG_NAME}",
                "public_repos": random.randint(5, 50),
                "followers": random.randint(10, 500),
                "following": random.randint(5, 200),
                "created_at": self.generate_random_date(
                    datetime(2020, 1, 1),
                    datetime(2022, 1, 1)
                ),
                "updated_at": self.generate_random_date(
                    datetime(2024, 1, 1),
                    datetime(2024, 8, 1)
                ),
                "organization": TEST_ORG_NAME,
                "integration_user_id": TEST_USER_ID
            }
            user_documents.append(user_data)
        
        await self.db["github_users"].delete_many({"integration_user_id": TEST_USER_ID})
        await self.db["github_users"].insert_many(user_documents)
        self.stats["users"] = len(user_documents)
        
        print(f" Created {len(user_documents)} organization members")

    async def create_issue_events(self, repositories: List[Dict[str, Any]]):
        
        print("\n Creating issue events (changelogs)...")
        
        event_types = ["closed", "reopened", "labeled", "unlabeled", "assigned", "unassigned", "referenced"]
        actors = ["alice-dev", "bob-coder", "charlie-eng", "diana-arch", "ethan-lead"]
        
        all_events = []
        
        for repo in repositories:
            events_per_repo = 50
            
            for i in range(events_per_repo):
                event_data = {
                    "id": 700001 + i + (repo["id"] * 100),
                    "event": random.choice(event_types),
                    "actor": {
                        "login": random.choice(actors),
                        "id": random.randint(300001, 300100),
                        "avatar_url": f"https://github.com/avatars/u/{random.randint(300001, 300100)}"
                    },
                    "created_at": self.generate_random_date(
                        datetime.fromisoformat(repo["created_at"].replace("Z", "")),
                        datetime.fromisoformat(repo["updated_at"].replace("Z", ""))
                    ),
                    "issue": {
                        "id": random.randint(500001, 500100),
                        "number": random.randint(1, 15),
                        "title": "Related issue for this event"
                    },
                    "commit_id": self.generate_sha() if random.choice([True, False]) else None,
                    "commit_url": f"https://github.com/{repo['full_name']}/commit/{self.generate_sha()}" if random.choice([True, False]) else None,
                    "repository": repo["full_name"],
                    "integration_user_id": TEST_USER_ID
                }
                all_events.append(event_data)
        
        # Clean existing and insert new
        await self.db["github_changelogs"].delete_many({"integration_user_id": TEST_USER_ID})
        await self.db["github_changelogs"].insert_many(all_events)
        self.stats["changelogs"] = len(all_events)
        
        print(f" Created {len(all_events)} issue events (changelogs)")

    async def generate_all_test_data(self):
        
        print(" GitHub Integration API - Test Data Generation")
        print("=" * 60)
        print(f"Organization: {TEST_ORG_NAME}")
        print(f"Target: 5 repositories, 2500+ commits each, 12+ PRs each, 15+ issues each")
        print("=" * 60)
        
        start_time = datetime.now()
        
        # Create base integration
        await self.create_test_integration()
        
        # Create organization
        await self.create_test_organization()
        
        # Create repositories
        repositories = await self.create_test_repositories()
        
        # Create members
        await self.create_organization_members()
        
        # Generate data for each repository
        print(f"\n Generating detailed data for {len(repositories)} repositories...")
        for i, repo in enumerate(repositories, 1):
            print(f"\n Processing repository {i}/{len(repositories)}: {repo['name']}")
            

            await self.create_commits_for_repo(repo, 2500)
            
            await self.create_pull_requests_for_repo(repo, 6)
            
            await self.create_issues_for_repo(repo, 6)
        
        # Create issue events
        await self.create_issue_events(repositories)
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        # Print final statistics
        print("\n" + "=" * 60)
        print(" TEST DATA GENERATION COMPLETE!")
        print("=" * 60)
        print(f"  Total Time: {duration.total_seconds():.2f} seconds")
        print(f" Organizations: {self.stats['organizations']}")
        print(f" Repositories: {self.stats['repositories']}")
        print(f" Commits: {self.stats['commits']:,}")
        print(f" Pull Requests: {self.stats['pulls']}")
        print(f" Issues: {self.stats['issues']}")
        print(f" Users: {self.stats['users']}")
        print(f" Changelogs: {self.stats['changelogs']}")
        print("=" * 60)

async def main():
    generator = GitHubTestDataGenerator()
    
    try:
        await generator.connect()
        await generator.generate_all_test_data()
        
    except Exception as e:
        print(f" Error generating test data: {e}")
    finally:
        await generator.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
