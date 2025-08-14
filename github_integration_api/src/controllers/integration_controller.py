from fastapi import HTTPException
from ..helpers.database import find_one, delete_many, insert_many, update_one
from ..helpers.github_api import GitHubAPI
from ..models.github_models import *
from datetime import datetime
from typing import Dict, Any

class IntegrationController:
    
    @staticmethod
    async def get_integration_status(user_id: int):
        integration = await find_one("github_integration", {"user_id": user_id})
        if not integration:
            return {"status": "not_connected", "message": "No GitHub integration found"}
        
        return {
            "status": integration.get("integration_status", "unknown"),
            "user": integration.get("user_info"),
            "connected_at": integration.get("connected_at"),
            "last_sync": integration.get("last_sync")
        }

    @staticmethod
    async def remove_integration(user_id: int):
        integration = await find_one("github_integration", {"user_id": user_id})
        if not integration:
            raise HTTPException(status_code=404, detail="Integration not found")
        
        # Delete all GitHub data for this user
        collections_to_clean = [
            "github_integration",
            "github_organizations", 
            "github_repos",
            "github_commits",
            "github_pulls",
            "github_issues",
            "github_changelogs",
            "github_users"
        ]
        
        for collection in collections_to_clean:
            if collection == "github_integration":
                await delete_many(collection, {"user_id": user_id})
            else:
                await delete_many(collection, {"integration_user_id": user_id})
        
        return {"message": "Integration and all associated data removed successfully"}

    @staticmethod
    async def resync_data(user_id: int):
        integration = await find_one("github_integration", {"user_id": user_id})
        if not integration:
            raise HTTPException(status_code=404, detail="Integration not found")
        
        access_token = integration.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="No access token found")
        
        github_api = GitHubAPI(access_token)
        
        # Clear existing data
        collections_to_clean = [
            "github_organizations", 
            "github_repos",
            "github_commits",
            "github_pulls",
            "github_issues",
            "github_changelogs",
            "github_users"
        ]
        
        for collection in collections_to_clean:
            await delete_many(collection, {"integration_user_id": user_id})
        
        sync_stats = {
            "organizations": 0,
            "repositories": 0,
            "commits": 0,
            "pulls": 0,
            "issues": 0,
            "changelogs": 0,
            "users": 0
        }
        
        try:
            # Fetch and store organizations
            print(f"DEBUG - Starting to fetch organizations for user {user_id}")
            orgs = await github_api.get_user_organizations()
            print(f"DEBUG - Organizations fetched: {orgs}")
            if not orgs:
                orgs = []
                print(f"DEBUG - No organizations found, initialized empty list")
                
            if orgs:
                print(f"DEBUG - Processing {len(orgs)} organizations")
                org_documents = []
                for org in orgs:
                    org_doc = org.copy()
                    org_doc["integration_user_id"] = user_id
                    org_documents.append(org_doc)
                
                if org_documents:
                    await insert_many("github_organizations", org_documents)
                    sync_stats["organizations"] = len(org_documents)
                    print(f"DEBUG - Inserted {len(org_documents)} organizations into database")
                
                # Fetch organization members
                user_documents = []
                for org in orgs:
                    members = await github_api.get_organization_members(org["login"])
                    for member in members:
                        member_doc = member.copy()
                        member_doc["integration_user_id"] = user_id
                        member_doc["organization"] = org["login"]
                        user_documents.append(member_doc)
                
                if user_documents:
                    await insert_many("github_users", user_documents)
                    sync_stats["users"] = len(user_documents)
            
            # Fetch user repositories
            user_repos = await github_api.get_user_repos()
            if not user_repos:
                user_repos = [] 
            all_repos = user_repos.copy()
            
            # Fetch organization repositories
            for org in orgs:
                org_repos = await github_api.get_organization_repos(org["login"])
                if org_repos:
                    all_repos.extend(org_repos)
            
            if all_repos:
                repo_documents = []
                for repo in all_repos:
                    repo_doc = repo.copy()
                    repo_doc["integration_user_id"] = user_id
                    # Rename 'language' to 'primary_language' to avoid MongoDB conflicts
                    if "language" in repo_doc:
                        repo_doc["primary_language"] = repo_doc.pop("language")
                    repo_documents.append(repo_doc)
                
                await insert_many("github_repos", repo_documents)
                sync_stats["repositories"] = len(repo_documents)
                
                # Fetch data for each repository
                for repo in all_repos:
                    owner = repo["owner"]["login"]
                    repo_name = repo["name"]
                    
                    # Fetch ALL commits with pagination
                    all_commits = []
                    page = 1
                    while True:
                        commits = await github_api.get_repository_commits(owner, repo_name, page=page, per_page=100)
                        if not commits:
                            break
                        all_commits.extend(commits)
                        if len(commits) < 100:  # Last page
                            break
                        page += 1
                    
                    if all_commits:
                        commit_documents = []
                        for commit in all_commits:
                            commit_doc = commit.copy()
                            commit_doc["integration_user_id"] = user_id
                            commit_doc["repository"] = repo["full_name"]
                            commit_documents.append(commit_doc)
                        
                        await insert_many("github_commits", commit_documents)
                        sync_stats["commits"] += len(commit_documents)
                    
                    # Fetch ALL pull requests with pagination
                    all_pulls = []
                    page = 1
                    while True:
                        pulls = await github_api.get_repository_pulls(owner, repo_name, page=page, per_page=100)
                        if not pulls:
                            break
                        all_pulls.extend(pulls)
                        if len(pulls) < 100:  # Last page
                            break
                        page += 1
                    
                    if all_pulls:
                        pull_documents = []
                        for pull in all_pulls:
                            pull_doc = pull.copy()
                            pull_doc["integration_user_id"] = user_id
                            pull_doc["repository"] = repo["full_name"]
                            pull_documents.append(pull_doc)
                        
                        await insert_many("github_pulls", pull_documents)
                        sync_stats["pulls"] += len(pull_documents)
                    
                    # Fetch ALL issues with pagination
                    all_issues = []
                    page = 1
                    while True:
                        issues = await github_api.get_repository_issues(owner, repo_name, page=page, per_page=100)
                        if not issues:
                            break
                        all_issues.extend(issues)
                        if len(issues) < 100:  # Last page
                            break
                        page += 1
                    
                    if all_issues:
                        issue_documents = []
                        for issue in all_issues:
                            if "pull_request" not in issue:
                                issue_doc = issue.copy()
                                issue_doc["integration_user_id"] = user_id
                                issue_doc["repository"] = repo["full_name"]
                                issue_documents.append(issue_doc)
                        
                        if issue_documents:
                            await insert_many("github_issues", issue_documents)
                            sync_stats["issues"] += len(issue_documents)
                    
                    # Fetch ALL events with pagination
                    all_events = []
                    page = 1
                    while True:
                        events = await github_api.get_repository_issue_events(owner, repo_name, page=page, per_page=100)
                        if not events:
                            break
                        all_events.extend(events)
                        if len(events) < 100:  # Last page
                            break
                        page += 1
                    
                    if all_events:
                        event_documents = []
                        for event in all_events:
                            event_doc = event.copy()
                            event_doc["integration_user_id"] = user_id
                            event_doc["repository"] = repo["full_name"]
                            event_documents.append(event_doc)
                        
                        await insert_many("github_changelogs", event_documents)
                        sync_stats["changelogs"] += len(event_documents)
            
            await update_one(
                "github_integration",
                {"user_id": user_id},
                {"last_sync": datetime.utcnow()}
            )
            
            return {
                "message": "Data resync completed successfully",
                "stats": sync_stats
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error during resync: {str(e)}")
