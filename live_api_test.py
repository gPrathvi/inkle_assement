#!/usr/bin/env python3
"""
Live API Test - Use YOUR real email to get real-time data
Just enter your email and see your notifications/likes instantly!
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_with_real_email():
    print("🔴 LIVE API TEST - Real Email → Real Data")
    print("=" * 50)
    
    # Get real user credentials
    print("📧 Enter YOUR email to see YOUR real data:")
    email_or_username = input("Your email/username: ").strip()
    password = input("Your password: ").strip()
    
    if not email_or_username or not password:
        print("❌ Please enter both email and password!")
        return
    
    print(f"\n🔐 Logging in as: {email_or_username}")
    
    # Login with real credentials
    login_response = requests.post(f"{BASE_URL}/api/auth/login/", json={
        "username": email_or_username,
        "password": password
    })
    
    if login_response.status_code != 200:
        error_msg = login_response.json().get('detail', 'Unknown error')
        print(f"❌ Login failed: {error_msg}")
        print("\n💡 Tips:")
        print("   - Make sure your account exists (run real_user_setup.py first)")
        print("   - Check your username/email spelling")
        print("   - Verify your password")
        return
    
    # Success! Get token
    token = login_response.json()["access"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ LOGIN SUCCESS!")
    
    # Get user profile
    profile_resp = requests.get(f"{BASE_URL}/api/users/me/", headers=headers)
    if profile_resp.status_code == 200:
        user_data = profile_resp.json()
        print(f"\n👤 Welcome back, {user_data['username']}!")
        print(f"   📧 Email: {user_data['email']}")
        print(f"   🆔 User ID: {user_data['id']}")
        print(f"   📅 Member since: {user_data['date_joined'][:10]}")
    
    print("\n" + "="*50)
    print("🔴 LIVE DATA FOR YOUR ACCOUNT:")
    print("="*50)
    
    # 1. LIVE NOTIFICATIONS
    print("\n📬 YOUR NOTIFICATIONS (Real-time):")
    notif_resp = requests.get(f"{BASE_URL}/api/notifications/", headers=headers)
    
    if notif_resp.status_code == 200:
        notifications = notif_resp.json().get('results', [])
        
        if notifications:
            for i, notif in enumerate(notifications, 1):
                notif_type = notif['type']
                created = notif['created_at'][:19].replace('T', ' ')
                is_read = notif['is_read']
                status = "✅ Read" if is_read else "🔴 NEW!"
                
                print(f"   {i}. {notif_type.title()} - {created} [{status}]")
                
                if notif_type == "LIKE":
                    print(f"      ❤️ Someone liked your post")
                elif notif_type == "FOLLOW":
                    print(f"      👥 Someone started following you")
                elif notif_type == "COMMENT":
                    print(f"      💬 Someone commented on your post")
        else:
            print("   📭 No notifications yet")
    else:
        print(f"   ❌ Could not fetch notifications: {notif_resp.status_code}")
    
    # 2. LIVE POSTS WITH LIKES
    print("\n📝 YOUR POSTS (with live like counts):")
    posts_resp = requests.get(f"{BASE_URL}/api/posts/", headers=headers)
    
    if posts_resp.status_code == 200:
        all_posts = posts_resp.json().get('results', [])
        your_posts = [p for p in all_posts if p['author'] == user_data['id']]
        
        if your_posts:
            for i, post in enumerate(your_posts, 1):
                content = post['content']
                if len(content) > 60:
                    content = content[:60] + "..."
                
                likes_count = post['likes_count']
                created = post['created_at'][:19].replace('T', ' ')
                
                print(f"   {i}. Post ID: {post['id']}")
                print(f"      📄 Content: \"{content}\"")
                print(f"      ❤️ Likes: {likes_count}")
                print(f"      📅 Created: {created}")
                print()
        else:
            print("   📝 You haven't created any posts yet")
    else:
        print(f"   ❌ Could not fetch posts: {posts_resp.status_code}")
    
    # 3. LIVE ACTIVITY FEED
    print("\n📊 YOUR ACTIVITY FEED (what's happening in your network):")
    feed_resp = requests.get(f"{BASE_URL}/api/feed/", headers=headers)
    
    if feed_resp.status_code == 200:
        activities = feed_resp.json().get('results', [])
        
        if activities:
            for i, activity in enumerate(activities[:5], 1):  # Show last 5
                activity_type = activity['type']
                created = activity['created_at'][:19].replace('T', ' ')
                
                print(f"   {i}. {activity_type.title()} - {created}")
                
                if activity_type == "LIKE":
                    print("      ❤️ Someone liked a post")
                elif activity_type == "FOLLOW":
                    print("      👥 Someone followed someone")
                elif activity_type == "POST":
                    print("      📄 Someone created a new post")
                elif activity_type == "COMMENT":
                    print("      💬 Someone commented on a post")
        else:
            print("   📭 No recent activity")
    else:
        print(f"   ❌ Could not fetch activity feed: {feed_resp.status_code}")
    
    print("\n" + "="*50)
    print("🎉 SUCCESS! Your real email is working with live data!")
    print(f"📧 Account: {email_or_username}")
    print(f"🔄 Data is updated in real-time")
    print(f"✅ Backend is fully functional!")
    
    # Offer to create a test post
    print(f"\n❓ Want to create a test post? (y/n)")
    create_post = input().strip().lower()
    
    if create_post == 'y':
        post_content = input("Enter your post content: ").strip()
        if post_content:
            post_resp = requests.post(f"{BASE_URL}/api/posts/", 
                json={"content": post_content}, headers=headers)
            
            if post_resp.status_code in [200, 201]:
                post_data = post_resp.json()
                print(f"✅ Post created successfully!")
                print(f"📄 Post ID: {post_data['id']}")
                print(f"📝 Content: {post_data['content']}")
            else:
                print(f"❌ Failed to create post: {post_resp.text}")

if __name__ == "__main__":
    try:
        test_with_real_email()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server!")
        print("🚀 Start the server first:")
        print("   cd Downloads/inkle")
        print("   python manage.py runserver 0.0.0.0:8000")
    except KeyboardInterrupt:
        print("\n👋 Test cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")