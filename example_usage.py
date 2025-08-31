#!/usr/bin/env python3
"""
Example usage of PinVibe User Registration System
This script demonstrates the registration process with email verification
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000/api/users"
TEST_EMAIL = "test@example.com"
TEST_USERNAME = "testuser123"

def print_response(response, title):
    """Print formatted API response"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_registration():
    """Test user registration"""
    print("Testing User Registration System")
    print("="*50)
    
    # Test data
    registration_data = {
        "username": TEST_USERNAME,
        "email": TEST_EMAIL,
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
        "bio": "This is a test user for demonstration"
    }
    
    # 1. Register new user
    print("\n1. Registering new user...")
    response = requests.post(f"{BASE_URL}/register/", json=registration_data)
    print_response(response, "Registration Response")
    
    if response.status_code == 201:
        print("✅ Registration successful!")
        user_data = response.json()
        print(f"User ID: {user_data.get('user_id')}")
        print(f"Email: {user_data.get('email')}")
        print(f"Message: {user_data.get('message')}")
    else:
        print("❌ Registration failed!")
        return False
    
    # 2. Try to login before email verification (should fail)
    print("\n2. Trying to login before email verification...")
    login_data = {
        "username": TEST_USERNAME,
        "password": "TestPass123!"
    }
    response = requests.post(f"{BASE_URL}/login/", json=login_data)
    print_response(response, "Login Before Verification Response")
    
    if response.status_code == 400:
        print("✅ Login correctly blocked before email verification!")
    else:
        print("❌ Login should have been blocked!")
    
    # 3. Test resend verification email
    print("\n3. Testing resend verification email...")
    resend_data = {"email": TEST_EMAIL}
    response = requests.post(f"{BASE_URL}/resend-verification/", json=resend_data)
    print_response(response, "Resend Verification Response")
    
    if response.status_code == 200:
        print("✅ Resend verification email successful!")
    else:
        print("❌ Resend verification email failed!")
    
    # 4. Test duplicate registration (should fail)
    print("\n4. Testing duplicate registration...")
    response = requests.post(f"{BASE_URL}/register/", json=registration_data)
    print_response(response, "Duplicate Registration Response")
    
    if response.status_code == 400:
        print("✅ Duplicate registration correctly blocked!")
    else:
        print("❌ Duplicate registration should have been blocked!")
    
    # 5. Test invalid password
    print("\n5. Testing invalid password...")
    invalid_data = registration_data.copy()
    invalid_data["username"] = "testuser456"
    invalid_data["email"] = "test456@example.com"
    invalid_data["password"] = "weak"
    invalid_data["password_confirm"] = "weak"
    
    response = requests.post(f"{BASE_URL}/register/", json=invalid_data)
    print_response(response, "Invalid Password Response")
    
    if response.status_code == 400:
        print("✅ Invalid password correctly rejected!")
    else:
        print("❌ Invalid password should have been rejected!")
    
    # 6. Test password mismatch
    print("\n6. Testing password mismatch...")
    mismatch_data = registration_data.copy()
    mismatch_data["username"] = "testuser789"
    mismatch_data["email"] = "test789@example.com"
    mismatch_data["password_confirm"] = "DifferentPass123!"
    
    response = requests.post(f"{BASE_URL}/register/", json=mismatch_data)
    print_response(response, "Password Mismatch Response")
    
    if response.status_code == 400:
        print("✅ Password mismatch correctly detected!")
    else:
        print("❌ Password mismatch should have been detected!")
    
    print("\n" + "="*50)
    print("Registration System Test Complete!")
    print("="*50)
    print("\nNote: To complete the email verification process:")
    print("1. Check your email for the verification link")
    print("2. Click the verification link or use the API endpoint")
    print("3. Then try logging in again")
    
    return True

def test_email_verification_simulation():
    """Simulate email verification process"""
    print("\n" + "="*50)
    print("Email Verification Simulation")
    print("="*50)
    
    # This would normally be done by clicking the email link
    # For demonstration, we'll show what the API call would look like
    
    print("\nTo verify email, you would call:")
    print(f"GET {BASE_URL}/verify-email/{{token}}/")
    print("\nWhere {token} is the verification token sent in the email.")
    
    print("\nAfter verification, you can login with:")
    login_data = {
        "username": TEST_USERNAME,
        "password": "TestPass123!"
    }
    print(f"POST {BASE_URL}/login/")
    print(f"Body: {json.dumps(login_data, indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    print("PinVibe User Registration System - Example Usage")
    print("Make sure the Django server is running on localhost:8000")
    print("Press Enter to continue...")
    input()
    
    try:
        test_registration()
        test_email_verification_simulation()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server!")
        print("Make sure Django is running with: python manage.py runserver")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\nExample completed!") 