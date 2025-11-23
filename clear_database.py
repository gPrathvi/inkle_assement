#!/usr/bin/env python3
"""
Clear all users and related data from the database
Start fresh with a clean database
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inkle_social.settings')
django.setup()

from django.contrib.auth import get_user_model
from posts.models import Post, Comment, Like
from social.models import Follow, Block
from activities.models import Activity
# Import Notification from the correct app
try:
    from activities.models import Notification
except ImportError:
    try:
        from users.models import Notification
    except ImportError:
        Notification = None

User = get_user_model()

def clear_all_data():
    print("🗑️ Clearing all data from database...")
    
    # Delete all data in order (to avoid foreign key constraints)
    
    if Notification:
        print("   Deleting notifications...")
        deleted_notifications = Notification.objects.all().delete()
        print(f"   ✅ Deleted {deleted_notifications[0]} notifications")
    else:
        print("   ⚠️ Notification model not found, skipping...")
    
    print("   Deleting activities...")
    deleted_activities = Activity.objects.all().delete()
    print(f"   ✅ Deleted {deleted_activities[0]} activities")
    
    print("   Deleting likes...")
    deleted_likes = Like.objects.all().delete()
    print(f"   ✅ Deleted {deleted_likes[0]} likes")
    
    print("   Deleting comments...")
    deleted_comments = Comment.objects.all().delete()
    print(f"   ✅ Deleted {deleted_comments[0]} comments")
    
    print("   Deleting follows...")
    deleted_follows = Follow.objects.all().delete()
    print(f"   ✅ Deleted {deleted_follows[0]} follows")
    
    print("   Deleting blocks...")
    deleted_blocks = Block.objects.all().delete()
    print(f"   ✅ Deleted {deleted_blocks[0]} blocks")
    
    print("   Deleting posts...")
    deleted_posts = Post.objects.all().delete()
    print(f"   ✅ Deleted {deleted_posts[0]} posts")
    
    print("   Deleting all users...")
    deleted_users = User.objects.all().delete()
    print(f"   ✅ Deleted {deleted_users[0]} users")
    
    print("\n🎉 Database cleared successfully!")
    print("✅ All users, posts, likes, follows, and notifications removed")
    print("🔄 You can now create fresh users")

def create_fresh_superuser():
    print("\n👑 Creating a new superuser...")
    
    username = input("Enter superuser username: ").strip()
    email = input("Enter superuser email: ").strip()
    password = input("Enter superuser password: ").strip()
    
    if not all([username, email, password]):
        print("❌ All fields are required")
        return
    
    try:
        superuser = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superuser '{username}' created successfully!")
        print(f"📧 Email: {email}")
        print(f"🔑 You can now login with these credentials")
        
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")

if __name__ == "__main__":
    print("🚨 WARNING: This will delete ALL data from the database!")
    print("   - All users")
    print("   - All posts") 
    print("   - All likes")
    print("   - All follows")
    print("   - All notifications")
    print("   - All activities")
    
    confirm = input("\n❓ Are you sure? Type 'YES' to continue: ").strip()
    
    if confirm.upper() == 'YES':
        clear_all_data()
        
        create_super = input("\n❓ Create a new superuser? (y/n): ").strip().lower()
        if create_super == 'y':
            create_fresh_superuser()
        
        print("\n🎯 Database is now clean!")
        print("🚀 Start the server and create new users:")
        print("   python manage.py runserver 0.0.0.0:8000")
        
    else:
        print("❌ Operation cancelled")