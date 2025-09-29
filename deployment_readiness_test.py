#!/usr/bin/env python3
"""
Khel Bhoomi Backend API - Render Deployment Readiness Test
Tests all critical deployment requirements for Render hosting platform
"""

import requests
import os
import sys
import json
from datetime import datetime

class RenderDeploymentTester:
    def __init__(self):
        self.base_url = "https://deploy-troubleshoot-15.preview.emergentagent.com"
        self.api_url = f"{self.base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.critical_failures = []
        self.token = None

    def log_test(self, name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
            if details:
                print(f"   {details}")
        else:
            print(f"❌ {name}")
            if details:
                print(f"   {details}")
            self.critical_failures.append(f"{name}: {details}")

    def test_health_endpoint(self):
        """Test 1: Health Check - Test /api/health endpoint"""
        print("\n🏥 DEPLOYMENT TEST 1: Health Check Endpoint")
        print("-" * 50)
        
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    self.log_test("Health endpoint working", True, f"Status: {data.get('status')}, Message: {data.get('message')}")
                    return True
                else:
                    self.log_test("Health endpoint working", False, f"Unexpected response: {data}")
                    return False
            else:
                self.log_test("Health endpoint working", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Health endpoint working", False, f"Connection error: {str(e)}")
            return False

    def test_environment_variables(self):
        """Test 2: Environment Variables - Verify backend can access required env vars"""
        print("\n🔧 DEPLOYMENT TEST 2: Environment Variables Access")
        print("-" * 50)
        
        # Test if backend can connect to MongoDB (indirect env var test)
        try:
            # Try to register a test user - this will fail if MONGO_URL is not accessible
            test_data = {
                "username": f"envtest_{datetime.now().strftime('%H%M%S')}",
                "email": f"envtest_{datetime.now().strftime('%H%M%S')}@test.com",
                "password": "TestPass123!",
                "full_name": "Environment Test User",
                "role": "athlete"
            }
            
            response = requests.post(f"{self.api_url}/auth/signup", json=test_data, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data:
                    self.log_test("MONGO_URL environment variable accessible", True, "Database connection successful")
                    self.log_test("JWT_SECRET_KEY environment variable accessible", True, "JWT token generated successfully")
                    self.token = data['access_token']  # Store for later tests
                    return True
                else:
                    self.log_test("Environment variables accessible", False, "No access token in response")
                    return False
            else:
                self.log_test("Environment variables accessible", False, f"Registration failed: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Environment variables accessible", False, f"Error: {str(e)}")
            return False

    def test_authentication_flow(self):
        """Test 3: Authentication Flow - Test login with demo users"""
        print("\n🔐 DEPLOYMENT TEST 3: Authentication Flow with Demo Users")
        print("-" * 50)
        
        demo_users = [
            {"username": "demo_athlete", "password": "demo123", "role": "athlete"},
            {"username": "demo_scout", "password": "demo123", "role": "scout"},
            {"username": "demo_fan", "password": "demo123", "role": "fan"},
            {"username": "testuser", "password": "password", "role": "fan"}
        ]
        
        successful_logins = 0
        for user in demo_users:
            try:
                response = requests.post(f"{self.api_url}/auth/login", 
                                       json={"username": user["username"], "password": user["password"]}, 
                                       timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if 'access_token' in data and data.get('user', {}).get('role') == user['role']:
                        self.log_test(f"Demo user login: {user['username']}", True, f"Role: {user['role']}")
                        successful_logins += 1
                        if not self.token:  # Store first successful token
                            self.token = data['access_token']
                    else:
                        self.log_test(f"Demo user login: {user['username']}", False, "Invalid response format")
                else:
                    self.log_test(f"Demo user login: {user['username']}", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_test(f"Demo user login: {user['username']}", False, f"Error: {str(e)}")
        
        return successful_logins >= 3  # At least 3 out of 4 should work

    def test_database_connection(self):
        """Test 4: Database Connection - Verify MongoDB Atlas connection"""
        print("\n🗄️ DEPLOYMENT TEST 4: MongoDB Atlas Database Connection")
        print("-" * 50)
        
        try:
            # Test database read operation
            response = requests.get(f"{self.api_url}/posts", timeout=10)
            if response.status_code == 200:
                posts = response.json()
                if isinstance(posts, list):
                    self.log_test("Database read operation", True, f"Retrieved {len(posts)} posts from database")
                    
                    # Test database write operation (if we have a token)
                    if self.token:
                        headers = {'Authorization': f'Bearer {self.token}'}
                        post_data = {
                            "content": "Database connection test post",
                            "post_type": "text",
                            "sports_tags": ["test", "deployment"]
                        }
                        write_response = requests.post(f"{self.api_url}/posts", json=post_data, headers=headers, timeout=10)
                        if write_response.status_code == 200:
                            self.log_test("Database write operation", True, "Successfully created test post")
                            return True
                        else:
                            self.log_test("Database write operation", False, f"HTTP {write_response.status_code}")
                            return False
                    else:
                        self.log_test("Database write operation", False, "No authentication token available")
                        return False
                else:
                    self.log_test("Database connection", False, "Invalid response format")
                    return False
            else:
                self.log_test("Database connection", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Database connection", False, f"Error: {str(e)}")
            return False

    def test_api_endpoints(self):
        """Test 5: API Endpoints - Test key endpoints"""
        print("\n🔗 DEPLOYMENT TEST 5: Key API Endpoints")
        print("-" * 50)
        
        endpoints_passed = 0
        total_endpoints = 0
        
        # Test public endpoints
        public_endpoints = [
            ("GET", "posts", "Get all posts"),
            ("POST", "auth/login", "User login", {"username": "demo_athlete", "password": "demo123"})
        ]
        
        for endpoint_test in public_endpoints:
            total_endpoints += 1
            method, endpoint, description = endpoint_test[:3]
            data = endpoint_test[3] if len(endpoint_test) > 3 else None
            
            try:
                if method == "GET":
                    response = requests.get(f"{self.api_url}/{endpoint}", timeout=10)
                elif method == "POST":
                    response = requests.post(f"{self.api_url}/{endpoint}", json=data, timeout=10)
                
                if response.status_code == 200:
                    self.log_test(f"{description} endpoint", True, f"{method} /{endpoint}")
                    endpoints_passed += 1
                else:
                    self.log_test(f"{description} endpoint", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_test(f"{description} endpoint", False, f"Error: {str(e)}")
        
        # Test authenticated endpoints (if we have a token)
        if self.token:
            headers = {'Authorization': f'Bearer {self.token}'}
            auth_endpoints = [
                ("GET", "users/me", "Get current user profile"),
            ]
            
            for method, endpoint, description in auth_endpoints:
                total_endpoints += 1
                try:
                    response = requests.get(f"{self.api_url}/{endpoint}", headers=headers, timeout=10)
                    if response.status_code == 200:
                        self.log_test(f"{description} endpoint", True, f"{method} /{endpoint}")
                        endpoints_passed += 1
                    else:
                        self.log_test(f"{description} endpoint", False, f"HTTP {response.status_code}")
                except Exception as e:
                    self.log_test(f"{description} endpoint", False, f"Error: {str(e)}")
        
        return endpoints_passed >= (total_endpoints * 0.8)  # 80% success rate

    def test_cors_configuration(self):
        """Test 6: CORS Configuration - Check CORS headers"""
        print("\n🌐 DEPLOYMENT TEST 6: CORS Configuration")
        print("-" * 50)
        
        try:
            # Test preflight request
            headers = {
                'Origin': 'https://deploy-troubleshoot-15.preview.emergentagent.com',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type,Authorization'
            }
            
            response = requests.options(f"{self.api_url}/posts", headers=headers, timeout=10)
            
            # Check for CORS headers in response
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
                'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials')
            }
            
            cors_configured = any(cors_headers.values())
            
            if cors_configured:
                self.log_test("CORS headers present", True, f"Found CORS headers: {[k for k, v in cors_headers.items() if v]}")
                
                # Test actual CORS request
                test_response = requests.get(f"{self.api_url}/health", 
                                           headers={'Origin': 'https://deploy-troubleshoot-15.preview.emergentagent.com'}, 
                                           timeout=10)
                if test_response.status_code == 200:
                    self.log_test("CORS requests working", True, "Cross-origin requests allowed")
                    return True
                else:
                    self.log_test("CORS requests working", False, f"HTTP {test_response.status_code}")
                    return False
            else:
                self.log_test("CORS configuration", False, "No CORS headers found")
                return False
                
        except Exception as e:
            self.log_test("CORS configuration", False, f"Error: {str(e)}")
            return False

    def test_production_readiness(self):
        """Test 7: Production Readiness - Server startup and request handling"""
        print("\n🚀 DEPLOYMENT TEST 7: Production Readiness")
        print("-" * 50)
        
        readiness_checks = 0
        total_checks = 0
        
        # Test 1: Server responds to requests
        total_checks += 1
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                self.log_test("Server responds to requests", True, f"Response time: {response.elapsed.total_seconds():.2f}s")
                readiness_checks += 1
            else:
                self.log_test("Server responds to requests", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Server responds to requests", False, f"Error: {str(e)}")
        
        # Test 2: JSON responses properly formatted
        total_checks += 1
        try:
            response = requests.get(f"{self.api_url}/posts", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("JSON responses properly formatted", True, "Valid JSON structure")
                    readiness_checks += 1
                else:
                    self.log_test("JSON responses properly formatted", False, "Invalid JSON structure")
            else:
                self.log_test("JSON responses properly formatted", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("JSON responses properly formatted", False, f"Error: {str(e)}")
        
        # Test 3: Error handling
        total_checks += 1
        try:
            response = requests.get(f"{self.api_url}/users/nonexistent_user", timeout=10)
            if response.status_code == 404:
                error_data = response.json()
                if 'detail' in error_data:
                    self.log_test("Error handling working", True, "Proper 404 error response")
                    readiness_checks += 1
                else:
                    self.log_test("Error handling working", False, "Invalid error response format")
            else:
                self.log_test("Error handling working", False, f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_test("Error handling working", False, f"Error: {str(e)}")
        
        return readiness_checks >= (total_checks * 0.8)  # 80% success rate

    def run_all_tests(self):
        """Run all deployment readiness tests"""
        print("🏏 KHEL BHOOMI BACKEND - RENDER DEPLOYMENT READINESS TEST")
        print("=" * 60)
        print("Testing backend API for Render hosting platform deployment")
        print("=" * 60)
        
        # Run all tests
        test_results = []
        test_results.append(("Health Check", self.test_health_endpoint()))
        test_results.append(("Environment Variables", self.test_environment_variables()))
        test_results.append(("Authentication Flow", self.test_authentication_flow()))
        test_results.append(("Database Connection", self.test_database_connection()))
        test_results.append(("API Endpoints", self.test_api_endpoints()))
        test_results.append(("CORS Configuration", self.test_cors_configuration()))
        test_results.append(("Production Readiness", self.test_production_readiness()))
        
        # Summary
        print("\n" + "=" * 60)
        print("🎯 DEPLOYMENT READINESS SUMMARY")
        print("=" * 60)
        
        passed_tests = sum(1 for _, result in test_results if result)
        total_tests = len(test_results)
        
        print(f"📊 Overall Test Results:")
        print(f"   Tests Run: {self.tests_run}")
        print(f"   Tests Passed: {self.tests_passed}")
        print(f"   Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"   Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        print(f"\n🎯 Deployment Categories:")
        for test_name, result in test_results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {status} {test_name}")
        
        print(f"\n📈 Deployment Readiness Score: {passed_tests}/{total_tests} ({(passed_tests/total_tests)*100:.1f}%)")
        
        if self.critical_failures:
            print(f"\n⚠️  Critical Issues Found:")
            for failure in self.critical_failures:
                print(f"   • {failure}")
        
        # Final verdict
        if passed_tests >= 6:  # At least 6 out of 7 categories should pass
            print(f"\n🎉 DEPLOYMENT READY: Backend API is ready for Render deployment!")
            return 0
        elif passed_tests >= 4:
            print(f"\n⚠️  DEPLOYMENT WITH CAUTION: Some issues found but core functionality works")
            return 1
        else:
            print(f"\n❌ NOT DEPLOYMENT READY: Critical issues must be resolved before deployment")
            return 2

if __name__ == "__main__":
    tester = RenderDeploymentTester()
    sys.exit(tester.run_all_tests())