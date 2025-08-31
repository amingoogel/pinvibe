#!/usr/bin/env python3
"""
Comprehensive test script for PinVibe User Registration System
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/api/users"
TEST_EMAIL = f"test_{int(time.time())}@example.com"
TEST_USERNAME = f"testuser_{int(time.time())}"

def print_test_result(test_name, success, response=None, expected_status=None):
    """Print formatted test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} - {test_name}")
    if response and not success:
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    elif expected_status and response:
        print(f"   Status: {response.status_code} (Expected: {expected_status})")
    print()

def test_registration_success():
    """Test successful user registration"""
    print("🧪 Testing successful user registration...")
    
    data = {
        "username": TEST_USERNAME,
        "email": TEST_EMAIL,
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
        "bio": "Test user for registration system"
    }
    
    response = requests.post(f"{BASE_URL}/register/", json=data)
    success = response.status_code == 201
    
    if success:
        result = response.json()
        print(f"   User ID: {result.get('user_id')}")
        print(f"   Email: {result.get('email')}")
        print(f"   Message: {result.get('message')}")
    
    print_test_result("Successful Registration", success, response, 201)
    return success

def test_duplicate_username():
    """Test duplicate username validation"""
    print("🧪 Testing duplicate username validation...")
    
    data = {
        "username": TEST_USERNAME,  # Same username as above
        "email": "different@example.com",
        "password": "TestPass123!",
        "password_confirm": "TestPass123!"
    }
    
    response = requests.post(f"{BASE_URL}/register/", json=data)
    success = response.status_code == 400
    
    print_test_result("Duplicate Username Validation", success, response, 400)
    return success

def test_duplicate_email():
    """Test duplicate email validation"""
    print("🧪 Testing duplicate email validation...")
    
    data = {
        "username": "differentuser",
        "email": TEST_EMAIL,  # Same email as above
        "password": "TestPass123!",
        "password_confirm": "TestPass123!"
    }
    
    response = requests.post(f"{BASE_URL}/register/", json=data)
    success = response.status_code == 400
    
    print_test_result("Duplicate Email Validation", success, response, 400)
    return success

def test_weak_password():
    """Test weak password validation"""
    print("🧪 Testing weak password validation...")
    
    data = {
        "username": "weakpassuser",
        "email": "weakpass@example.com",
        "password": "weak",
        "password_confirm": "weak"
    }
    
    response = requests.post(f"{BASE_URL}/register/", json=data)
    success = response.status_code == 400
    
    print_test_result("Weak Password Validation", success, response, 400)
    return success

def test_password_mismatch():
    """Test password confirmation mismatch"""
    print("🧪 Testing password confirmation mismatch...")
    
    data = {
        "username": "mismatchuser",
        "email": "mismatch@example.com",
        "password": "TestPass123!",
        "password_confirm": "DifferentPass123!"
    }
    
    response = requests.post(f"{BASE_URL}/register/", json=data)
    success = response.status_code == 400
    
    print_test_result("Password Mismatch Validation", success, response, 400)
    return success

def test_login_before_verification():
    """Test login attempt before email verification"""
    print("🧪 Testing login before email verification...")
    
    data = {
        "username": TEST_USERNAME,
        "password": "TestPass123!"
    }
    
    response = requests.post(f"{BASE_URL}/login/", json=data)
    success = response.status_code == 400
    
    if success:
        result = response.json()
        print(f"   Error: {result.get('error')}")
        print(f"   Needs Verification: {result.get('needs_verification')}")
    
    print_test_result("Login Before Verification", success, response, 400)
    return success

def test_resend_verification():
    """Test resend verification email"""
    print("🧪 Testing resend verification email...")
    
    data = {"email": TEST_EMAIL}
    
    response = requests.post(f"{BASE_URL}/resend-verification/", json=data)
    success = response.status_code == 200
    
    if success:
        result = response.json()
        print(f"   Message: {result.get('message')}")
    
    print_test_result("Resend Verification Email", success, response, 200)
    return success

def test_invalid_login():
    """Test invalid login credentials"""
    print("🧪 Testing invalid login credentials...")
    
    data = {
        "username": "nonexistentuser",
        "password": "wrongpassword"
    }
    
    response = requests.post(f"{BASE_URL}/login/", json=data)
    success = response.status_code == 400
    
    if success:
        result = response.json()
        print(f"   Error: {result.get('error')}")
    
    print_test_result("Invalid Login Credentials", success, response, 400)
    return success

def run_all_tests():
    """Run all tests and provide summary"""
    print("🚀 Starting PinVibe Registration System Tests")
    print("=" * 60)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Test Email: {TEST_EMAIL}")
    print(f"Test Username: {TEST_USERNAME}")
    print("=" * 60)
    print()
    
    tests = [
        ("Successful Registration", test_registration_success),
        ("Duplicate Username", test_duplicate_username),
        ("Duplicate Email", test_duplicate_email),
        ("Weak Password", test_weak_password),
        ("Password Mismatch", test_password_mismatch),
        ("Login Before Verification", test_login_before_verification),
        ("Resend Verification", test_resend_verification),
        ("Invalid Login", test_invalid_login),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ ERROR - {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Registration system is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
    
    print("=" * 60)
    print("\n📝 Next Steps:")
    print("1. Check your email for verification link")
    print("2. Click the verification link to activate your account")
    print("3. Try logging in again after verification")
    print("4. Test the complete user flow")

if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server!")
        print("Make sure Django is running with: python manage.py runserver")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\nTest completed!") 