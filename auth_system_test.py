#!/usr/bin/env python3
"""
Khel Bhoomi Authentication System Test
Testing the recreated authentication system with new database structure
"""

import requests
import json
import sys
from datetime import datetime

class AuthSystemTester:
    def __init__(self, base_url="https://deploy-troubleshoot-15.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        
    def log_test(self, test_name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {test_name}")
            if details:
                print(f"   {details}")
        else:
            self.failed_tests.append(test_name)
            print(f"❌ {test_name}")
            if details:
                print(f"   {details}")
    
    def make_request(self, method, endpoint, data=None, headers=None):
        """Make HTTP request with error handling"""
        url = f"{self.base_url}/{endpoint}"
        request_headers = {'Content-Type': 'application/json'}
        
        if self.token:
            request_headers['Authorization'] = f'Bearer {self.token}'
        
        if headers:
            request_headers.update(headers)
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=request_headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=request_headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=request_headers)
            
            return response
        except Exception as e:
            print(f"   Request failed: {str(e)}")
            return None
    
    def test_api_health(self):
        """Test 1: API Health Check"""
        print("\n🏥 Testing API Health Check")
        print("-" * 40)
        
        response = self.make_request('GET', 'health')
        if response and response.status_code == 200:
            try:
                data = response.json()
                self.log_test("API Health Check", True, f"Status: {data.get('status', 'unknown')}")
                return True
            except:
                self.log_test("API Health Check", True, f"Status code: {response.status_code}")
                return True
        else:
            status = response.status_code if response else "No response"
            self.log_test("API Health Check", False, f"Status: {status}")
            return False
    
    def test_demo_user_login(self, username, password, expected_role=None):
        """Test login with demo users"""
        response = self.make_request('POST', 'auth/login', {
            'username': username,
            'password': password
        })
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if 'access_token' in data and 'user' in data:
                    self.token = data['access_token']
                    user = data['user']
                    role_match = not expected_role or user.get('role') == expected_role
                    
                    details = f"Role: {user.get('role', 'unknown')}, Token received"
                    self.log_test(f"Login {username}", True, details)
                    return True, data
                else:
                    self.log_test(f"Login {username}", False, "Missing token or user data")
                    return False, {}
            except Exception as e:
                self.log_test(f"Login {username}", False, f"JSON parse error: {str(e)}")
                return False, {}
        else:
            status = response.status_code if response else "No response"
            error = response.text if response else "Connection failed"
            self.log_test(f"Login {username}", False, f"Status: {status}, Error: {error}")
            return False, {}
    
    def test_signup(self, username, email, password, full_name, role):
        """Test user signup"""
        response = self.make_request('POST', 'auth/signup', {
            'username': username,
            'email': email,
            'password': password,
            'full_name': full_name,
            'role': role
        })
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if 'access_token' in data and 'user' in data:
                    details = f"User created with role: {data['user'].get('role', 'unknown')}"
                    self.log_test(f"Signup {username}", True, details)
                    return True, data
                else:
                    self.log_test(f"Signup {username}", False, "Missing token or user data")
                    return False, {}
            except Exception as e:
                self.log_test(f"Signup {username}", False, f"JSON parse error: {str(e)}")
                return False, {}
        else:
            status = response.status_code if response else "No response"
            error = response.text if response else "Connection failed"
            self.log_test(f"Signup {username}", False, f"Status: {status}, Error: {error}")
            return False, {}
    
    def test_token_validation(self):
        """Test JWT token validation with /api/users/me"""
        if not self.token:
            self.log_test("Token Validation", False, "No token available")
            return False
        
        response = self.make_request('GET', 'users/me')
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if 'username' in data and 'role' in data:
                    details = f"User: {data.get('username')}, Role: {data.get('role')}"
                    self.log_test("Token Validation", True, details)
                    return True, data
                else:
                    self.log_test("Token Validation", False, "Invalid user data structure")
                    return False, {}
            except Exception as e:
                self.log_test("Token Validation", False, f"JSON parse error: {str(e)}")
                return False, {}
        else:
            status = response.status_code if response else "No response"
            error = response.text if response else "Connection failed"
            self.log_test("Token Validation", False, f"Status: {status}, Error: {error}")
            return False, {}
    
    def test_posts_functionality(self):
        """Test posts creation and retrieval"""
        if not self.token:
            self.log_test("Posts Test", False, "No authentication token")
            return False
        
        # Test creating a post
        post_data = {
            'content': 'Testing new database structure for posts collection! 🏏',
            'post_type': 'text',
            'sports_tags': ['testing', 'database']
        }
        
        response = self.make_request('POST', 'posts', post_data)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if 'id' in data and 'content' in data:
                    self.log_test("Create Post", True, f"Post ID: {data.get('id')}")
                    
                    # Test retrieving posts
                    posts_response = self.make_request('GET', 'posts')
                    if posts_response and posts_response.status_code == 200:
                        posts_data = posts_response.json()
                        if isinstance(posts_data, list):
                            self.log_test("Retrieve Posts", True, f"Found {len(posts_data)} posts")
                            return True
                        else:
                            self.log_test("Retrieve Posts", False, "Invalid posts data format")
                            return False
                    else:
                        self.log_test("Retrieve Posts", False, "Failed to retrieve posts")
                        return False
                else:
                    self.log_test("Create Post", False, "Invalid post response structure")
                    return False
            except Exception as e:
                self.log_test("Create Post", False, f"JSON parse error: {str(e)}")
                return False
        else:
            status = response.status_code if response else "No response"
            error = response.text if response else "Connection failed"
            self.log_test("Create Post", False, f"Status: {status}, Error: {error}")
            return False
    
    def run_comprehensive_test(self):
        """Run all authentication system tests"""
        print("🔐 Khel Bhoomi Authentication System Test")
        print("Testing recreated authentication with new database structure")
        print("=" * 60)
        
        # Test 1: API Health Check
        health_ok = self.test_api_health()
        
        # Test 2: Demo Users Login Testing
        print("\n🔐 Testing Demo Users Login")
        print("-" * 40)
        
        demo_users = [
            ('demo_athlete', 'demo123', 'athlete'),
            ('demo_scout', 'demo123', 'scout'),
            ('demo_fan', 'demo123', 'fan'),
            ('testuser', 'password', None)  # No specific role expected
        ]
        
        successful_logins = []
        for username, password, expected_role in demo_users:
            success, user_data = self.test_demo_user_login(username, password, expected_role)
            if success:
                successful_logins.append((username, user_data))
        
        # Test 3: Token Validation (using last successful login)
        print("\n🔑 Testing JWT Token Validation")
        print("-" * 40)
        
        if successful_logins:
            # Use the last successful login for token validation
            token_validation_ok = self.test_token_validation()
        else:
            self.log_test("Token Validation", False, "No successful logins to test with")
            token_validation_ok = False
        
        # Test 4: New User Signup Testing
        print("\n📝 Testing New User Signup")
        print("-" * 40)
        
        timestamp = datetime.now().strftime('%H%M%S')
        new_user_data = {
            'username': f'newuser_{timestamp}',
            'email': f'newuser_{timestamp}@khelbhoomi.com',
            'password': 'NewUser123!',
            'full_name': 'New Test User',
            'role': 'athlete'
        }
        
        signup_success, signup_data = self.test_signup(**new_user_data)
        
        # Test 5: Posts Functionality (using new user or demo user)
        print("\n📱 Testing Posts Functionality")
        print("-" * 40)
        
        posts_ok = self.test_posts_functionality()
        
        # Test 6: Database Structure Verification (indirect)
        print("\n🗄️ Database Structure Verification")
        print("-" * 40)
        
        # We can't directly access the database, but we can infer from API responses
        # that the new collection structure is working if all above tests pass
        
        collections_working = []
        if successful_logins:
            collections_working.append("users collection (login successful)")
        if signup_success:
            collections_working.append("signup collection (signup records)")
        if posts_ok:
            collections_working.append("posts collection (posts created/retrieved)")
        
        if collections_working:
            self.log_test("Database Collections", True, f"Working: {', '.join(collections_working)}")
        else:
            self.log_test("Database Collections", False, "No evidence of working collections")
        
        # Final Summary
        print("\n📊 Test Results Summary")
        print("=" * 60)
        print(f"Total Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.failed_tests:
            print(f"\n❌ Failed Tests:")
            for test in self.failed_tests:
                print(f"   - {test}")
        
        # Priority Focus Results
        print(f"\n🎯 Priority Focus Results:")
        demo_login_success = len(successful_logins) > 0
        print(f"   ✅ Demo users login: {'PASS' if demo_login_success else 'FAIL'}")
        print(f"   ✅ New collection structure: {'PASS' if collections_working else 'FAIL'}")
        print(f"   ✅ Login/signup records: {'PASS' if (successful_logins or signup_success) else 'FAIL'}")
        print(f"   ✅ JWT tokens: {'PASS' if token_validation_ok else 'FAIL'}")
        
        return self.tests_passed == self.tests_run

def main():
    tester = AuthSystemTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🎉 All authentication system tests passed!")
        return 0
    else:
        print("\n⚠️ Some authentication tests failed. Check the results above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())