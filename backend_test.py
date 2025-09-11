import requests
import sys
import json
from datetime import datetime

class KhelBhoomiAPITester:
    def __init__(self, base_url="https://quick-access-18.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.current_user = None
        self.created_post_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'
        
        if headers:
            test_headers.update(headers)

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    if isinstance(response_data, dict) and len(str(response_data)) < 500:
                        print(f"   Response: {json.dumps(response_data, indent=2)}")
                    elif isinstance(response_data, list):
                        print(f"   Response: List with {len(response_data)} items")
                except:
                    print(f"   Response: {response.text[:200]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Error: {response.text}")

            return success, response.json() if response.text and response.status_code < 500 else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_user_registration(self, username, email, password, full_name, role):
        """Test user registration"""
        success, response = self.run_test(
            f"User Registration ({role})",
            "POST",
            "auth/register",
            200,
            data={
                "username": username,
                "email": email,
                "password": password,
                "full_name": full_name,
                "role": role
            }
        )
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.current_user = response.get('user', {})
            return True
        return False

    def test_user_login(self, username, password):
        """Test user login"""
        success, response = self.run_test(
            "User Login",
            "POST",
            "auth/login",
            200,
            data={"username": username, "password": password}
        )
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.current_user = response.get('user', {})
            return True
        return False

    def test_get_current_user(self):
        """Test getting current user profile"""
        success, response = self.run_test(
            "Get Current User Profile",
            "GET",
            "users/me",
            200
        )
        return success

    def test_create_post(self, content, post_type="text", sports_tags=None):
        """Test creating a post"""
        if sports_tags is None:
            sports_tags = []
            
        success, response = self.run_test(
            "Create Post",
            "POST",
            "posts",
            200,
            data={
                "content": content,
                "post_type": post_type,
                "sports_tags": sports_tags
            }
        )
        if success and 'id' in response:
            self.created_post_id = response['id']
            return True
        return False

    def test_get_posts(self):
        """Test getting all posts"""
        success, response = self.run_test(
            "Get All Posts",
            "GET",
            "posts",
            200
        )
        return success, response

    def test_get_user_profile(self, username):
        """Test getting user profile by username"""
        success, response = self.run_test(
            f"Get User Profile ({username})",
            "GET",
            f"users/{username}",
            200
        )
        return success

    def test_get_user_posts(self, user_id):
        """Test getting posts by user ID"""
        success, response = self.run_test(
            f"Get User Posts ({user_id})",
            "GET",
            f"posts/user/{user_id}",
            200
        )
        return success

def main():
    print("🏏 Starting Khel Bhoomi API Tests")
    print("=" * 50)
    
    # Setup
    tester = KhelBhoomiAPITester()
    timestamp = datetime.now().strftime('%H%M%S')
    
    # Test data for different roles
    test_users = [
        {
            "username": f"athlete_{timestamp}",
            "email": f"athlete_{timestamp}@test.com",
            "password": "TestPass123!",
            "full_name": "Test Athlete",
            "role": "athlete"
        },
        {
            "username": f"scout_{timestamp}",
            "email": f"scout_{timestamp}@test.com", 
            "password": "TestPass123!",
            "full_name": "Test Scout",
            "role": "scout"
        },
        {
            "username": f"fan_{timestamp}",
            "email": f"fan_{timestamp}@test.com",
            "password": "TestPass123!",
            "full_name": "Test Fan",
            "role": "fan"
        }
    ]

    print("\n📝 Testing User Registration for All Roles")
    print("-" * 40)
    
    registered_users = []
    for user_data in test_users:
        if tester.test_user_registration(**user_data):
            registered_users.append(user_data)
            print(f"✅ Successfully registered {user_data['role']}: {user_data['username']}")
        else:
            print(f"❌ Failed to register {user_data['role']}: {user_data['username']}")

    if not registered_users:
        print("❌ No users registered successfully, stopping tests")
        return 1

    print(f"\n🔐 Testing Login Flow")
    print("-" * 40)
    
    # Test login with first registered user
    first_user = registered_users[0]
    if not tester.test_user_login(first_user['username'], first_user['password']):
        print("❌ Login failed, stopping tests")
        return 1

    print(f"\n👤 Testing User Profile Endpoints")
    print("-" * 40)
    
    # Test getting current user profile
    tester.test_get_current_user()
    
    # Test getting user profile by username
    tester.test_get_user_profile(first_user['username'])

    print(f"\n📱 Testing Posts Functionality")
    print("-" * 40)
    
    # Test creating posts with different content
    test_posts = [
        {
            "content": "Just finished an amazing training session! 💪 #TrainingDay",
            "post_type": "text",
            "sports_tags": ["training", "fitness"]
        },
        {
            "content": "Great match today! Our team showed incredible teamwork and determination.",
            "post_type": "text", 
            "sports_tags": ["teamwork", "match"]
        },
        {
            "content": "Excited to announce my new personal best in the 100m sprint! 🏃‍♂️",
            "post_type": "achievement",
            "sports_tags": ["sprint", "personal-best"]
        }
    ]
    
    created_posts = 0
    for i, post_data in enumerate(test_posts):
        if tester.test_create_post(**post_data):
            created_posts += 1
            print(f"✅ Created post {i+1}")
        else:
            print(f"❌ Failed to create post {i+1}")

    # Test getting all posts
    success, posts_response = tester.test_get_posts()
    if success:
        posts_count = len(posts_response) if isinstance(posts_response, list) else 0
        print(f"✅ Retrieved {posts_count} posts from feed")

    # Test getting user posts
    if tester.current_user and 'id' in tester.current_user:
        tester.test_get_user_posts(tester.current_user['id'])

    print(f"\n🔍 Testing Different User Roles")
    print("-" * 40)
    
    # Test login with different roles
    for user_data in registered_users[1:]:  # Skip first user as already tested
        print(f"\nTesting {user_data['role']} role:")
        if tester.test_user_login(user_data['username'], user_data['password']):
            tester.test_get_current_user()
            # Create a role-specific post
            role_posts = {
                "scout": "Looking for talented young players for our academy! 🔍 #ScoutingTalent",
                "fan": "What an incredible match! So proud of our team! 🏆 #TeamSpirit"
            }
            if user_data['role'] in role_posts:
                tester.test_create_post(
                    role_posts[user_data['role']], 
                    "text", 
                    [user_data['role'], "community"]
                )

    print(f"\n📊 Test Results Summary")
    print("=" * 50)
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Tests Failed: {tester.tests_run - tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed! API is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the API implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())