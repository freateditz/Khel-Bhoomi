import requests
import json

def test_demo_users():
    """Test all demo users mentioned in the request"""
    base_url = "https://authfix-3.preview.emergentagent.com/api"
    
    # Demo users to test
    demo_users = [
        {"username": "demo_athlete", "password": "demo123"},
        {"username": "demo_scout", "password": "demo123"},
        {"username": "demo_fan", "password": "demo123"},
        {"username": "testuser", "password": "password"}
    ]
    
    print("🔐 Testing Demo Users Login")
    print("=" * 50)
    
    for user in demo_users:
        print(f"\n🔍 Testing login for {user['username']}")
        print("-" * 30)
        
        try:
            response = requests.post(
                f"{base_url}/auth/login",
                json=user,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ SUCCESS: {user['username']} logged in successfully")
                print(f"   Token: {data['access_token'][:50]}...")
                print(f"   User Role: {data['user']['role']}")
                print(f"   Full Name: {data['user']['full_name']}")
                
                # Test protected endpoint with token
                token = data['access_token']
                me_response = requests.get(
                    f"{base_url}/users/me",
                    headers={'Authorization': f'Bearer {token}'}
                )
                
                if me_response.status_code == 200:
                    print(f"✅ Token validation successful for {user['username']}")
                else:
                    print(f"❌ Token validation failed for {user['username']}: {me_response.status_code}")
                    
            else:
                print(f"❌ FAILED: {user['username']} login failed")
                print(f"   Status: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ ERROR: {user['username']} - {str(e)}")

def test_health_check():
    """Test API health check"""
    print("\n🏥 Testing API Health Check")
    print("=" * 50)
    
    # Test /docs endpoint
    try:
        docs_response = requests.get("https://authfix-3.preview.emergentagent.com/docs")
        print(f"📖 /docs endpoint: Status {docs_response.status_code}")
        if docs_response.status_code == 200:
            print("✅ API documentation is accessible")
        else:
            print(f"❌ API documentation not accessible: {docs_response.status_code}")
    except Exception as e:
        print(f"❌ /docs endpoint error: {str(e)}")
    
    # Test basic API endpoint
    try:
        api_response = requests.get("https://authfix-3.preview.emergentagent.com/api/posts")
        print(f"📱 /api/posts endpoint: Status {api_response.status_code}")
        if api_response.status_code == 200:
            posts = api_response.json()
            print(f"✅ API is working - Retrieved {len(posts)} posts")
        else:
            print(f"❌ API endpoint not working: {api_response.status_code}")
    except Exception as e:
        print(f"❌ API endpoint error: {str(e)}")

def test_registration():
    """Test new user registration"""
    print("\n📝 Testing User Registration")
    print("=" * 50)
    
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    test_user = {
        "username": f"newuser_{timestamp}",
        "email": f"newuser_{timestamp}@test.com",
        "password": "testpass123",
        "full_name": "New Test User",
        "role": "fan"
    }
    
    try:
        response = requests.post(
            "https://authfix-3.preview.emergentagent.com/api/auth/register",
            json=test_user,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Registration successful for {test_user['username']}")
            print(f"   User ID: {data['user']['id']}")
            print(f"   Token received: {data['access_token'][:50]}...")
            
            # Test login with new user
            login_response = requests.post(
                "https://authfix-3.preview.emergentagent.com/api/auth/login",
                json={"username": test_user['username'], "password": test_user['password']},
                headers={'Content-Type': 'application/json'}
            )
            
            if login_response.status_code == 200:
                print(f"✅ Login successful with newly registered user")
            else:
                print(f"❌ Login failed with newly registered user: {login_response.status_code}")
                
        else:
            print(f"❌ Registration failed: Status {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")

if __name__ == "__main__":
    test_health_check()
    test_demo_users()
    test_registration()