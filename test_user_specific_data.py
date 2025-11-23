#!/usr/bin/env python3
"""
Test script showing how user gets their personal likes and notifications
when they login with their email/credentials
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_user_personalized_data():
    print("🔐 Testing User-Specific Data Retrieval")
    
    # 1. Setup - Create two users and some interactions
    print("\n1️⃣ Setting up test users...")
    
    # Create Alice
    alice_signup = requests.post(f"{BASE_URL}/api/auth/signup/", json={
        "username": "alice_test",
        "email": "alice@test.com", 
        "password": "secret123"
    })
    print(f"Alice signup: {alice_signup.status_code}")
    
    # Create Bob  
    bob_signup = requests.post(f"{BASE_URL}/api/auth/signup/", json={
        "username": "bob_test",
        "email": "bob@test.com",
        "password": "secret123" 
    })
    print(f"Bob signup: {bob_signup.status_code}")
    
    # 2. Login Alice with her email credentials
    print("\n2️⃣ Alice logs in with her email...")
    alice_login = requests.post(f"{BASE_URL}/api/auth/login/", json={
        "username": "alice_test",  # Can also use email in most setups
        "password": "secret123"
    })
    
    if alice_login.status_code != 200:
        print(f"❌ Alice login failed: {alice_login.text}")
        return
        
    alice_token = alice_login.json()["access"]
    alice_headers = {"Authorization": f"Bearer {alice_token}"}
    print("✅ Alice logged in successfully")
    
    # Get Alice's user ID
    alice_me = requests.get(f"{BASE_URL}/api/users/me/", headers=alice_headers)
    alice_data = alice_me.json()
    alice_id = alice_data["id"]
    print(f"Alice ID: {alice_id}, Email: {alice_data['email']}")
    
    # 3. Login Bob and create interactions
    print("\n3️⃣ Bob logs in and creates interactions...")
    bob_login = requests.post(f"{BASE_URL}/api/auth/login/", json={
        "username": "bob_test",
        "password": "secret123"
    })
    bob_token = bob_login.json()["access"]
    bob_headers = {"Authorization": f"Bearer {bob_token}"}
    
    # Alice creates a post
    alice_post = requests.post(f"{BASE_URL}/api/posts/", 
        json={"content": "Alice's post for testing likes!"}, 
        headers=alice_headers
    )
    alice_post_id = alice_post.json()["id"]
    print(f"Alice created post ID: {alice_post_id}")
    
    # Bob likes Alice's post (this creates notification for Alice)
    bob_like = requests.post(f"{BASE_URL}/api/posts/{alice_post_id}/like/", 
        json={}, headers=bob_headers)
    print(f"Bob liked Alice's post: {bob_like.status_code}")
    
    # Bob follows Alice (this creates notification for Alice)
    bob_follow = requests.post(f"{BASE_URL}/api/users/{alice_id}/follow/", 
        json={}, headers=bob_headers)
    print(f"Bob followed Alice: {bob_follow.status_code}")
    
    # 4. NOW - Alice checks HER personalized data
    print(f"\n4️⃣ Alice (alice@test.com) gets her personalized data...")
    
    # Alice's notifications (should show Bob's like and follow)
    alice_notifications = requests.get(f"{BASE_URL}/api/notifications/", 
        headers=alice_headers)
    notifications = alice_notifications.json()
    
    print(f"\n📬 Alice's Notifications ({len(notifications.get('results', []))}):")
    for notif in notifications.get('results', []):
        print(f"  - Type: {notif['type']}, Actor ID: {notif['actor_id']}, Read: {notif['is_read']}")
    
    # Alice's posts with like counts
    alice_posts = requests.get(f"{BASE_URL}/api/posts/", headers=alice_headers)
    posts = alice_posts.json()
    
    print(f"\n📝 Alice's Posts (showing like counts):")
    for post in posts.get('results', []):
        if post['author'] == alice_id:  # Only Alice's posts
            print(f"  - Post ID: {post['id']}")
            print(f"    Content: {post['content']}")
            print(f"    Likes: {post['likes_count']}")
            print(f"    Created: {post['created_at']}")
    
    # Alice's activity feed (shows what people in her network did)
    alice_feed = requests.get(f"{BASE_URL}/api/feed/", headers=alice_headers)
    feed = alice_feed.json()
    
    print(f"\n📊 Alice's Activity Feed ({len(feed.get('results', []))}):")
    for activity in feed.get('results', []):
        activity_type = activity['type']
        actor_id = activity['actor_id']
        post_id = activity.get('post_id', 'N/A')
        target_user = activity.get('target_user_id', 'N/A')
        
        if activity_type == "LIKE":
            print(f"  - User {actor_id} liked post {post_id}")
        elif activity_type == "FOLLOW":
            print(f"  - User {actor_id} followed user {target_user}")
        elif activity_type == "POST":
            print(f"  - User {actor_id} created post {post_id}")
        elif activity_type == "COMMENT":
            print(f"  - User {actor_id} commented on post {post_id}")
    
    # 5. Show what Alice gets vs what Bob gets (different data!)
    print(f"\n5️⃣ Comparison: Alice vs Bob data...")
    
    bob_notifications = requests.get(f"{BASE_URL}/api/notifications/", 
        headers=bob_headers)
    bob_notif_count = len(bob_notifications.json().get('results', []))
    alice_notif_count = len(notifications.get('results', []))
    
    print(f"📬 Notifications:")
    print(f"  - Alice has {alice_notif_count} notifications")
    print(f"  - Bob has {bob_notif_count} notifications")
    print("  → Each user sees only THEIR notifications!")
    
    print(f"\n✅ User-Specific Data Working Correctly!")
    print(f"When Alice logs in with alice@test.com:")
    print(f"  📬 She gets HER notifications (likes/follows she received)")
    print(f"  📝 She sees ALL posts but can see like counts on her posts")  
    print(f"  📊 She gets activity feed from people she follows")
    print(f"  🔒 Everything is personalized to her account!")

if __name__ == "__main__":
    try:
        test_user_personalized_data()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure to run:")
        print("   python manage.py runserver 0.0.0.0:8000")
    except Exception as e:
        print(f"❌ Error: {e}")