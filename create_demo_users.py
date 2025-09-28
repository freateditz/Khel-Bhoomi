#!/usr/bin/env python3

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
from passlib.context import CryptContext
import uuid
from datetime import datetime, timezone

# Load environment variables
ROOT_DIR = Path(__file__).parent / "backend"
load_dotenv(ROOT_DIR / '.env')

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def create_demo_users():
    """Create demo users in MongoDB Atlas database"""
    
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    collection = db[os.environ.get('COLLECTION_NAME', 'Data')]
    
    print("🎭 Creating Demo Users in MongoDB Atlas")
    print("=" * 50)
    
    # Demo users data
    demo_users = [
        {
            "username": "demo_athlete",
            "email": "demo.athlete@khelbhoomi.com",
            "password": "demo123",
            "role": "athlete",
            "full_name": "Demo Athlete",
            "bio": "Professional athlete passionate about cricket and football",
            "sports_interests": ["Cricket", "Football", "Basketball"]
        },
        {
            "username": "demo_scout",
            "email": "demo.scout@khelbhoomi.com", 
            "password": "demo123",
            "role": "scout",
            "full_name": "Demo Scout",
            "bio": "Talent scout looking for the next sports stars",
            "sports_interests": ["Cricket", "Football", "Tennis", "Swimming"]
        },
        {
            "username": "demo_fan",
            "email": "demo.fan@khelbhoomi.com",
            "password": "demo123", 
            "role": "fan",
            "full_name": "Demo Fan",
            "bio": "Sports enthusiast and passionate fan",
            "sports_interests": ["Cricket", "Football", "Hockey", "Badminton"]
        },
        {
            "username": "testuser",
            "email": "testuser@khelbhoomi.com",
            "password": "password",
            "role": "fan", 
            "full_name": "Test User",
            "bio": "Test user for development purposes",
            "sports_interests": ["Cricket", "Football"]
        }
    ]
    
    try:
        created_count = 0
        
        for user_data in demo_users:
            # Check if user already exists
            existing_user = await collection.find_one({
                "$or": [
                    {"username": user_data["username"]}, 
                    {"email": user_data["email"]}
                ], 
                "type": "user"
            })
            
            if existing_user:
                print(f"  ⚠️  {user_data['username']} already exists, skipping...")
                continue
            
            # Create user document
            user_doc = {
                "id": str(uuid.uuid4()),
                "username": user_data["username"],
                "email": user_data["email"],
                "password": get_password_hash(user_data["password"]),
                "role": user_data["role"],
                "full_name": user_data["full_name"],
                "bio": user_data["bio"],
                "profile_image": "",
                "sports_interests": user_data["sports_interests"],
                "achievements": [],
                "created_at": datetime.now(timezone.utc).isoformat(),
                "type": "user"  # Important: type field for single collection
            }
            
            # Insert user
            await collection.insert_one(user_doc)
            created_count += 1
            print(f"  ✅ Created {user_data['username']} ({user_data['role']})")
        
        print(f"\n🎉 Successfully created {created_count} demo users!")
        
        # Verify creation
        print(f"\n🔍 Verification:")
        print("-" * 30)
        for user_data in demo_users:
            user_exists = await collection.find_one({"username": user_data["username"], "type": "user"})
            if user_exists:
                print(f"  ✅ {user_data['username']} verified in database")
            else:
                print(f"  ❌ {user_data['username']} NOT found")
                
    except Exception as e:
        print(f"❌ Error creating demo users: {str(e)}")
    
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(create_demo_users())