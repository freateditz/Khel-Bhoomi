#!/usr/bin/env python3
"""
Script to create dummy users for easy login access to Khel Bhoomi
"""

import asyncio
import os
import sys
import uuid
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from pathlib import Path

# Add the backend directory to Python path to import modules
sys.path.append(str(Path(__file__).parent / 'backend'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / 'backend' / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL'] 
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# Dummy users data
DUMMY_USERS = [
    {
        "id": str(uuid.uuid4()),
        "username": "demo_athlete",
        "email": "athlete@demo.com",
        "password": "demo123",
        "full_name": "Alex Champion",
        "role": "athlete",
        "bio": "Professional basketball player from Mumbai. State champion and aspiring to play at national level.",
        "profile_image": "",
        "sports_interests": ["Basketball", "Track & Field"],
        "achievements": ["State Championship Winner 2024", "Best Player Award - Regional Tournament"],
        "created_at": datetime.now(timezone.utc)
    },
    {
        "id": str(uuid.uuid4()),
        "username": "demo_scout", 
        "email": "scout@demo.com",
        "password": "demo123",
        "full_name": "Sarah Talent Finder",
        "role": "scout",
        "bio": "Professional sports scout with 8+ years experience in discovering young talent across India.",
        "profile_image": "",
        "sports_interests": ["Basketball", "Football", "Swimming", "Track & Field"],
        "achievements": ["89 Athletes Scouted", "23 Successful Placements", "95% Success Rate"],
        "created_at": datetime.now(timezone.utc)
    },
    {
        "id": str(uuid.uuid4()),
        "username": "demo_fan",
        "email": "fan@demo.com", 
        "password": "demo123",
        "full_name": "Raj Sports Lover",
        "role": "fan",
        "bio": "Passionate sports enthusiast who loves following athletes and supporting upcoming talent.",
        "profile_image": "",
        "sports_interests": ["Cricket", "Football", "Basketball", "Hockey"],
        "achievements": [],
        "created_at": datetime.now(timezone.utc)
    },
    {
        "id": str(uuid.uuid4()),
        "username": "testuser",
        "email": "test@test.com",
        "password": "password",
        "full_name": "Test User",
        "role": "fan",
        "bio": "A simple test user for quick access.",
        "profile_image": "",
        "sports_interests": ["General Sports"],
        "achievements": [],
        "created_at": datetime.now(timezone.utc)
    }
]

def prepare_for_mongo(data):
    """Convert datetime objects to ISO format for MongoDB storage"""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
    return data

async def create_dummy_users():
    """Create dummy users in the database"""
    print("🚀 Creating dummy users for Khel Bhoomi...")
    
    try:
        # Clear existing dummy users first (optional)
        dummy_usernames = [user["username"] for user in DUMMY_USERS]
        result = await db.users.delete_many({"username": {"$in": dummy_usernames}})
        if result.deleted_count > 0:
            print(f"🗑️  Removed {result.deleted_count} existing dummy users")
        
        # Create new dummy users
        for user_data in DUMMY_USERS:
            # Hash the password
            user_data["password"] = get_password_hash(user_data["password"])
            
            # Prepare for MongoDB storage
            user_data = prepare_for_mongo(user_data)
            
            # Insert into database
            await db.users.insert_one(user_data)
            print(f"✅ Created user: {user_data['username']} ({user_data['role']})")
        
        print("\n🎉 Successfully created all dummy users!")
        print("\n📋 Login Credentials:")
        print("=" * 50)
        print("👤 Athlete Account:")
        print("   Username: demo_athlete")
        print("   Password: demo123")
        print("\n🎯 Scout Account:")
        print("   Username: demo_scout") 
        print("   Password: demo123")
        print("\n❤️  Fan Account:")
        print("   Username: demo_fan")
        print("   Password: demo123")
        print("\n🧪 Test Account:")
        print("   Username: testuser")
        print("   Password: password")
        print("=" * 50)
        
        # Create some sample posts
        await create_sample_posts()
        
    except Exception as e:
        print(f"❌ Error creating dummy users: {e}")
    finally:
        client.close()

async def create_sample_posts():
    """Create some sample posts to populate the feed"""
    print("\n📝 Creating sample posts...")
    
    # Get user IDs for the dummy users
    users = await db.users.find({"username": {"$in": ["demo_athlete", "demo_scout", "demo_fan"]}}).to_list(length=None)
    user_map = {user["username"]: user for user in users}
    
    sample_posts = [
        {
            "id": str(uuid.uuid4()),
            "user_id": user_map["demo_athlete"]["id"],
            "username": "demo_athlete",
            "user_role": "athlete",
            "content": "Just finished an intense training session! 🏀 Working on my three-point shots for the upcoming championship. The dedication is paying off - feeling stronger every day! #Basketball #Training #ChampionMindset",
            "post_type": "text",
            "image_url": None,
            "video_url": None,
            "sports_tags": ["Basketball", "Training"],
            "likes": 34,
            "comments": 8,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "user_id": user_map["demo_scout"]["id"],
            "username": "demo_scout", 
            "user_role": "scout",
            "content": "Excited to announce that our latest discovery, Priya Sharma, has been selected for the national track & field team! 🎉 This is what happens when talent meets opportunity. Keep an eye on this rising star! #TalentScout #TrackAndField #ProudMoment",
            "post_type": "text",
            "image_url": None,
            "video_url": None,
            "sports_tags": ["Track & Field", "Scouting"],
            "likes": 67,
            "comments": 15,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "user_id": user_map["demo_fan"]["id"],
            "username": "demo_fan",
            "user_role": "fan", 
            "content": "What an incredible match last night! The level of skill and determination shown by both teams was absolutely phenomenal. This is why I love sports - it brings out the best in people! 🔥⚽ #Football #SportsLover #Amazing",
            "post_type": "text",
            "image_url": None,
            "video_url": None,
            "sports_tags": ["Football"],
            "likes": 23,
            "comments": 5,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "user_id": user_map["demo_athlete"]["id"],
            "username": "demo_athlete",
            "user_role": "athlete",
            "content": "Grateful for all the support from my coaches and teammates! 🙏 Just achieved a personal best in my sprint time. Small improvements every day lead to big achievements! #Gratitude #PersonalBest #TeamWork",
            "post_type": "achievement",
            "image_url": None,
            "video_url": None,
            "sports_tags": ["Track & Field", "Achievement"],
            "likes": 89,
            "comments": 12,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    # Insert sample posts
    for post in sample_posts:
        await db.posts.insert_one(post)
        print(f"✅ Created post by {post['username']}")
    
    print("🎉 Sample posts created successfully!")

if __name__ == "__main__":
    asyncio.run(create_dummy_users())