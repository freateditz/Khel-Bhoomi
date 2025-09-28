#!/usr/bin/env python3

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent / "backend"
load_dotenv(ROOT_DIR / '.env')

async def check_database():
    """Check the MongoDB Atlas database structure and existing users"""
    
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    collection = db[os.environ.get('COLLECTION_NAME', 'Data')]
    
    print("🔍 Checking MongoDB Atlas Database")
    print("=" * 50)
    print(f"Database: {os.environ['DB_NAME']}")
    print(f"Collection: {os.environ.get('COLLECTION_NAME', 'Data')}")
    print(f"Connection: {mongo_url[:50]}...")
    
    try:
        # Check total documents
        total_docs = await collection.count_documents({})
        print(f"\n📊 Total documents in collection: {total_docs}")
        
        # Check users
        user_count = await collection.count_documents({"type": "user"})
        print(f"👥 Total users: {user_count}")
        
        # Check posts
        post_count = await collection.count_documents({"type": "post"})
        print(f"📝 Total posts: {post_count}")
        
        # List all users
        print(f"\n👤 Existing Users:")
        print("-" * 30)
        users = await collection.find({"type": "user"}).to_list(length=None)
        
        if users:
            for user in users:
                print(f"  • {user.get('username', 'N/A')} ({user.get('role', 'N/A')}) - {user.get('email', 'N/A')}")
        else:
            print("  No users found in database")
        
        # Check for demo users specifically
        print(f"\n🎭 Demo Users Status:")
        print("-" * 30)
        demo_users = ["demo_athlete", "demo_scout", "demo_fan", "testuser"]
        
        for demo_user in demo_users:
            user_exists = await collection.find_one({"username": demo_user, "type": "user"})
            if user_exists:
                print(f"  ✅ {demo_user} exists")
            else:
                print(f"  ❌ {demo_user} NOT found")
        
        # Sample posts
        print(f"\n📄 Sample Posts:")
        print("-" * 30)
        posts = await collection.find({"type": "post"}).limit(3).to_list(length=3)
        
        if posts:
            for i, post in enumerate(posts, 1):
                print(f"  {i}. {post.get('username', 'N/A')}: {post.get('content', 'N/A')[:50]}...")
        else:
            print("  No posts found in database")
            
    except Exception as e:
        print(f"❌ Error checking database: {str(e)}")
    
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(check_database())