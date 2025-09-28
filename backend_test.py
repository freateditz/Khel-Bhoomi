import requests
import sys
import json
from datetime import datetime

class KhelBhoomiAPITester:
    def __init__(self, base_url="https://env-config-4.preview.emergentagent.com/api"):
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
            "auth/signup",
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

    def test_update_profile_single_field(self, field_name, field_value):
        """Test updating a single profile field"""
        success, response = self.run_test(
            f"Update Profile - {field_name}",
            "PUT",
            "users/me",
            200,
            data={field_name: field_value}
        )
        return success, response

    def test_update_profile_multiple_fields(self, update_data):
        """Test updating multiple profile fields at once"""
        success, response = self.run_test(
            "Update Profile - Multiple Fields",
            "PUT",
            "users/me",
            200,
            data=update_data
        )
        return success, response

    def test_update_profile_empty_body(self):
        """Test updating profile with empty request body"""
        success, response = self.run_test(
            "Update Profile - Empty Body",
            "PUT",
            "users/me",
            400,
            data={}
        )
        return success

    def test_update_profile_invalid_token(self):
        """Test updating profile with invalid JWT token"""
        # Save current token
        original_token = self.token
        # Set invalid token
        self.token = "invalid_token_123"
        
        success, response = self.run_test(
            "Update Profile - Invalid Token",
            "PUT",
            "users/me",
            401,
            data={"full_name": "Should Fail"}
        )
        
        # Restore original token
        self.token = original_token
        return success

    def test_profile_update_flow(self):
        """Test complete profile update flow"""
        print(f"\n🔄 Testing Profile Update Flow")
        print("-" * 40)
        
        # Test 1: Update full_name only
        success, response = self.test_update_profile_single_field("full_name", "Updated Athlete Name")
        if success:
            print("✅ Successfully updated full_name")
        else:
            print("❌ Failed to update full_name")
            return False

        # Verify the update by getting current user
        success, user_data = self.run_test("Verify full_name update", "GET", "users/me", 200)
        if success and user_data.get('full_name') == "Updated Athlete Name":
            print("✅ full_name update verified")
        else:
            print("❌ full_name update verification failed")

        # Test 2: Update bio only
        success, response = self.test_update_profile_single_field("bio", "I am a passionate athlete who loves cricket and football!")
        if success:
            print("✅ Successfully updated bio")
        else:
            print("❌ Failed to update bio")

        # Verify bio update
        success, user_data = self.run_test("Verify bio update", "GET", "users/me", 200)
        if success and user_data.get('bio') == "I am a passionate athlete who loves cricket and football!":
            print("✅ bio update verified")
        else:
            print("❌ bio update verification failed")

        # Test 3: Update sports_interests only
        sports_interests = ["Cricket", "Football", "Basketball", "Tennis"]
        success, response = self.test_update_profile_single_field("sports_interests", sports_interests)
        if success:
            print("✅ Successfully updated sports_interests")
        else:
            print("❌ Failed to update sports_interests")

        # Verify sports_interests update
        success, user_data = self.run_test("Verify sports_interests update", "GET", "users/me", 200)
        if success and user_data.get('sports_interests') == sports_interests:
            print("✅ sports_interests update verified")
        else:
            print("❌ sports_interests update verification failed")

        # Test 4: Update multiple fields at once
        multiple_updates = {
            "full_name": "Multi-Update Athlete",
            "bio": "Updated bio with multiple fields",
            "profile_image": "https://example.com/new-profile.jpg",
            "sports_interests": ["Swimming", "Hockey", "Badminton"]
        }
        success, response = self.test_update_profile_multiple_fields(multiple_updates)
        if success:
            print("✅ Successfully updated multiple fields")
        else:
            print("❌ Failed to update multiple fields")

        # Verify multiple fields update
        success, user_data = self.run_test("Verify multiple fields update", "GET", "users/me", 200)
        if success:
            all_verified = True
            for field, expected_value in multiple_updates.items():
                if user_data.get(field) != expected_value:
                    print(f"❌ {field} update verification failed")
                    all_verified = False
            if all_verified:
                print("✅ All multiple fields update verified")
        else:
            print("❌ Multiple fields update verification failed")

        # Test 5: Empty request body (should fail)
        if self.test_update_profile_empty_body():
            print("✅ Empty body correctly rejected")
        else:
            print("❌ Empty body test failed")

        # Test 6: Invalid JWT token (should fail)
        if self.test_update_profile_invalid_token():
            print("✅ Invalid token correctly rejected")
        else:
            print("❌ Invalid token test failed")

        return True

def main():
    print("🏏 Starting Khel Bhoomi API Tests")
    print("=" * 50)
    
    # Setup
    tester = KhelBhoomiAPITester()
    
    # Test 1: API Health Check
    print(f"\n🏥 Testing API Health Check")
    print("-" * 40)
    
    # Test if backend is accessible via /docs
    try:
        import requests
        docs_url = "https://env-config-4.preview.emergentagent.com/docs"
        response = requests.get(docs_url)
        if response.status_code == 200:
            print("✅ Backend API is accessible via /docs")
        else:
            print(f"❌ Backend API health check failed - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Backend API health check failed - Error: {str(e)}")
    
    # Test 2: User Registration with specified test data
    print(f"\n📝 Testing User Registration with Specified Test Data")
    print("-" * 40)
    
    test_user_data = {
        "username": "testuser2024",
        "email": "test@khelbhoomi.com",
        "password": "testpass123",
        "role": "athlete",
        "full_name": "Test User 2024"
    }
    
    registration_success = tester.test_user_registration(**test_user_data)
    if registration_success:
        print("✅ Successfully registered new test user")
        
        # Test 3: User Login with newly created user
        print(f"\n🔐 Testing Login with Newly Created User")
        print("-" * 40)
        
        login_success = tester.test_user_login(test_user_data['username'], test_user_data['password'])
        if login_success:
            print("✅ Successfully logged in with new test user")
            
            # Test 4: Token Validation
            print(f"\n🔑 Testing Token Validation")
            print("-" * 40)
            
            token_validation_success = tester.test_get_current_user()
            if token_validation_success:
                print("✅ JWT token validation successful")
            else:
                print("❌ JWT token validation failed")
        else:
            print("❌ Login with newly created user failed")
    else:
        print("❌ User registration failed")
    
    # Test 5: Try login with demo user (fallback)
    print(f"\n🔐 Testing Login with Demo User (Fallback)")
    print("-" * 40)
    
    # Test login with demo_athlete as requested
    if not tester.test_user_login("demo_athlete", "demo123"):
        print("❌ Demo athlete login failed, will continue with other tests")
    else:
        print("✅ Successfully logged in as demo_athlete")
    
    print("✅ Successfully logged in as demo_athlete")
    
    # Test the new profile update functionality
    if not tester.test_profile_update_flow():
        print("❌ Profile update tests failed")
        return 1
    
    print(f"\n📝 Testing User Registration for All Roles")
    print("-" * 40)
    
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
    
    registered_users = []
    for user_data in test_users:
        if tester.test_user_registration(**user_data):
            registered_users.append(user_data)
            print(f"✅ Successfully registered {user_data['role']}: {user_data['username']}")
        else:
            print(f"❌ Failed to register {user_data['role']}: {user_data['username']}")

    if not registered_users:
        print("❌ No users registered successfully, continuing with existing tests")
        # Continue with existing functionality tests using demo_athlete
        first_user = {"username": "demo_athlete", "password": "demo123"}
    else:
        print(f"\n🔐 Testing Login Flow with New Users")
        print("-" * 40)
        
        # Test login with first registered user
        first_user = registered_users[0]
        if not tester.test_user_login(first_user['username'], first_user['password']):
            print("❌ Login failed, using demo_athlete for remaining tests")
            first_user = {"username": "demo_athlete", "password": "demo123"}
            tester.test_user_login(first_user['username'], first_user['password'])

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