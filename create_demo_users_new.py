#!/usr/bin/env python3
"""
Script to create demo users for Khel Bhoomi platform with the new collection structure.
This script populates users, login, signup, and profile collections.
"""

import asyncio
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from passlib.context import CryptContext
import uuid

# Add backend to path to import models
sys.path.append('/app/backend')

# Load environment
ROOT_DIR = Path(__file__).parent / "backend"
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def create_demo_users():
    """Create demo users for the Khel Bhoomi platform"""
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Collections
    users_collection = db['users']
    login_collection = db['login']
    signup_collection = db['signup']
    profile_collection = db['profile']
    posts_collection = db['posts']
    
    print("🎯 Creating Demo Users for Khel Bhoomi")
    print("=" * 50)
    
    # Demo users data
    demo_users = [
        {
            "username": "demo_athlete",
            "email": "athlete@khelbhoomi.com",
            "password": "demo123",
            "role": "athlete",
            "full_name": "Arjun Kumar",
            "bio": "Professional cricket player from Mumbai. Passionate about the game and always striving for excellence.",
            "sports_interests": ["Cricket", "Football", "Swimming"],
            "achievements": ["State Level Cricket Championship Winner 2023", "Mumbai District Football Captain"]
        },
        {
            "username": "demo_scout",
            "email": "scout@khelbhoomi.com", 
            "password": "demo123",
            "role": "scout",
            "full_name": "Priya Sharma",
            "bio": "Professional sports scout with 10+ years experience. I help talented athletes reach their potential.",
            "sports_interests": ["Cricket", "Basketball", "Tennis"],
            "achievements": ["Discovered 15+ professional athletes", "Best Scout Award 2022"]
        },
        {
            "username": "demo_fan",
            "email": "fan@khelbhoomi.com",
            "password": "demo123", 
            "role": "fan",
            "full_name": "Rahul Singh",
            "bio": "Die-hard sports enthusiast! Love watching cricket, football, and supporting upcoming athletes.",
            "sports_interests": ["Cricket", "Football", "Hockey", "Tennis"],
            "achievements": ["Cricket Fan Club President", "Organized 5 sports viewing events"]
        },
        {
            "username": "testuser",
            "email": "test@khelbhoomi.com",
            "password": "password",
            "role": "fan",
            "full_name": "Test User",
            "bio": "Test account for Khel Bhoomi platform. Sports lover and community member.",
            "sports_interests": ["Football", "Basketball"],
            "achievements": ["Beta Tester", "Community Contributor"]
        }
    ]
    
    created_users = []
    
    for user_data in demo_users:
        try:
            # Check if user already exists
            existing_user = await users_collection.find_one({"username": user_data["username"]})
            if existing_user:
                print(f"✅ User {user_data['username']} already exists")
                continue
                
            # Create user ID
            user_id = str(uuid.uuid4())
            current_time = datetime.now(timezone.utc)
            
            # Hash password
            hashed_password = get_password_hash(user_data["password"])
            
            # 1. Create user in users collection
            user_doc = {
                "id": user_id,
                "username": user_data["username"],
                "email": user_data["email"],
                "password": hashed_password,
                "role": user_data["role"],
                "full_name": user_data["full_name"],
                "bio": user_data.get("bio", ""),
                "profile_image": "",
                "sports_interests": user_data.get("sports_interests", []),
                "achievements": user_data.get("achievements", []),
                "created_at": current_time.isoformat()
            }
            await users_collection.insert_one(user_doc)
            
            # 2. Create signup record
            signup_record = {
                "id": str(uuid.uuid4()),
                "username": user_data["username"],
                "email": user_data["email"],
                "role": user_data["role"],
                "full_name": user_data["full_name"],
                "signup_time": current_time.isoformat()
            }
            await signup_collection.insert_one(signup_record)
            
            # 3. Create profile record
            profile_record = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "username": user_data["username"],
                "full_name": user_data["full_name"],
                "bio": user_data.get("bio", ""),
                "profile_image": "",
                "sports_interests": user_data.get("sports_interests", []),
                "achievements": user_data.get("achievements", []),
                "followers_count": 0,
                "following_count": 0,
                "posts_count": 0,
                "created_at": current_time.isoformat()
            }
            await profile_collection.insert_one(profile_record)
            
            created_users.append(user_data)
            print(f"✅ Created user: {user_data['username']} ({user_data['role']})")
            
        except Exception as e:
            print(f"❌ Error creating user {user_data['username']}: {str(e)}")
    
    # Create sample posts for demo users
    sample_posts = [
        {
            "username": "demo_athlete",
            "content": "Just finished an intense cricket training session! Working on my batting technique for the upcoming tournament. 🏏",
            "post_type": "text",
            "sports_tags": ["Cricket", "Training"]
        },
        {
            "username": "demo_scout", 
            "content": "Attended the state-level basketball championship today. So many talented young players! Excited to connect with some promising athletes. 🏀",
            "post_type": "text",
            "sports_tags": ["Basketball", "Scouting"]
        },
        {
            "username": "demo_fan",
            "content": "What an incredible match! The energy in the stadium was absolutely electric. Nothing beats live sports! ⚡",
            "post_type": "text", 
            "sports_tags": ["Cricket", "Stadium"]
        }
    ]
    
    print(f"\n📝 Creating Sample Posts")
    print("-" * 30)
    
    for post_data in sample_posts:
        try:
            # Find user
            user = await users_collection.find_one({"username": post_data["username"]})
            if user:
                post_doc = {
                    "id": str(uuid.uuid4()),
                    "user_id": user["id"],
                    "username": post_data["username"],
                    "user_role": user["role"],
                    "content": post_data["content"],
                    "post_type": post_data["post_type"],
                    "image_url": None,
                    "video_url": None,
                    "sports_tags": post_data["sports_tags"],
                    "likes": 0,
                    "comments": 0,
                    "created_at": datetime.now(timezone.utc).isoformat()
                }
                await posts_collection.insert_one(post_doc)
                
                # Update post count in profile
                await profile_collection.update_one(
                    {"username": post_data["username"]},
                    {"$inc": {"posts_count": 1}}
                )
                
                print(f"✅ Created post for {post_data['username']}")
        except Exception as e:
            print(f"❌ Error creating post for {post_data['username']}: {str(e)}")
    
    # Summary
    print(f"\n🎉 Demo Users Setup Complete!")
    print("-" * 40)
    print(f"✅ Created {len(created_users)} users")
    print(f"✅ Created {len(sample_posts)} sample posts")
    
    print(f"\n🔑 Login Credentials:")
    print("-" * 20)
    for user in demo_users:
        print(f"👤 {user['role'].title()}: {user['username']} / {user['password']}")
    
    # Check collections
    print(f"\n📊 Database Statistics:")
    print("-" * 25)
    users_count = await users_collection.count_documents({})
    profiles_count = await profile_collection.count_documents({})
    posts_count = await posts_collection.count_documents({})
    signup_count = await signup_collection.count_documents({})
    
    print(f"Users: {users_count}")
    print(f"Profiles: {profiles_count}") 
    print(f"Posts: {posts_count}")
    print(f"Signups: {signup_count}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_demo_users())