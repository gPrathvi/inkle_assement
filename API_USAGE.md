# Inkle Backend API - Complete Usage Guide

## 🚀 Quick Start

1. **Start the server:**
```bash
cd Downloads/inkle
python manage.py runserver 0.0.0.0:8000
```

2. **Test all features:**
```bash
python demo_all_features.py
```

3. **Browse API docs:**
- Swagger UI: http://localhost:8000/api/docs/
- Health check: http://localhost:8000/health/

## 📝 All API Endpoints

### 1. Authentication

**Signup:**
```bash
curl -X POST http://localhost:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"secret123"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}'
```
Returns: `{"access": "TOKEN", "refresh": "REFRESH_TOKEN"}`

**Use the access token in all requests:**
```bash
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 2. User Profile

**Get my profile:**
```bash
curl http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Update my profile:**
```bash
curl -X PATCH http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"new@example.com"}'
```

**Search users:**
```bash
curl "http://localhost:8000/api/users/search/?q=alice" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Posts

**Create post:**
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Hello world! 👋"}'
```

**List all posts:**
```bash
curl http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Get specific post:**
```bash
curl http://localhost:8000/api/posts/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Update post (only if you're the author):**
```bash
curl -X PATCH http://localhost:8000/api/posts/1/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Updated content"}'
```

**Delete post (soft delete):**
```bash
curl -X DELETE http://localhost:8000/api/posts/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Likes

**Like a post:**
```bash
curl -X POST http://localhost:8000/api/posts/1/like/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Unlike a post:**
```bash
curl -X DELETE http://localhost:8000/api/posts/1/like/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 5. Comments

**Create comment:**
```bash
curl -X POST http://localhost:8000/api/comments/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"post":1,"content":"Nice post!"}'
```

**List comments for a post:**
```bash
curl "http://localhost:8000/api/comments/?post=1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 6. Social Features

**Follow a user:**
```bash
curl -X POST http://localhost:8000/api/users/2/follow/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Unfollow a user:**
```bash
curl -X DELETE http://localhost:8000/api/users/2/follow/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Block a user:**
```bash
curl -X POST http://localhost:8000/api/users/2/block/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Unblock a user:**
```bash
curl -X DELETE http://localhost:8000/api/users/2/block/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 7. Activity Feed

**Get activity feed:**
```bash
curl http://localhost:8000/api/feed/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Filter by activity type:**
```bash
# Only posts
curl "http://localhost:8000/api/feed/?type=posts" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Only likes  
curl "http://localhost:8000/api/feed/?type=likes" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Only follows
curl "http://localhost:8000/api/feed/?type=follows" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 8. Notifications

**Get my notifications:**
```bash
curl http://localhost:8000/api/notifications/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Mark all notifications as read:**
```bash
curl -X POST http://localhost:8000/api/notifications/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Mark single notification as read:**
```bash
curl -X POST http://localhost:8000/api/notifications/1/read/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 9. Admin Features (for admin/owner users only)

**List all users (admin only):**
```bash
curl http://localhost:8000/api/admin/users/ \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

**Deactivate user (admin only):**
```bash
curl -X DELETE http://localhost:8000/api/admin/users/2/ \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

**Reactivate user (admin only):**
```bash
curl -X POST http://localhost:8000/api/admin/users/2/reactivate/ \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

**Delete post as admin:**
```bash
curl -X DELETE http://localhost:8000/api/admin/posts/1/ \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

**Promote user to admin (owner only):**
```bash
curl -X POST http://localhost:8000/api/owner/admins/2/ \
  -H "Authorization: Bearer OWNER_TOKEN"
```

## 🎯 Assignment Requirements - All Implemented ✅

### ✅ User Management
- [x] User signup/login with JWT authentication
- [x] User profiles with update capability
- [x] User search functionality

### ✅ Posts & Content
- [x] Create posts
- [x] Like/unlike posts  
- [x] Comment on posts
- [x] Delete posts (soft delete)

### ✅ Social Features
- [x] Follow/unfollow users
- [x] Block/unblock users
- [x] Activity feed showing network activities

### ✅ Activity Wall
Shows all activities in the network:
- "ABC made a post"
- "DEF followed ABC"  
- "PQR liked ABC's post"
- User deleted by 'Owner'
- Post deleted by 'Admin'

### ✅ Admin Permissions
- **User role**: Can create posts, like, follow, comment
- **Admin role**: Can delete user profiles/posts + all user abilities
- **Owner role**: Can create/delete admins + all admin abilities

### ✅ Proper Permissions
- JWT authentication required for all endpoints
- Object-level permissions (only author can edit their posts)
- Role-based permissions for admin operations
- Blocked users cannot see each other's content

## 🔧 Configuration

The backend now has easier development settings:
- `DEBUG=True` by default for development
- CORS allows all origins in DEBUG mode
- Session authentication added for easier testing
- Default frontend origin support

## 📊 Data Flow Example

1. **Alice signs up and logs in** → Gets JWT token
2. **Alice creates a post** → Post stored, activity logged
3. **Bob likes Alice's post** → Like created, Alice gets notification
4. **Bob follows Alice** → Follow relationship created, Alice gets notification  
5. **Alice checks activity feed** → Sees Bob's like and follow activities
6. **Alice checks notifications** → Sees like and follow notifications from Bob

## 🔍 Troubleshooting

**401 Unauthorized:**
- Make sure you include `Authorization: Bearer <token>` header
- Check if your token is valid (tokens expire after 12 hours)

**403 Forbidden:**
- You're trying to access an admin/owner endpoint without proper role
- You're trying to modify someone else's content

**400 Bad Request:**
- Check your JSON payload format
- Missing required fields

**404 Not Found:**
- Check the endpoint URL
- Make sure the resource ID exists

## 🚀 Ready for Testing!

All Inkle assignment requirements are implemented and working. The backend provides:
- Complete REST API with proper permissions
- JWT authentication
- Social activity feed
- Admin/Owner role hierarchy
- Comprehensive documentation

Start the server and run `python demo_all_features.py` to see everything working!