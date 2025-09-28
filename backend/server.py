from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
import jwt
from passlib.context import CryptContext
import bcrypt

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]
collection = db[os.environ.get('COLLECTION_NAME', 'Data')]

# JWT and Password setup
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-here')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# User Models
class UserRole(str):
    ATHLETE = "athlete"
    SCOUT = "scout"
    FAN = "fan"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str
    full_name: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    sports_interests: Optional[List[str]] = None

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    role: str
    full_name: str
    bio: Optional[str] = ""
    profile_image: Optional[str] = ""
    sports_interests: List[str] = []
    achievements: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

# Post Models
class PostCreate(BaseModel):
    content: str
    post_type: str = "text"  # text, image, video, achievement, news
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    sports_tags: List[str] = []

class Post(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    username: str
    user_role: str
    content: str
    post_type: str
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    sports_tags: List[str] = []
    likes: int = 0
    comments: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_data = await db.users.find_one({"username": username})
    if user_data is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return User(**user_data)

def prepare_for_mongo(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
    return data

def parse_from_mongo(item):
    if isinstance(item, dict):
        for key, value in item.items():
            if isinstance(value, str) and key.endswith('_at'):
                try:
                    item[key] = datetime.fromisoformat(value)
                except:
                    pass
    return item

# Authentication Routes
@api_router.post("/auth/register", response_model=Token)
async def register(user_data: UserCreate):
    # Check if user exists
    existing_user = await db.users.find_one({"$or": [{"username": user_data.username}, {"email": user_data.email}]})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Hash password
    hashed_password = get_password_hash(user_data.password)
    
    # Create user
    user = User(
        username=user_data.username,
        email=user_data.email,
        role=user_data.role,
        full_name=user_data.full_name
    )
    
    user_dict = user.dict()
    user_dict['password'] = hashed_password
    user_dict = prepare_for_mongo(user_dict)
    
    await db.users.insert_one(user_dict)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer", user=user)

@api_router.post("/auth/login", response_model=Token)
async def login(user_credentials: UserLogin):
    user_data = await db.users.find_one({"username": user_credentials.username})
    if not user_data or not verify_password(user_credentials.password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    user_data = parse_from_mongo(user_data)
    user = User(**{k: v for k, v in user_data.items() if k != 'password'})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer", user=user)

# Posts Routes
@api_router.post("/posts", response_model=Post)
async def create_post(post_data: PostCreate, current_user: User = Depends(get_current_user)):
    post = Post(
        user_id=current_user.id,
        username=current_user.username,
        user_role=current_user.role,
        content=post_data.content,
        post_type=post_data.post_type,
        image_url=post_data.image_url,
        video_url=post_data.video_url,
        sports_tags=post_data.sports_tags
    )
    
    post_dict = prepare_for_mongo(post.dict())
    await db.posts.insert_one(post_dict)
    
    return post

@api_router.get("/posts", response_model=List[Post])
async def get_posts(skip: int = 0, limit: int = 20):
    posts_data = await db.posts.find().sort("created_at", -1).skip(skip).limit(limit).to_list(length=None)
    posts = []
    for post_data in posts_data:
        post_data = parse_from_mongo(post_data)
        posts.append(Post(**post_data))
    return posts

@api_router.get("/posts/user/{user_id}", response_model=List[Post])
async def get_user_posts(user_id: str):
    posts_data = await db.posts.find({"user_id": user_id}).sort("created_at", -1).to_list(length=None)
    posts = []
    for post_data in posts_data:
        post_data = parse_from_mongo(post_data)
        posts.append(Post(**post_data))
    return posts

# User Profile Routes
@api_router.get("/users/me", response_model=User)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@api_router.get("/users/{username}", response_model=User)
async def get_user_profile(username: str):
    user_data = await db.users.find_one({"username": username})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = parse_from_mongo(user_data)
    return User(**{k: v for k, v in user_data.items() if k != 'password'})

@api_router.put("/users/me", response_model=User)
async def update_user_profile(user_update: UserUpdate, current_user: User = Depends(get_current_user)):
    # Prepare update data
    update_data = {}
    if user_update.full_name is not None:
        update_data['full_name'] = user_update.full_name
    if user_update.bio is not None:
        update_data['bio'] = user_update.bio
    if user_update.profile_image is not None:
        update_data['profile_image'] = user_update.profile_image
    if user_update.sports_interests is not None:
        update_data['sports_interests'] = user_update.sports_interests
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # Update user in database
    result = await db.users.update_one(
        {"id": current_user.id}, 
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Return updated user
    updated_user_data = await db.users.find_one({"id": current_user.id})
    if not updated_user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user_data = parse_from_mongo(updated_user_data)
    return User(**{k: v for k, v in updated_user_data.items() if k != 'password'})

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()