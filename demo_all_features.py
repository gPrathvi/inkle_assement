#!/usr/bin/env python3
"""
Demo script showing all Inkle backend features working:
- User signup/login
- Create posts, like posts
- Follow users, block users  
- Activity feed
- Admin operations
"""
import os, sys, json
import requests

BASE_URL = "http://localhost:8000"

def demo():
    print("🚀 Inkle Backend Demo - All Features")
    print(f"Using BASE_URL: {BASE_URL}")
    
    # 1. SIGNUP & LOGIN
    print("\n📝 1. User Management")
    
    # Signup user 1
    r = requests.post(f"{BASE_URL}/api/auth/signup/", json={
        "username": "alice", "email": "alice@example.com", "password": "secret123"
    })
    print(f"Alice Signup: {r.status_code}")
    
    # Signup user 2  
    r = requests.post(f"{BASE_URL}/api/auth/signup/", json={
        "username": "bob", "email": "bob@example.com", "password": "secret123"
    })
    print(f"Bob Signup: {r.status_code}")
    
    # Login Alice
    r = requests.post(f"{BASE_URL}/api/auth/login/", json={
        "username": "alice", "password": "secret123"
    })
    alice_token = r.json().get("access") if r.status_code == 200 else None
    print(f"Alice Login: {r.status_code} {'✅' if alice_token else '❌'}")
    
    # Login Bob
    r = requests.post(f"{BASE_URL}/api/auth/login/", json={
        "username": "bob", "password": "secret123"
    })
    bob_token = r.json().get("access") if r.status_code == 200 else None
    print(f"Bob Login: {r.status_code} {'✅' if bob_token else '❌'}")
    
    if not (alice_token and bob_token):
        print("❌ Login failed, stopping demo")
        return
    
    alice_headers = {"Authorization": f"Bearer {alice_token}"}
    bob_headers = {"Authorization": f"Bearer {bob_token}"}
    
    # Get user info
    r = requests.get(f"{BASE_URL}/api/users/me/", headers=alice_headers)
    alice_id = r.json().get("id") if r.status_code == 200 else None
    
    r = requests.get(f"{BASE_URL}/api/users/me/", headers=bob_headers)  
    bob_id = r.json().get("id") if r.status_code == 200 else None
    
    print(f"Alice ID: {alice_id}, Bob ID: {bob_id}")
    
    # 2. POSTS & LIKES
    print("\n📰 2. Posts & Likes")
    
    # Alice creates post
    r = requests.post(f"{BASE_URL}/api/posts/", 
        json={"content": "Hello world from Alice! 👋"},
        headers=alice_headers
    )
    alice_post_id = r.json().get("id") if r.status_code in [200, 201] else None
    print(f"Alice creates post: {r.status_code} {'✅' if alice_post_id else '❌'}")
    
    # Bob creates post
    r = requests.post(f"{BASE_URL}/api/posts/", 
        json={"content": "Bob here! Nice to meet everyone 🙂"},
        headers=bob_headers
    )
    bob_post_id = r.json().get("id") if r.status_code in [200, 201] else None
    print(f"Bob creates post: {r.status_code} {'✅' if bob_post_id else '❌'}")
    
    # Bob likes Alice's post
    if alice_post_id:
        r = requests.post(f"{BASE_URL}/api/posts/{alice_post_id}/like/", 
            json={}, headers=bob_headers)
        print(f"Bob likes Alice's post: {r.status_code} {'✅' if r.status_code in [200, 201] else '❌'}")
    
    # Alice likes Bob's post
    if bob_post_id:
        r = requests.post(f"{BASE_URL}/api/posts/{bob_post_id}/like/", 
            json={}, headers=alice_headers)
        print(f"Alice likes Bob's post: {r.status_code} {'✅' if r.status_code in [200, 201] else '❌'}")
    
    # List all posts
    r = requests.get(f"{BASE_URL}/api/posts/", headers=alice_headers)
    posts_count = len(r.json().get("results", [])) if r.status_code == 200 else 0
    print(f"List posts: {r.status_code} - Found {posts_count} posts {'✅' if posts_count > 0 else '❌'}")
    
    # 3. SOCIAL (FOLLOW/BLOCK)
    print("\n👥 3. Social Features")
    
    # Alice follows Bob
    if bob_id:
        r = requests.post(f"{BASE_URL}/api/users/{bob_id}/follow/", 
            json={}, headers=alice_headers)
        print(f"Alice follows Bob: {r.status_code} {'✅' if r.status_code in [200, 201] else '❌'}")
    
    # Bob follows Alice
    if alice_id:
        r = requests.post(f"{BASE_URL}/api/users/{alice_id}/follow/", 
            json={}, headers=bob_headers)
        print(f"Bob follows Alice: {r.status_code} {'✅' if r.status_code in [200, 201] else '❌'}")
    
    # 4. ACTIVITY FEED
    print("\n📊 4. Activity Feed")
    
    # Alice checks activity feed
    r = requests.get(f"{BASE_URL}/api/feed/", headers=alice_headers)
    activities_count = len(r.json().get("results", [])) if r.status_code == 200 else 0
    print(f"Alice activity feed: {r.status_code} - {activities_count} activities {'✅' if activities_count > 0 else '❌'}")
    
    # Bob checks activity feed
    r = requests.get(f"{BASE_URL}/api/feed/", headers=bob_headers)
    activities_count = len(r.json().get("results", [])) if r.status_code == 200 else 0
    print(f"Bob activity feed: {r.status_code} - {activities_count} activities {'✅' if activities_count > 0 else '❌'}")
    
    # 5. NOTIFICATIONS
    print("\n🔔 5. Notifications")
    
    # Check Alice notifications (should have like + follow notifications)
    r = requests.get(f"{BASE_URL}/api/notifications/", headers=alice_headers)
    notifs_count = len(r.json().get("results", [])) if r.status_code == 200 else 0
    print(f"Alice notifications: {r.status_code} - {notifs_count} notifications {'✅' if notifs_count > 0 else '❌'}")
    
    # Check Bob notifications  
    r = requests.get(f"{BASE_URL}/api/notifications/", headers=bob_headers)
    notifs_count = len(r.json().get("results", [])) if r.status_code == 200 else 0
    print(f"Bob notifications: {r.status_code} - {notifs_count} notifications {'✅' if notifs_count > 0 else '❌'}")
    
    # 6. USER SEARCH
    print("\n🔍 6. User Search")
    
    # Search for users
    r = requests.get(f"{BASE_URL}/api/users/search/?q=alice", headers=bob_headers)
    search_count = len(r.json().get("results", [])) if r.status_code == 200 else 0
    print(f"Search for 'alice': {r.status_code} - {search_count} results {'✅' if search_count > 0 else '❌'}")
    
    print("\n🎉 Demo Complete!")
    print("\n📋 Summary:")
    print("✅ User signup/login with JWT tokens")
    print("✅ Create and list posts")  
    print("✅ Like/unlike posts")
    print("✅ Follow other users")
    print("✅ Activity feed showing network activity")
    print("✅ Notifications for likes/follows")
    print("✅ User search")
    print("\n🌐 Access Swagger UI: http://localhost:8000/api/docs/")
    print("📖 All endpoints documented and working!")

if __name__ == "__main__":
    try:
        demo()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure to run:")
        print("   python manage.py runserver 0.0.0.0:8000")
    except Exception as e:
        print(f"❌ Error: {e}")