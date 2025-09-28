import requests
import sys
import json
from datetime import datetime

class DummyLoginTester:
    def __init__(self, base_url="https://authfix-3.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        
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

            self.test_results.append({
                'name': name,
                'success': success,
                'status_code': response.status_code,
                'expected_status': expected_status,
                'response': response.json() if response.text and response.status_code < 500 else {}
            })

            return success, response.json() if response.text and response.status_code < 500 else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.test_results.append({
                'name': name,
                'success': False,
                'error': str(e)
            })
            return False, {}

    def test_dummy_login(self, username, password, expected_role):
        """Test login with dummy credentials"""
        success, response = self.run_test(
            f"Dummy Login - {username} ({expected_role})",
            "POST",
            "auth/login",
            200,
            data={"username": username, "password": password}
        )
        
        if success:
            # Verify response structure
            required_fields = ['access_token', 'token_type', 'user']
            missing_fields = [field for field in required_fields if field not in response]
            
            if missing_fields:
                print(f"❌ Missing required fields: {missing_fields}")
                return False, None
            
            # Verify token type
            if response.get('token_type') != 'bearer':
                print(f"❌ Expected token_type 'bearer', got '{response.get('token_type')}'")
                return False, None
            
            # Verify user data
            user = response.get('user', {})
            if user.get('username') != username:
                print(f"❌ Username mismatch: expected {username}, got {user.get('username')}")
                return False, None
            
            if user.get('role') != expected_role:
                print(f"❌ Role mismatch: expected {expected_role}, got {user.get('role')}")
                return False, None
            
            print(f"✅ Login successful for {username}")
            print(f"   User ID: {user.get('id')}")
            print(f"   Full Name: {user.get('full_name')}")
            print(f"   Role: {user.get('role')}")
            print(f"   Email: {user.get('email')}")
            
            return True, response.get('access_token')
        
        return False, None

    def test_authenticated_endpoint(self, token, endpoint_name, endpoint):
        """Test an authenticated endpoint with JWT token"""
        headers = {'Authorization': f'Bearer {token}'}
        success, response = self.run_test(
            endpoint_name,
            "GET",
            endpoint,
            200,
            headers=headers
        )
        return success, response

    def test_invalid_credentials(self):
        """Test login with invalid credentials"""
        success, response = self.run_test(
            "Invalid Credentials Test",
            "POST",
            "auth/login",
            401,
            data={"username": "invalid_user", "password": "wrong_password"}
        )
        return success

def main():
    print("🏏 Testing Khel Bhoomi Dummy Login Functionality")
    print("=" * 60)
    
    tester = DummyLoginTester()
    
    # Dummy user credentials to test
    dummy_users = [
        {"username": "demo_athlete", "password": "demo123", "role": "athlete"},
        {"username": "demo_scout", "password": "demo123", "role": "scout"},
        {"username": "demo_fan", "password": "demo123", "role": "fan"},
        {"username": "testuser", "password": "password", "role": "fan"}
    ]
    
    print("\n🔐 Testing Dummy User Logins")
    print("-" * 40)
    
    successful_logins = []
    
    # Test each dummy user login
    for user in dummy_users:
        success, token = tester.test_dummy_login(
            user["username"], 
            user["password"], 
            user["role"]
        )
        
        if success and token:
            successful_logins.append({
                "username": user["username"],
                "role": user["role"],
                "token": token
            })
    
    print(f"\n👤 Testing Authenticated Endpoints")
    print("-" * 40)
    
    # Test authenticated endpoints with each successful login
    for login in successful_logins:
        print(f"\nTesting with {login['username']} ({login['role']}):")
        
        # Test /api/users/me endpoint
        tester.test_authenticated_endpoint(
            login['token'],
            f"Get Current User - {login['username']}",
            "users/me"
        )
    
    print(f"\n📱 Testing Posts Endpoint")
    print("-" * 40)
    
    # Test posts endpoint (should work without authentication)
    success, posts_response = tester.run_test(
        "Get All Posts",
        "GET", 
        "posts",
        200
    )
    
    if success and isinstance(posts_response, list):
        print(f"✅ Posts endpoint returned {len(posts_response)} posts")
        if len(posts_response) > 0:
            print("   Sample post structure:")
            sample_post = posts_response[0]
            for key in ['id', 'username', 'user_role', 'content', 'post_type', 'created_at']:
                if key in sample_post:
                    print(f"     {key}: {sample_post[key]}")
    
    print(f"\n❌ Testing Invalid Credentials")
    print("-" * 40)
    
    # Test invalid credentials
    tester.test_invalid_credentials()
    
    print(f"\n📊 Test Results Summary")
    print("=" * 60)
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Tests Failed: {tester.tests_run - tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    print(f"\n🔍 Detailed Results:")
    for result in tester.test_results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"  {status} - {result['name']}")
        if not result['success'] and 'error' in result:
            print(f"    Error: {result['error']}")
    
    if tester.tests_passed == tester.tests_run:
        print("\n🎉 All dummy login tests passed! Authentication is working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the authentication implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())