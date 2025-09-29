import requests
import sys
import json
import jwt
from datetime import datetime, timezone

class AuthenticationTester:
    def __init__(self, base_url="https://deploy-troubleshoot-15.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        
        # Test users as specified in the request
        self.test_users = [
            {"username": "demo_athlete", "password": "demo123", "expected_role": "athlete"},
            {"username": "demo_scout", "password": "demo123", "expected_role": "scout"},
            {"username": "demo_fan", "password": "demo123", "expected_role": "fan"},
            {"username": "testuser", "password": "password", "expected_role": None}  # Role unknown
        ]

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

    def test_login_endpoint(self, username, password):
        """Test POST /api/auth/login endpoint"""
        url = f"{self.base_url}/auth/login"
        
        try:
            response = requests.post(
                url,
                json={"username": username, "password": password},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if JWT token is returned
                if 'access_token' in data and 'token_type' in data and 'user' in data:
                    token = data['access_token']
                    user = data['user']
                    
                    # Verify token format (should be JWT)
                    try:
                        # Decode without verification to check structure
                        decoded = jwt.decode(token, options={"verify_signature": False})
                        
                        # Check token has required fields
                        if 'sub' in decoded and 'exp' in decoded:
                            # Check expiration is in future
                            exp_time = datetime.fromtimestamp(decoded['exp'], tz=timezone.utc)
                            current_time = datetime.now(timezone.utc)
                            
                            if exp_time > current_time:
                                self.log_test(
                                    f"Login {username}",
                                    True,
                                    f"Token valid, expires at {exp_time}, user: {user.get('username', 'N/A')}, role: {user.get('role', 'N/A')}"
                                )
                                return True, token, user
                            else:
                                self.log_test(
                                    f"Login {username}",
                                    False,
                                    f"Token expired: {exp_time} <= {current_time}"
                                )
                        else:
                            self.log_test(
                                f"Login {username}",
                                False,
                                f"Token missing required fields (sub/exp): {decoded}"
                            )
                    except Exception as e:
                        self.log_test(
                            f"Login {username}",
                            False,
                            f"Invalid JWT token format: {str(e)}"
                        )
                else:
                    self.log_test(
                        f"Login {username}",
                        False,
                        f"Missing required fields in response: {list(data.keys())}"
                    )
            else:
                self.log_test(
                    f"Login {username}",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                f"Login {username}",
                False,
                f"Request failed: {str(e)}"
            )
            
        return False, None, None

    def test_protected_endpoint(self, token, username):
        """Test GET /api/users/me with JWT token"""
        url = f"{self.base_url}/users/me"
        
        try:
            response = requests.get(
                url,
                headers={
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }
            )
            
            if response.status_code == 200:
                user_data = response.json()
                if 'username' in user_data and user_data['username'] == username:
                    self.log_test(
                        f"Protected endpoint access for {username}",
                        True,
                        f"User profile retrieved: {user_data.get('full_name', 'N/A')}, role: {user_data.get('role', 'N/A')}"
                    )
                    return True, user_data
                else:
                    self.log_test(
                        f"Protected endpoint access for {username}",
                        False,
                        f"Username mismatch: expected {username}, got {user_data.get('username', 'N/A')}"
                    )
            else:
                self.log_test(
                    f"Protected endpoint access for {username}",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                f"Protected endpoint access for {username}",
                False,
                f"Request failed: {str(e)}"
            )
            
        return False, None

    def test_invalid_credentials(self):
        """Test login with invalid credentials"""
        url = f"{self.base_url}/auth/login"
        
        # Test with wrong password
        try:
            response = requests.post(
                url,
                json={"username": "demo_athlete", "password": "wrongpassword"},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 401:
                self.log_test(
                    "Invalid credentials (wrong password)",
                    True,
                    "Correctly returned 401 Unauthorized"
                )
            else:
                self.log_test(
                    "Invalid credentials (wrong password)",
                    False,
                    f"Expected 401, got {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Invalid credentials (wrong password)",
                False,
                f"Request failed: {str(e)}"
            )

        # Test with non-existent user
        try:
            response = requests.post(
                url,
                json={"username": "nonexistent_user", "password": "anypassword"},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 401:
                self.log_test(
                    "Invalid credentials (non-existent user)",
                    True,
                    "Correctly returned 401 Unauthorized"
                )
            else:
                self.log_test(
                    "Invalid credentials (non-existent user)",
                    False,
                    f"Expected 401, got {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Invalid credentials (non-existent user)",
                False,
                f"Request failed: {str(e)}"
            )

    def test_missing_credentials(self):
        """Test login with missing credentials"""
        url = f"{self.base_url}/auth/login"
        
        # Test with missing password
        try:
            response = requests.post(
                url,
                json={"username": "demo_athlete"},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code in [400, 422]:  # 400 Bad Request or 422 Unprocessable Entity
                self.log_test(
                    "Missing credentials (no password)",
                    True,
                    f"Correctly returned {response.status_code}"
                )
            else:
                self.log_test(
                    "Missing credentials (no password)",
                    False,
                    f"Expected 400/422, got {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Missing credentials (no password)",
                False,
                f"Request failed: {str(e)}"
            )

        # Test with missing username
        try:
            response = requests.post(
                url,
                json={"password": "demo123"},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code in [400, 422]:
                self.log_test(
                    "Missing credentials (no username)",
                    True,
                    f"Correctly returned {response.status_code}"
                )
            else:
                self.log_test(
                    "Missing credentials (no username)",
                    False,
                    f"Expected 400/422, got {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Missing credentials (no username)",
                False,
                f"Request failed: {str(e)}"
            )

    def test_invalid_token_access(self):
        """Test protected endpoint with invalid JWT token"""
        url = f"{self.base_url}/users/me"
        
        # Test with malformed token
        try:
            response = requests.get(
                url,
                headers={
                    'Authorization': 'Bearer invalid_token_123',
                    'Content-Type': 'application/json'
                }
            )
            
            if response.status_code == 401:
                self.log_test(
                    "Invalid JWT token access",
                    True,
                    "Correctly rejected invalid token with 401"
                )
            else:
                self.log_test(
                    "Invalid JWT token access",
                    False,
                    f"Expected 401, got {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Invalid JWT token access",
                False,
                f"Request failed: {str(e)}"
            )

        # Test with no token
        try:
            response = requests.get(
                url,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code in [401, 403]:
                self.log_test(
                    "No JWT token access",
                    True,
                    f"Correctly rejected request without token with {response.status_code}"
                )
            else:
                self.log_test(
                    "No JWT token access",
                    False,
                    f"Expected 401/403, got {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "No JWT token access",
                False,
                f"Request failed: {str(e)}"
            )

    def run_comprehensive_auth_tests(self):
        """Run all authentication tests"""
        print("🔐 Khel Bhoomi Authentication System Testing")
        print("=" * 60)
        print(f"Backend URL: {self.base_url}")
        print()

        # Test 1: Login with all dummy users
        print("📝 Testing Login with All Dummy Users")
        print("-" * 40)
        
        successful_logins = []
        for user in self.test_users:
            success, token, user_data = self.test_login_endpoint(user["username"], user["password"])
            if success:
                successful_logins.append({
                    "username": user["username"],
                    "token": token,
                    "user_data": user_data
                })

        print()

        # Test 2: Test protected endpoints with valid tokens
        print("🔒 Testing Protected Endpoints with Valid Tokens")
        print("-" * 40)
        
        for login_info in successful_logins:
            self.test_protected_endpoint(login_info["token"], login_info["username"])

        print()

        # Test 3: Test authentication error cases
        print("⚠️  Testing Authentication Error Cases")
        print("-" * 40)
        
        self.test_invalid_credentials()
        self.test_missing_credentials()
        self.test_invalid_token_access()

        print()

        # Test 4: JWT Token validation
        print("🔍 JWT Token Validation Details")
        print("-" * 40)
        
        for login_info in successful_logins:
            token = login_info["token"]
            username = login_info["username"]
            
            try:
                # Decode token without verification to inspect
                decoded = jwt.decode(token, options={"verify_signature": False})
                exp_time = datetime.fromtimestamp(decoded['exp'], tz=timezone.utc)
                issued_time = datetime.fromtimestamp(decoded.get('iat', decoded['exp'] - 1800), tz=timezone.utc)
                
                print(f"✅ {username} token details:")
                print(f"   Subject: {decoded.get('sub', 'N/A')}")
                print(f"   Issued: {issued_time}")
                print(f"   Expires: {exp_time}")
                print(f"   Valid for: {(exp_time - datetime.now(timezone.utc)).total_seconds() / 60:.1f} minutes")
                
            except Exception as e:
                print(f"❌ {username} token analysis failed: {str(e)}")

        print()

        # Summary
        print("📊 Authentication Test Results")
        print("=" * 60)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {len(self.failed_tests)}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.failed_tests:
            print(f"\n❌ Failed Tests:")
            for test in self.failed_tests:
                print(f"   - {test}")
        
        print()
        
        if len(self.failed_tests) == 0:
            print("🎉 All authentication tests passed! The system is ready for frontend login.")
            return True
        else:
            print("⚠️  Some authentication tests failed. Please review the issues above.")
            return False

def main():
    tester = AuthenticationTester()
    success = tester.run_comprehensive_auth_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())