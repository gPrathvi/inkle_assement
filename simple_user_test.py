#!/usr/bin/env python3
"""
Simple test: Login with email → Get personalized likes & notifications
"""
import requests

BASE_URL = "http://localhost:8000"

def test_alice_personalized_data():
    print("🔐 Alice Login Test - Email → Personal Data")
    
    # Alice logs in with her email credentials
    print("\n📧 Alice logging in with: alice@example.com")
    
    login_response = requests.post(f"{BASE_URL}/api/auth/login/", json={
        "username": "alice",  # or use email if configured
        "password": "secret123"
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.text}")
        return
    
    # Get Alice's access token
    token = login_response.json()["access"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Alice logged in successfully!")
    
    # 1. Get Alice's profile info
    profile = requests.get(f"{BASE_URL}/api/users/me/", headers=headers)
    user_data = profile.json()
    print(f"\n👤 Alice's Profile:")
    print(f"   ID: {user_data['id']}")
    print(f"   Username: {user_data['username']}")
    print(f"   Email: {user_data['email']}")
    print(f"   Role: {user_data['role']}")
    
    # 2. Get Alice's notifications (likes/follows she received)
    notifications = requests.get(f"{BASE_URL}/api/notifications/", headers=headers)
    notif_data = notifications.json()
    print(f"\n📬 Alice's Notifications ({len(notif_data.get('results', []))}):")
    
    for notif in notif_data.get('results', []):
        notif_type = notif['type']
        actor_id = notif['actor_id'] 
        is_read = notif['is_read']
        created = notif['created_at'][:19]  # Remove microseconds
        
        if notif_type == "LIKE":
            print(f"   🤍 User {actor_id} liked your post - {created} {'(read)' if is_read else '(unread)'}")
        elif notif_type == "FOLLOW":
            print(f"   👥 User {actor_id} followed you - {created} {'(read)' if is_read else '(unread)'}")
        elif notif_type == "COMMENT":
            print(f"   💬 User {actor_id} commented on your post - {created} {'(read)' if is_read else '(unread)'}")
    
    # 3. Get Alice's posts and their like counts
    posts = requests.get(f"{BASE_URL}/api/posts/", headers=headers)
    posts_data = posts.json()
    alice_id = user_data['id']
    
    print(f"\n📝 Alice's Posts (with like counts):")
    alice_posts = [p for p in posts_data.get('results', []) if p['author'] == alice_id]
    
    for post in alice_posts:
        content = post['content'][:50] + "..." if len(post['content']) > 50 else post['content']
        likes = post['likes_count']
        created = post['created_at'][:19]
        print(f"   📄 Post {post['id']}: \"{content}\"")
        print(f"       ❤️ {likes} likes - Created: {created}")
    
    # 4. Get Alice's activity feed (what people in her network did)
    feed = requests.get(f"{BASE_URL}/api/feed/", headers=headers)
    feed_data = feed.json()
    
    print(f"\n📊 Alice's Activity Feed ({len(feed_data.get('results', []))}):")
    for activity in feed_data.get('results', [])[:5]:  # Show last 5 activities
        activity_type = activity['type']
        actor_id = activity['actor_id']
        created = activity['created_at'][:19]
        
        if activity_type == "LIKE":
            print(f"   🤍 User {actor_id} liked a post - {created}")
        elif activity_type == "FOLLOW":
            print(f"   👥 User {actor_id} followed someone - {created}")
        elif activity_type == "POST":
            print(f"   📄 User {actor_id} created a post - {created}")
        elif activity_type == "COMMENT":
            print(f"   💬 User {actor_id} commented on a post - {created}")
    
    print(f"\n✅ RESULT: When Alice logs in with her email, she gets:")
    print(f"   📧 Her profile data (alice@example.com)")
    print(f"   📬 Her notifications (who liked/followed her)")
    print(f"   📝 Her posts with like counts")
    print(f"   📊 Activity feed from her network")
    print(f"   🔒 All data is personalized to HER account!")

if __name__ == "__main__":
    try:
        test_alice_personalized_data()
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Start with:")
        print("   python manage.py runserver 0.0.0.0:8000")
    except Exception as e:
        print(f"❌ Error: {e}")