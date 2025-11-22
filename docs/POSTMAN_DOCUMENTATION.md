# Inkle API - Complete Postman Documentation

## Overview
This document provides comprehensive documentation for testing all features of the Inkle Backend API using Postman.

## Files Required
- **Collection**: `docs/postman/inkle_api.postman_collection.json`
- **Environment**: `docs/postman/inkle_local.postman_environment.json`

## Setup Steps
1. Import both files into Postman
2. Select "Inkle Local" environment (top-right dropdown)
3. Ensure `base_url` is set to `http://localhost:8000`
4. Start your Django server: `python manage.py runserver 0.0.0.0:8000`

## Authentication Flow
The collection automatically handles JWT tokens. After Login, the `access_token` is saved to your environment.

---

## 1. Authentication & User Management

### 1.1 User Signup
- **Endpoint**: `POST /api/auth/signup/`
- **Purpose**: Create a new user account
- **Body**:
```json
{
  "username": "alice",
  "email": "alice@example.com", 
  "password": "secret123"
}
```
- **Expected Response**: `201 Created`
- **Note**: Returns `400` if username/email already exists (expected on re-runs)

### 1.2 User Login (JWT)
- **Endpoint**: `POST /api/auth/login/`
- **Purpose**: Authenticate and get JWT tokens
- **Body**:
```json
{
  "username": "alice",
  "password": "secret123"
}
```
- **Expected Response**: `200 OK` with access/refresh tokens
- **Auto-Feature**: Token automatically saved to environment as `access_token`

### 1.3 Refresh Token
- **Endpoint**: `POST /api/auth/refresh/`
- **Purpose**: Get new access token using refresh token
- **Body**:
```json
{
  "refresh": "{{refresh_token}}"
}
```
- **Expected Response**: `200 OK` with new access token

### 1.4 Get Current User (Me)
- **Endpoint**: `GET /api/users/me/`
- **Purpose**: Get current user profile
- **Auth**: Requires Bearer token
- **Expected Response**: `200 OK` with user data

### 1.5 Update Current User (Me)
- **Endpoint**: `PATCH /api/users/me/`
- **Purpose**: Update current user profile
- **Auth**: Requires Bearer token
- **Body**:
```json
{
  "email": "newemail@example.com",
  "bio": "Updated bio"
}
```
- **Expected Response**: `200 OK` with updated user data

### 1.6 Search Users
- **Endpoint**: `GET /api/users/search/?q=alice`
- **Purpose**: Search for users by username/email
- **Auth**: Requires Bearer token
- **Query Params**: `q` (search term)
- **Expected Response**: `200 OK` with list of matching users

---

## 2. Posts Management

### 2.1 Create Post
- **Endpoint**: `POST /api/posts/`
- **Purpose**: Create a new post
- **Auth**: Requires Bearer token
- **Body**:
```json
{
  "content": "This is my first post!",
  "visibility": "public"
}
```
- **Expected Response**: `201 Created` with post data including `id`
- **Note**: Save the post `id` for subsequent operations

### 2.2 List Posts
- **Endpoint**: `GET /api/posts/`
- **Purpose**: Get list of all posts
- **Auth**: Requires Bearer token
- **Expected Response**: `200 OK` with paginated post list

### 2.3 Get Single Post
- **Endpoint**: `GET /api/posts/{id}/`
- **Purpose**: Get details of a specific post
- **Auth**: Requires Bearer token
- **URL**: Replace `{id}` with actual post ID
- **Expected Response**: `200 OK` with post details

### 2.4 Update Post
- **Endpoint**: `PATCH /api/posts/{id}/`
- **Purpose**: Update an existing post
- **Auth**: Requires Bearer token (must be post author)
- **Body**:
```json
{
  "content": "Updated post content"
}
```
- **Expected Response**: `200 OK` with updated post

### 2.5 Delete Post
- **Endpoint**: `DELETE /api/posts/{id}/`
- **Purpose**: Soft delete a post
- **Auth**: Requires Bearer token (must be post author)
- **Expected Response**: `204 No Content`

### 2.6 Like Post
- **Endpoint**: `POST /api/posts/{id}/like/`
- **Purpose**: Like a post
- **Auth**: Requires Bearer token
- **Expected Response**: `201 Created` (first like) or `200 OK` (already liked)

### 2.7 Unlike Post
- **Endpoint**: `DELETE /api/posts/{id}/like/`
- **Purpose**: Remove like from a post
- **Auth**: Requires Bearer token
- **Expected Response**: `204 No Content`

---

## 3. Comments Management

### 3.1 Create Comment
- **Endpoint**: `POST /api/comments/`
- **Purpose**: Add comment to a post
- **Auth**: Requires Bearer token
- **Body**:
```json
{
  "post": 1,
  "content": "Great post!"
}
```
- **Expected Response**: `201 Created` with comment data
- **Note**: Use actual post ID

### 3.2 List Comments (by Post)
- **Endpoint**: `GET /api/comments/?post={post_id}`
- **Purpose**: Get all comments for a specific post
- **Auth**: Requires Bearer token
- **Query Params**: `post` (post ID)
- **Expected Response**: `200 OK` with comments list

### 3.3 Update Comment
- **Endpoint**: `PATCH /api/comments/{id}/`
- **Purpose**: Update an existing comment
- **Auth**: Requires Bearer token (must be comment author)
- **Body**:
```json
{
  "content": "Updated comment content"
}
```
- **Expected Response**: `200 OK` with updated comment

### 3.4 Delete Comment
- **Endpoint**: `DELETE /api/comments/{id}/`
- **Purpose**: Delete a comment
- **Auth**: Requires Bearer token (must be comment author)
- **Expected Response**: `204 No Content`

---

## 4. Social Features

### 4.1 Follow User
- **Endpoint**: `POST /api/users/{id}/follow/`
- **Purpose**: Follow another user
- **Auth**: Requires Bearer token
- **URL**: Replace `{id}` with target user ID
- **Expected Response**: `201 Created` (new follow) or `200 OK` (already following)

### 4.2 Unfollow User
- **Endpoint**: `DELETE /api/users/{id}/follow/`
- **Purpose**: Unfollow a user
- **Auth**: Requires Bearer token
- **Expected Response**: `204 No Content`

### 4.3 Block User
- **Endpoint**: `POST /api/users/{id}/block/`
- **Purpose**: Block another user
- **Auth**: Requires Bearer token
- **Expected Response**: `201 Created` (new block) or `200 OK` (already blocked)

### 4.4 Unblock User
- **Endpoint**: `DELETE /api/users/{id}/block/`
- **Purpose**: Unblock a user
- **Auth**: Requires Bearer token
- **Expected Response**: `204 No Content`

---

## 5. Activity & Notifications

### 5.1 Get Feed (All Activities)
- **Endpoint**: `GET /api/feed/`
- **Purpose**: Get activity feed (posts from followed users + own posts)
- **Auth**: Requires Bearer token
- **Expected Response**: `200 OK` with activity feed

### 5.2 Get Personal Feed
- **Endpoint**: `GET /api/feed/?type=personal`
- **Purpose**: Get personal activity feed
- **Auth**: Requires Bearer token
- **Query Params**: `type=personal`
- **Expected Response**: `200 OK` with personal feed

### 5.3 List Notifications
- **Endpoint**: `GET /api/notifications/`
- **Purpose**: Get all notifications for current user
- **Auth**: Requires Bearer token
- **Expected Response**: `200 OK` with notifications list

### 5.4 Mark Single Notification as Read
- **Endpoint**: `PATCH /api/notifications/{id}/read/`
- **Purpose**: Mark a specific notification as read
- **Auth**: Requires Bearer token
- **URL**: Replace `{id}` with notification ID
- **Expected Response**: `200 OK`

### 5.5 Mark All Notifications as Read
- **Endpoint**: `POST /api/notifications/mark-all-read/`
- **Purpose**: Mark all notifications as read
- **Auth**: Requires Bearer token
- **Expected Response**: `204 No Content`

---

## 6. Health & Documentation

### 6.1 Health Check
- **Endpoint**: `GET /health/`
- **Purpose**: Check API health status
- **Auth**: None required
- **Expected Response**: `200 OK` with `{"status":"ok"}`

### 6.2 OpenAPI Schema
- **Endpoint**: `GET /api/schema/`
- **Purpose**: Get OpenAPI schema
- **Auth**: None required
- **Expected Response**: `200 OK` with schema JSON

### 6.3 Swagger UI
- **Endpoint**: `GET /api/docs/`
- **Purpose**: Interactive API documentation
- **Auth**: None required (but endpoints require auth)
- **Response**: HTML Swagger UI

---

## Testing Workflow

### Complete End-to-End Test:

1. **Setup Users**:
   - Create User A (alice): `POST /api/auth/signup/`
   - Login as User A: `POST /api/auth/login/`
   - Create User B (bob): Change username/email in signup
   - Search for User B: `GET /api/users/search/?q=bob`

2. **Content Creation**:
   - Create posts as User A: `POST /api/posts/`
   - Add comments to posts: `POST /api/comments/`
   - Like posts: `POST /api/posts/{id}/like/`

3. **Social Interactions**:
   - Follow User B: `POST /api/users/{bob_id}/follow/`
   - Check feed: `GET /api/feed/`
   - Check notifications: `GET /api/notifications/`

4. **Content Management**:
   - Edit posts/comments: `PATCH /api/posts/{id}/` or `PATCH /api/comments/{id}/`
   - Unlike posts: `DELETE /api/posts/{id}/like/`
   - Delete content: `DELETE /api/posts/{id}/` or `DELETE /api/comments/{id}/`

5. **Cleanup**:
   - Unfollow users: `DELETE /api/users/{id}/follow/`
   - Mark notifications read: `POST /api/notifications/mark-all-read/`

## Troubleshooting

### Common Issues:
- **401 Unauthorized**: Run Login again to refresh token
- **400 Username exists**: Expected on signup re-runs, proceed with login
- **404 Not Found**: Check if IDs in URLs are real (create content first)
- **403 Forbidden**: Check if you own the content you're trying to modify

### ID Management:
- Sample IDs (10, 20, 2) in collection are placeholders
- Replace with real IDs from your test session
- Create content first, then use returned IDs for subsequent operations

---

## Environment Variables Used
- `{{base_url}}` - API base URL (default: http://localhost:8000)
- `{{access_token}}` - JWT access token (auto-set after login)
- `{{refresh_token}}` - JWT refresh token (manual set if needed)

This documentation covers all major features of the Inkle API. Each endpoint has been tested and verified to work correctly when proper authentication and data are provided.