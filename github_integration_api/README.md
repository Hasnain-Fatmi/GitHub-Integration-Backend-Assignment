# GitHub Integration Backend API

A comprehensive FastAPI backend application that provides secure GitHub OAuth integration with full data synchronization capabilities. This API enables applications to authenticate with GitHub, fetch organizational data, and maintain synchronized repositories, commits, pull requests, issues, and user information through a modern REST API.

## Project Description

The GitHub Integration Backend API serves as a middleware solution that bridges applications with GitHub's data ecosystem. It implements OAuth2 authentication flows, comprehensive data fetching from GitHub's REST API, and provides a unified interface for querying synchronized GitHub data.

This API is built with modern Python technologies and follows best practices for scalability, security, and performance. It's designed to handle high-volume data operations while maintaining data consistency and providing real-time access to GitHub information.

**Core Capabilities:**
- **Complete GitHub OAuth2 Integration**: Secure authentication flow with GitHub using industry-standard OAuth2 protocols
- **Comprehensive Data Synchronization**: Automated fetching and storage of organizations, repositories, commits, pull requests, issues, users, and event logs
- **Advanced Query API**: Dynamic querying with pagination, filtering, sorting, and full-text search across all data collections
- **Global Search**: Cross-collection search functionality for comprehensive data discovery
- **Integration Management**: Complete lifecycle management including status monitoring, data removal, and resynchronization
- **High-Performance Architecture**: Fully asynchronous operations using FastAPI, Motor, and HTTPX

**Technology Stack:**
- **Backend Framework**: FastAPI 0.104.1 with async/await support
- **Database**: MongoDB with Motor async driver for optimal performance
- **HTTP Client**: HTTPX for GitHub API integration
- **Authentication**: GitHub OAuth2 with secure token management
- **Data Validation**: Pydantic for robust data modeling

## Setup Instructions

### Prerequisites

- **Python 3.11** - Required for modern async/await features
- **MongoDB** - Local installation or MongoDB Atlas cloud service
- **GitHub OAuth Application** - Required for authentication integration
- **Git** - For repository cloning and version control

### Installation Steps

1. **Clone Repository and Environment Setup**
   ```bash
   git clone https://github.com/Hasnain-Fatmi/GitHub-Integration-Backend-Assignment
   cd "github_integration_api"
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   .\venv\Scripts\Activate.ps1    # Windows PowerShell
   .\venv\Scripts\activate.bat    # Windows Command Prompt
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Database Configuration**
   
   **Option A: Local MongoDB**
   ```bash
   # Install MongoDB Community Server
   # Download from: https://www.mongodb.com/try/download/community
   # Start MongoDB service (usually runs on port 27017)
   ```
   
   **Option B: MongoDB Atlas (Cloud)**
   ```bash
   # Create free cluster
   # Get connection string and update MONGODB_URL in .env
   ```

3. **GitHub OAuth Application Setup**
   
   Navigate to GitHub Settings → Developer settings → OAuth Apps:
   ```
   Application name: GitHub Integration API
   Homepage URL: http://localhost:8000
   Authorization callback URL: http://localhost:8000/auth/github/callback
   ```
   
   After creation, note your **Client ID** and **Client Secret**.

4. **Environment Configuration**
   
   The `.env` file contains your configuration. Update with your specific values:
   ```env
   # MongoDB Configuration
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=github_integration
   
   # GitHub OAuth Configuration
   GITHUB_CLIENT_ID=your_github_client_id_here
   GITHUB_CLIENT_SECRET=your_github_client_secret_here
   GITHUB_REDIRECT_URI=http://localhost:8000/auth/github/callback
   
   # Security Configuration
   SECRET_KEY=your-super-secret-key-for-jwt-signing-make-this-random-and-long
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Launch Application**
   ```bash
   # Development mode with auto-reload
   python main.py
   
   # Production mode (alternative)
   uvicorn src.server:app --host 0.0.0.0 --port 8000
   ```

### Access Points

- **API Base URL**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc

### Verification

Test your installation with the provided utilities (Navigate to Testing_Scripts in seperate terminal while Server is running):
```bash
cd Testing_Scripts
python test_oauth_flow.py        # Interactive OAuth flow testing
python generate_test_data.py     # Generate sample data for testing
python test_api_data.py          # API endpoint validation
python inspect_api_data.py       # Detailed data inspection
```
   
## API Usage Guide

### Base URL
```
http://localhost:8000
```

### Authentication Endpoints

#### GitHub OAuth Login
**Endpoint:** `GET /auth/github/login`

**Description:** Initiates the GitHub OAuth authorization flow by redirecting to GitHub's authorization server.

**Parameters:** None

**Response:** HTTP 302/307 redirect to GitHub authorization URL

**Example:**
```bash
curl -L "http://localhost:8000/auth/github/login"
```

**Response Headers:**
```
Location: https://github.com/login/oauth/authorize?client_id=...&redirect_uri=...&scope=...
```

#### GitHub OAuth Callback
**Endpoint:** `GET /auth/github/callback`

**Description:** Handles the OAuth callback from GitHub after user authorization. This endpoint processes the authorization code and establishes the integration.

**Parameters:**
- `code` (query, required): Authorization code from GitHub
- `state` (query, optional): State parameter for CSRF protection

**Response:** JSON with integration status or redirect to success page

### Integration Management Endpoints

#### Check Integration Status
**Endpoint:** `GET /integration/status`

**Description:** Retrieves the current integration status for a user, including connected GitHub account information and sync timestamps.

**Parameters:**
- `user_id` (query, required): The user ID to check integration status for

**Response:**
```json
{
  "status": "connected",
  "user": {
    "id": 12345,
    "login": "username",
    "name": "User Name",
    "email": "user@example.com",
    "avatar_url": "https://github.com/avatars/u/12345",
    "html_url": "https://github.com/username",
    "company": "Company Name",
    "public_repos": 25,
    "followers": 100,
    "following": 50
  },
  "connected_at": "2024-01-01T00:00:00Z",
  "last_sync": "2024-01-01T12:00:00Z"
}
```

**Example:**
```bash
curl "http://localhost:8000/integration/status?user_id=12345"
```

#### Resync Integration Data
**Endpoint:** `POST /integration/resync`

**Description:** Re-fetches and synchronizes all GitHub data for the specified user. This operation may take several minutes for large organizations.

**Request Body:**
```json
{
  "user_id": 12345
}
```

**Response:**
```json
{
  "message": "Resync completed successfully",
  "stats": {
    "organizations": 2,
    "repositories": 15,
    "commits": 450,
    "pulls": 25,
    "issues": 30,
    "users": 20,
    "changelogs": 75
  },
  "sync_time": "2024-01-01T12:30:00Z"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/integration/resync" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 12345}'
```

#### Remove Integration
**Endpoint:** `POST /integration/remove`

**Description:** Removes all integration data for a specified user from the database. This action is irreversible.

**Request Body:**
```json
{
  "user_id": 12345
}
```

**Response:**
```json
{
  "message": "Integration removed successfully",
  "removed_collections": ["github_integration", "github_repos", "github_commits"],
  "total_removed": 1500
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/integration/remove" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 12345}'
```

### Data Access Endpoints

#### Dynamic Collection Querying
**Endpoint:** `GET /data/{collection}`

**Description:** Retrieves data from any GitHub collection with advanced filtering, pagination, sorting, and search capabilities. This is the primary endpoint for accessing synchronized GitHub data.

**Available Collections:**
- `github_organizations` - GitHub organizations and their metadata
- `github_repos` - Repository information, statistics, and settings
- `github_commits` - Commit history with author and file change details
- `github_pulls` - Pull requests with review status and merge information
- `github_issues` - Issues with labels, assignees, and state tracking
- `github_changelogs` - Issue events and state change history
- `github_users` - Users and organization members with profile data

**Query Parameters:**
- `page` (integer, optional): Page number, starting from 1 (default: 1)
- `limit` (integer, optional): Items per page, maximum 100 (default: 20)
- `sort_by` (string, optional): Field name to sort results by
- `sort_order` (string, optional): Sort direction - `asc` or `desc` (default: asc)
- `search` (string, optional): Keyword search across relevant text fields
- `filter` (string, optional): JSON object containing MongoDB filter criteria

**Response Structure:**
```json
{
  "data": [...],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 200,
    "items_per_page": 20,
    "has_next": true,
    "has_previous": false
  },
  "meta": {
    "collection": "github_repos",
    "filters_applied": true,
    "search_applied": false,
    "sort_by": "created_at",
    "sort_order": "desc"
  }
}
```

**Usage Examples:**

**Basic Repository Query:**
```bash
curl "http://localhost:8000/data/github_repos"
```

**Paginated and Sorted Query:**
```bash
curl "http://localhost:8000/data/github_repos?page=2&limit=10&sort_by=stargazers_count&sort_order=desc"
```

**Search Query:**
```bash
curl "http://localhost:8000/data/github_repos?search=python"
```

**Filtered Query (Repositories with Python language and more than 100 stars):**
```bash
curl "http://localhost:8000/data/github_repos?filter={\"language\":\"Python\",\"stargazers_count\":{\"\$gt\":100}}"
```

**Complex Query Example:**
```bash
curl "http://localhost:8000/data/github_commits?page=1&limit=5&sort_by=commit.author.date&sort_order=desc&filter={\"commit.author.name\":\"John Doe\"}&search=fix"
```

#### Global Search
**Endpoint:** `GET /search`

**Description:** Performs a global search across all GitHub data collections for the specified keyword. This provides a unified search experience across repositories, commits, pull requests, and issues.

**Parameters:**
- `q` (query, required): Search keyword or phrase

**Response:**
```json
{
  "keyword": "fastapi",
  "total_results": 15,
  "collections_searched": ["github_repos", "github_commits", "github_pulls", "github_issues"],
  "results": {
    "github_repos": [
      {
        "name": "fastapi-project",
        "description": "A FastAPI web application",
        "language": "Python",
        "stargazers_count": 125
      }
    ],
    "github_commits": [
      {
        "sha": "abc123",
        "commit": {
          "message": "Add FastAPI endpoints for user management"
        }
      }
    ]
  }
}
```

**Example:**
```bash
curl "http://localhost:8000/search?q=fastapi"
```

## Data Models and Schema

The application uses comprehensive Pydantic models that automatically map GitHub API responses to structured MongoDB documents. All GitHub entity relationships and metadata are preserved during synchronization.

### Core Data Models

**GitHubIntegration**
- User authentication tokens and OAuth metadata
- Integration status and connection timestamps  
- User profile information from GitHub

**GitHubOrganization** 
- Organization profile and metadata
- Member count and repository statistics
- Billing and plan information

**GitHubRepository**
- Complete repository information including statistics
- Language breakdown and topic tags
- Collaboration and permission settings

**GitHubCommit**
- Full commit history with author and committer details
- File change statistics and verification status
- Parent commit relationships

**GitHubPullRequest**
- Pull request metadata and review status
- Merge information and conflict resolution
- Associated issues and linked discussions

**GitHubIssue**
- Issue tracking with labels and assignees
- State management and milestone tracking
- Comment threads and reaction data

**GitHubUser**
- User and organization member profiles
- Contribution statistics and activity data
- Social connections and collaboration metrics

**GitHubChangelog**
- Issue and pull request event tracking
- State change history and audit trails
- User action attribution and timestamps

## Testing and Development

### Testing Utilities

The project includes comprehensive testing utilities for development and validation:

**OAuth Flow Testing**
```bash
python test_oauth_flow.py
```
Interactive testing utility that guides through the complete OAuth authorization flow with browser integration.

**API Data Testing**
```bash
python test_api_data.py
```
Validates all API endpoints with sample data and provides detailed response analysis.

**Test Data Generation**
```bash
python generate_test_data.py
```
Generates realistic test data for development and testing purposes with configurable volumes.

**Data Inspection**
```bash
python inspect_api_data.py
```
Detailed data structure inspection utility for understanding stored GitHub data and response formats.

### Development Workflow

1. **Setup Development Environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows
   pip install -r requirements.txt
   ```

2. **Generate Test Data**
   ```bash
   python generate_test_data.py
   ```

3. **Run Application**
   ```bash
   python main.py
   ```

4. **Test API Endpoints**
   ```bash
   python test_api_data.py
   ```

5. **Test OAuth Flow** (requires GitHub OAuth app)
   ```bash
   python test_oauth_flow.py
   ```

## Performance and Best Practices

### API Performance Features
- **Asynchronous Operations**: All database and HTTP operations use async/await for optimal performance
- **Pagination**: Built-in pagination prevents memory issues with large datasets
- **Database Optimization**: MongoDB queries are optimized with proper indexing

### Data Synchronization
- Data is synchronized during the initial OAuth flow
- Manual resync can be triggered using the `/integration/resync` endpoint
- Large organizations may require several minutes for complete synchronization
- Incremental updates are recommended for production usage

