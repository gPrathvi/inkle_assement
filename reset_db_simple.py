#!/usr/bin/env python3
"""
Simple database reset - automatically clears all data
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inkle_social.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

def reset_database():
    print("🗑️ Resetting database...")
    
    try:
        with transaction.atomic():
            # Get all models from apps
            from django.apps import apps
            
            models_to_clear = []
            
            # Get all models from our apps
            for app_name in ['users', 'posts', 'social', 'activities', 'adminops']:
                try:
                    app_models = apps.get_app_config(app_name).get_models()
                    models_to_clear.extend(app_models)
                except:
                    continue
            
            # Clear in reverse order to avoid foreign key issues
            total_deleted = 0
            for model in reversed(models_to_clear):
                try:
                    count = model.objects.count()
                    if count > 0:
                        model.objects.all().delete()
                        total_deleted += count
                        print(f"   ✅ Cleared {count} records from {model.__name__}")
                except Exception as e:
                    print(f"   ⚠️ Could not clear {model.__name__}: {e}")
            
            print(f"\n🎉 Database reset complete!")
            print(f"📊 Total records deleted: {total_deleted}")
            print("✅ Ready for fresh users!")
            
    except Exception as e:
        print(f"❌ Error during reset: {e}")

def create_test_superuser():
    print("\n👑 Creating test superuser...")
    
    try:
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("✅ Test superuser created:")
        print("   Username: admin")
        print("   Email: admin@example.com") 
        print("   Password: admin123")
        
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")

if __name__ == "__main__":
    reset_database()
    create_test_superuser()
    
    print("\n🚀 Database is now clean!")
    print("🌐 You can now:")
    print("   1. Start server: python manage.py runserver 0.0.0.0:8000")
    print("   2. Open simple_frontend.html in browser")
    print("   3. Create new users with your real email!")