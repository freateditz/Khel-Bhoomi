import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

async def test_mongodb_connection():
    """Test MongoDB Atlas connection and check demo users"""
    
    # Load environment variables
    ROOT_DIR = Path(__file__).parent / "backend"
    load_dotenv(ROOT_DIR / '.env')
    
    mongo_url = os.environ['MONGO_URL']
    db_name = os.environ['DB_NAME']
    collection_name = os.environ.get('COLLECTION_NAME', 'Data')
    
    print("🔍 Testing MongoDB Atlas Connection")
    print("=" * 50)
    print(f"Database: {db_name}")
    print(f"Collection: {collection_name}")
    print(f"Connection URL: {mongo_url[:50]}...")
    
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        collection = db[collection_name]
        
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful")
        
        # Check demo users
        demo_users = ["demo_athlete", "demo_scout", "demo_fan", "testuser"]
        
        print(f"\n👥 Checking Demo Users in Database")
        print("-" * 40)
        
        for username in demo_users:
            user = await collection.find_one({"username": username, "type": "user"})
            if user:
                print(f"✅ {username} exists - Role: {user.get('role', 'N/A')}, Email: {user.get('email', 'N/A')}")
            else:
                print(f"❌ {username} NOT FOUND in database")
        
        # Count total users and posts
        user_count = await collection.count_documents({"type": "user"})
        post_count = await collection.count_documents({"type": "post"})
        
        print(f"\n📊 Database Statistics")
        print("-" * 40)
        print(f"Total Users: {user_count}")
        print(f"Total Posts: {post_count}")
        
        # List all users
        print(f"\n📋 All Users in Database")
        print("-" * 40)
        users = await collection.find({"type": "user"}).to_list(length=None)
        for user in users:
            print(f"- {user.get('username', 'N/A')} ({user.get('role', 'N/A')}) - {user.get('email', 'N/A')}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_mongodb_connection())