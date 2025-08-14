from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class GitHubUser(BaseModel):
    id: int
    login: str
    name: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    html_url: Optional[str] = None
    type: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    public_repos: Optional[int] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class GitHubIntegration(BaseModel):
    user_id: int
    access_token: str
    user_info: GitHubUser
    integration_status: str = "active"
    connected_at: datetime = Field(default_factory=datetime.utcnow)
    last_sync: Optional[datetime] = None

class GitHubOrganization(BaseModel):
    id: int
    login: str
    name: Optional[str] = None
    description: Optional[str] = None
    html_url: Optional[str] = None
    avatar_url: Optional[str] = None
    location: Optional[str] = None
    email: Optional[str] = None
    public_repos: Optional[int] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    type: Optional[str] = None

class GitHubRepository(BaseModel):
    id: int
    name: str
    full_name: str
    owner: Dict[str, Any]
    private: bool
    html_url: str
    description: Optional[str] = None
    fork: bool
    created_at: str
    updated_at: str
    pushed_at: Optional[str] = None
    size: int
    stargazers_count: int
    watchers_count: int
    primary_language: Optional[str] = None # language was conflicting with MongoDB, So Mapped to primary_language
    forks_count: int
    open_issues_count: int
    default_branch: str
    archived: bool
    disabled: bool
    topics: List[str] = []

class GitHubCommit(BaseModel):
    sha: str
    commit: Dict[str, Any]
    author: Optional[Dict[str, Any]] = None
    committer: Optional[Dict[str, Any]] = None
    parents: List[Dict[str, Any]] = []
    html_url: str
    repository: str

class GitHubPullRequest(BaseModel):
    id: int
    number: int
    state: str
    title: str
    user: Dict[str, Any]
    body: Optional[str] = None
    created_at: str
    updated_at: str
    closed_at: Optional[str] = None
    merged_at: Optional[str] = None
    merge_commit_sha: Optional[str] = None
    head: Dict[str, Any]
    base: Dict[str, Any]
    html_url: str
    repository: str

class GitHubIssue(BaseModel):
    id: int
    number: int
    title: str
    user: Dict[str, Any]
    labels: List[Dict[str, Any]] = []
    state: str
    assignee: Optional[Dict[str, Any]] = None
    assignees: List[Dict[str, Any]] = []
    milestone: Optional[Dict[str, Any]] = None
    comments: int
    created_at: str
    updated_at: str
    closed_at: Optional[str] = None
    body: Optional[str] = None
    html_url: str
    repository: str

class GitHubChangelog(BaseModel):
    id: int
    event: str
    actor: Dict[str, Any]
    created_at: str
    issue: Optional[Dict[str, Any]] = None
    commit_id: Optional[str] = None
    commit_url: Optional[str] = None
    repository: str
