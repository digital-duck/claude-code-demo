# API Reference

## Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [Request/Response Format](#requestresponse-format)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [Pagination](#pagination)
8. [Examples](#examples)

## Overview

### Base URL
```
Development: http://localhost:3000/api/v1
Production:  https://api.example.com/api/v1
```

### API Versioning
The API uses URL versioning. The current version is `v1`.

### Content Type
All requests and responses use `application/json` unless otherwise specified.

### Standard Headers
```http
Content-Type: application/json
Authorization: Bearer <token>
X-Request-ID: <unique-request-id>
```

## Authentication

### Authentication Flow

#### 1. Register New User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePassword123!",
  "firstName": "John",
  "lastName": "Doe"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid-here",
      "email": "user@example.com",
      "username": "johndoe",
      "firstName": "John",
      "lastName": "Doe",
      "createdAt": "2024-11-21T10:30:00Z"
    },
    "tokens": {
      "accessToken": "eyJhbGciOiJIUzI1NiIs...",
      "refreshToken": "eyJhbGciOiJIUzI1NiIs...",
      "expiresIn": 900
    }
  }
}
```

#### 2. Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid-here",
      "email": "user@example.com",
      "username": "johndoe"
    },
    "tokens": {
      "accessToken": "eyJhbGciOiJIUzI1NiIs...",
      "refreshToken": "eyJhbGciOiJIUzI1NiIs...",
      "expiresIn": 900
    }
  }
}
```

#### 3. Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
  "refreshToken": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIs...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIs...",
    "expiresIn": 900
  }
}
```

#### 4. Logout
```http
POST /auth/logout
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "refreshToken": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

### Token Information
- **Access Token:** Valid for 15 minutes
- **Refresh Token:** Valid for 7 days
- **Token Type:** Bearer
- **Algorithm:** HS256 (HMAC with SHA-256)

## API Endpoints

### Users

#### Get Current User
```http
GET /users/me
Authorization: Bearer <access-token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "uuid-here",
    "email": "user@example.com",
    "username": "johndoe",
    "firstName": "John",
    "lastName": "Doe",
    "avatar": "https://cdn.example.com/avatars/uuid.jpg",
    "createdAt": "2024-11-21T10:30:00Z",
    "updatedAt": "2024-11-21T10:30:00Z"
  }
}
```

#### Update Current User
```http
PATCH /users/me
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "firstName": "Jane",
  "lastName": "Smith",
  "bio": "Software developer passionate about web technologies"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "uuid-here",
    "email": "user@example.com",
    "username": "johndoe",
    "firstName": "Jane",
    "lastName": "Smith",
    "bio": "Software developer passionate about web technologies",
    "updatedAt": "2024-11-21T11:45:00Z"
  }
}
```

#### Get User by ID
```http
GET /users/:userId
Authorization: Bearer <access-token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "uuid-here",
    "username": "johndoe",
    "firstName": "John",
    "lastName": "Doe",
    "bio": "Software developer",
    "avatar": "https://cdn.example.com/avatars/uuid.jpg",
    "createdAt": "2024-11-21T10:30:00Z"
  }
}
```

#### List Users
```http
GET /users?page=1&limit=20&search=john&sort=createdAt:desc
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 20, max: 100)
- `search` (optional): Search term for username/email
- `sort` (optional): Sort field and direction (e.g., `createdAt:desc`)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "users": [
      {
        "id": "uuid-1",
        "username": "johndoe",
        "firstName": "John",
        "lastName": "Doe",
        "avatar": "https://cdn.example.com/avatars/uuid-1.jpg"
      },
      {
        "id": "uuid-2",
        "username": "janedoe",
        "firstName": "Jane",
        "lastName": "Doe",
        "avatar": "https://cdn.example.com/avatars/uuid-2.jpg"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 150,
      "totalPages": 8,
      "hasNext": true,
      "hasPrev": false
    }
  }
}
```

#### Delete User
```http
DELETE /users/:userId
Authorization: Bearer <access-token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

### Posts

#### Create Post
```http
POST /posts
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "title": "My First Post",
  "content": "This is the content of my first post.",
  "tags": ["javascript", "web-development"],
  "published": true
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "uuid-here",
    "title": "My First Post",
    "content": "This is the content of my first post.",
    "slug": "my-first-post",
    "tags": ["javascript", "web-development"],
    "published": true,
    "author": {
      "id": "user-uuid",
      "username": "johndoe",
      "avatar": "https://cdn.example.com/avatars/uuid.jpg"
    },
    "createdAt": "2024-11-21T12:00:00Z",
    "updatedAt": "2024-11-21T12:00:00Z"
  }
}
```

#### Get Post by ID
```http
GET /posts/:postId
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "uuid-here",
    "title": "My First Post",
    "content": "This is the content of my first post.",
    "slug": "my-first-post",
    "tags": ["javascript", "web-development"],
    "published": true,
    "views": 125,
    "likes": 15,
    "author": {
      "id": "user-uuid",
      "username": "johndoe",
      "firstName": "John",
      "lastName": "Doe",
      "avatar": "https://cdn.example.com/avatars/uuid.jpg"
    },
    "createdAt": "2024-11-21T12:00:00Z",
    "updatedAt": "2024-11-21T12:00:00Z"
  }
}
```

#### List Posts
```http
GET /posts?page=1&limit=20&tag=javascript&author=johndoe&published=true
```

**Query Parameters:**
- `page` (optional): Page number
- `limit` (optional): Items per page
- `tag` (optional): Filter by tag
- `author` (optional): Filter by author username
- `published` (optional): Filter by published status
- `search` (optional): Search in title and content
- `sort` (optional): Sort field and direction

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "posts": [
      {
        "id": "uuid-1",
        "title": "My First Post",
        "excerpt": "This is the content of my first post...",
        "slug": "my-first-post",
        "tags": ["javascript"],
        "author": {
          "id": "user-uuid",
          "username": "johndoe",
          "avatar": "https://cdn.example.com/avatars/uuid.jpg"
        },
        "views": 125,
        "likes": 15,
        "createdAt": "2024-11-21T12:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 45,
      "totalPages": 3,
      "hasNext": true,
      "hasPrev": false
    }
  }
}
```

#### Update Post
```http
PATCH /posts/:postId
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "title": "Updated Post Title",
  "content": "Updated content",
  "tags": ["javascript", "typescript"],
  "published": true
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "uuid-here",
    "title": "Updated Post Title",
    "content": "Updated content",
    "tags": ["javascript", "typescript"],
    "published": true,
    "updatedAt": "2024-11-21T13:30:00Z"
  }
}
```

#### Delete Post
```http
DELETE /posts/:postId
Authorization: Bearer <access-token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Post deleted successfully"
}
```

### Comments

#### Create Comment
```http
POST /posts/:postId/comments
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "content": "Great post! Very informative.",
  "parentId": null
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "comment-uuid",
    "content": "Great post! Very informative.",
    "author": {
      "id": "user-uuid",
      "username": "johndoe",
      "avatar": "https://cdn.example.com/avatars/uuid.jpg"
    },
    "parentId": null,
    "likes": 0,
    "createdAt": "2024-11-21T14:00:00Z"
  }
}
```

#### Get Comments for Post
```http
GET /posts/:postId/comments?page=1&limit=20&sort=createdAt:desc
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "comments": [
      {
        "id": "comment-uuid-1",
        "content": "Great post!",
        "author": {
          "id": "user-uuid",
          "username": "johndoe",
          "avatar": "https://cdn.example.com/avatars/uuid.jpg"
        },
        "likes": 5,
        "replies": 2,
        "createdAt": "2024-11-21T14:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 25,
      "totalPages": 2,
      "hasNext": true,
      "hasPrev": false
    }
  }
}
```

### File Upload

#### Upload File
```http
POST /upload
Authorization: Bearer <access-token>
Content-Type: multipart/form-data

file: <binary-data>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "file-uuid",
    "filename": "image.jpg",
    "url": "https://cdn.example.com/uploads/file-uuid.jpg",
    "mimeType": "image/jpeg",
    "size": 245678,
    "uploadedAt": "2024-11-21T15:00:00Z"
  }
}
```

**Constraints:**
- Max file size: 10MB
- Allowed types: image/jpeg, image/png, image/gif, image/webp
- Filename must be alphanumeric with extension

## Request/Response Format

### Standard Success Response
```json
{
  "success": true,
  "data": {
    // Response data
  },
  "message": "Optional success message"
}
```

### Standard Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      // Additional error details
    }
  }
}
```

### Field Validation Errors
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "fields": {
        "email": ["Email is required", "Invalid email format"],
        "password": ["Password must be at least 8 characters"]
      }
    }
  }
}
```

## Error Handling

### HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | OK - Request succeeded |
| 201 | Created - Resource created successfully |
| 204 | No Content - Request succeeded, no content to return |
| 400 | Bad Request - Invalid request data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Resource conflict (e.g., duplicate) |
| 422 | Unprocessable Entity - Validation error |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |
| 503 | Service Unavailable - Service temporarily unavailable |

### Error Codes

| Error Code | Description |
|------------|-------------|
| VALIDATION_ERROR | Request validation failed |
| AUTHENTICATION_ERROR | Authentication failed |
| AUTHORIZATION_ERROR | Insufficient permissions |
| NOT_FOUND | Resource not found |
| DUPLICATE_RESOURCE | Resource already exists |
| RATE_LIMIT_EXCEEDED | Too many requests |
| INTERNAL_ERROR | Internal server error |
| SERVICE_UNAVAILABLE | Service temporarily unavailable |

### Example Error Response
```json
{
  "success": false,
  "error": {
    "code": "AUTHENTICATION_ERROR",
    "message": "Invalid credentials provided",
    "details": {
      "timestamp": "2024-11-21T16:00:00Z",
      "requestId": "req-uuid-here"
    }
  }
}
```

## Rate Limiting

### Limits
- **Anonymous:** 60 requests per hour
- **Authenticated:** 1000 requests per hour
- **Premium:** 5000 requests per hour

### Rate Limit Headers
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 995
X-RateLimit-Reset: 1700582400
```

### Rate Limit Exceeded Response
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please try again later.",
    "details": {
      "limit": 1000,
      "remaining": 0,
      "resetAt": "2024-11-21T17:00:00Z"
    }
  }
}
```

## Pagination

### Request Parameters
- `page`: Page number (starts at 1)
- `limit`: Items per page (default: 20, max: 100)

### Response Format
```json
{
  "success": true,
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 150,
      "totalPages": 8,
      "hasNext": true,
      "hasPrev": false
    }
  }
}
```

### Link Header (Optional)
```http
Link: <https://api.example.com/api/v1/posts?page=2>; rel="next",
      <https://api.example.com/api/v1/posts?page=8>; rel="last"
```

## Examples

### Complete Request Example with cURL

```bash
# Login
curl -X POST https://api.example.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }'

# Create post with authentication
curl -X POST https://api.example.com/api/v1/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -d '{
    "title": "My New Post",
    "content": "Post content here",
    "tags": ["javascript"],
    "published": true
  }'

# Get posts with filters
curl -X GET "https://api.example.com/api/v1/posts?page=1&limit=10&tag=javascript" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

### JavaScript/Fetch Example

```javascript
// Login
const loginResponse = await fetch('https://api.example.com/api/v1/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePassword123!'
  })
});

const { data } = await loginResponse.json();
const accessToken = data.tokens.accessToken;

// Create post
const postResponse = await fetch('https://api.example.com/api/v1/posts', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`
  },
  body: JSON.stringify({
    title: 'My New Post',
    content: 'Post content here',
    tags: ['javascript'],
    published: true
  })
});

const post = await postResponse.json();
```

---

*Last Updated: 2024-11-21*
*API Version: v1*
