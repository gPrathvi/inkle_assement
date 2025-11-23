#!/usr/bin/env python3
"""
Real User Setup - Create account with YOUR actual email
Then test real-time notifications and likes
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def setup_real_user():
    print("🔑 Real User Setup - Enter YOUR actual details")
    
    # Get user's real information
    print("\n📧 Enter your real details:")
    your_email = input("Your email: ")
    your_username = input("Your username: ")
    your_password = input("Your password: ")
    
    print(f"\n🔧 Setting up account for: {your_email}")
    
    # 1. Create account with real email
    signup_data = {
        "username": your_username,
        "email": your_email,
        "password": your_password
    }
    
    signup = requests.post(f"{BASE_URL}/api/auth/signup/", json=signup_data)
    
    if signup.status_code == 201:
        print("✅ Account created successfully!")
    elif signup.status_code == 400:
        print("ℹ️ Account already exists, proceeding with login...")
    else:
        print(f"❌ Signup failed: {signup.text}")
        return
    
    # 2. Login with real credentials
    login_data = {
        "username": your_username,
        "password": your_password
    }
    
    login = requests.post(f"{BASE_URL}/api/auth/login/", json=login_data)
    
    if login.status_code != 200:
        print(f"❌ Login failed: {login.text}")
        return
    
    your_token = login.json()["access"]
    your_headers = {"Authorization": f"Bearer {your_token}"}
    
    print(f"✅ Logged in successfully!")
    
    # 3. Get your profile
    profile = requests.get(f"{BASE_URL}/api/users/me/", headers=your_headers)
    your_data = profile.json()
    your_id = your_data["id"]
    
    print(f"\n👤 Your Profile:")
    print(f"   ID: {your_id}")
    print(f"   Username: {your_data['username']}")
    print(f"   Email: {your_data['email']}")
    print(f"   Joined: {your_data['date_joined'][:10]}")
    
    # 4. Create some demo users to interact with you
    print(f"\n🤖 Creating demo users to interact with your account...")
    
    demo_users = [
        {"username": "demo_alice", "email": "demo_alice@example.com", "password": "demo123"},
        {"username": "demo_bob", "email": "demo_bob@example.com", "password": "demo123"},
        {"username": "demo_charlie", "email": "demo_charlie@example.com", "password": "demo123"}
    ]
    
    demo_tokens = []
    
    for user in demo_users:
        # Create demo user
        requests.post(f"{BASE_URL}/api/auth/signup/", json=user)
        
        # Login demo user
        login_resp = requests.post(f"{BASE_URL}/api/auth/login/", json={
            "username": user["username"],
            "password": user["password"]
        })
        
        if login_resp.status_code == 200:
            demo_token = login_resp.json()["access"]
            demo_tokens.append((user["username"], demo_token))
            print(f"   ✅ Created: {user['username']}")
    
    # 5. Create a post with YOUR account
    print(f"\n📝 Creating a post with your account...")
    
    post_content = f"Hello! This is {your_username}'s real post at {datetime.now().strftime('%H:%M')}"
    post_data = {"content": post_content}
    
    create_post = requests.post(f"{BASE_URL}/api/posts/", 
        json=post_data, headers=your_headers)
    
    if create_post.status_code in [200, 201]:
        your_post_id = create_post.json()["id"]
        print(f"   ✅ Created post ID: {your_post_id}")
        print(f"   Content: {post_content}")
    else:
        print(f"   ❌ Post creation failed: {create_post.text}")
        return
    
    # 6. Demo users interact with YOUR post
    print(f"\n🎭 Demo users interacting with YOUR post...")
    
    for demo_name, demo_token in demo_tokens:
        demo_headers = {"Authorization": f"Bearer {demo_token}"}
        
        # Demo user likes YOUR post
        like_resp = requests.post(f"{BASE_URL}/api/posts/{your_post_id}/like/", 
            json={}, headers=demo_headers)
        
        if like_resp.status_code in [200, 201]:
            print(f"   ❤️ {demo_name} liked your post")
        
        # Demo user follows YOU
        follow_resp = requests.post(f"{BASE_URL}/api/users/{your_id}/follow/", 
            json={}, headers=demo_headers)
        
        if follow_resp.status_code in [200, 201]:
            print(f"   👥 {demo_name} followed you")
    
    # 7. NOW CHECK YOUR REAL-TIME DATA
    print(f"\n🔍 Checking YOUR real-time data for {your_email}...")
    
    # Your notifications (real-time)
    notifications = requests.get(f"{BASE_URL}/api/notifications/", headers=your_headers)
    notif_data = notifications.json()
    
    print(f"\n📬 YOUR Notifications ({len(notif_data.get('results', []))}):")
    for notif in notif_data.get('results', []):
        notif_type = notif['type']
        created = notif['created_at'][:19]
        is_read = notif['is_read']
        
        if notif_type == "LIKE":
            print(f"   ❤️ Someone liked your post - {created} {'(read)' if is_read else '(NEW!)'}")
        elif notif_type == "FOLLOW":
            print(f"   👥 Someone followed you - {created} {'(read)' if is_read else '(NEW!)'}")
    
    # Your posts with like counts (real-time)
    posts = requests.get(f"{BASE_URL}/api/posts/", headers=your_headers)
    posts_data = posts.json()
    
    print(f"\n📝 YOUR Posts with Like Counts:")
    your_posts = [p for p in posts_data.get('results', []) if p['author'] == your_id]
    
    for post in your_posts:
        content = post['content'][:50] + "..." if len(post['content']) > 50 else post['content']
        likes = post['likes_count']
        created = post['created_at'][:19]
        print(f"   📄 Post {post['id']}: \"{content}\"")
        print(f"       ❤️ {likes} likes - Created: {created}")
    
    # Your activity feed (real-time)
    feed = requests.get(f"{BASE_URL}/api/feed/", headers=your_headers)
    feed_data = feed.json()
    
    print(f"\n📊 YOUR Activity Feed:")
    for activity in feed_data.get('results', [])[:5]:
        activity_type = activity['type']
        created = activity['created_at'][:19]
        
        if activity_type == "LIKE":
            print(f"   ❤️ Someone liked a post - {created}")
        elif activity_type == "FOLLOW":
            print(f"   👥 Someone followed someone - {created}")
        elif activity_type == "POST":
            print(f"   📄 Someone created a post - {created}")
    
    print(f"\n🎉 SUCCESS! Your real email ({your_email}) is working!")
    print(f"✅ You can now login and get YOUR real notifications and likes!")
    print(f"\n🔑 Your Login Credentials:")
    print(f"   Email/Username: {your_username}")
    print(f"   Password: {your_password}")
    print(f"   Login URL: {BASE_URL}/api/auth/login/")

if __name__ == "__main__":
    try:
        setup_real_user()
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Start with:")
        print("   python manage.py runserver 0.0.0.0:8000")
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")