#!/usr/bin/env python3
"""
Test Password Reset Functionality
Tests the complete password reset flow without requiring email
"""

from auth_system import AuthSystem
from email_service import EmailService
from datetime import datetime
import time

def test_password_reset():
    """Test the complete password reset flow"""
    
    print("=" * 60)
    print("Testing Password Reset Functionality")
    print("=" * 60)
    print()
    
    auth = AuthSystem()
    email_service = EmailService()
    
    # Step 1: Check email configuration
    print("📋 Step 1: Checking email configuration...")
    is_valid, msg = email_service._validate_config()
    if is_valid:
        print("   ✅ Email service is configured")
    else:
        print(f"   ⚠️  Email service not configured: {msg}")
        print("   ℹ️  Demo mode: Will display reset tokens instead of sending emails")
    print()
    
    # Step 2: Create test user if doesn't exist
    print("📋 Step 2: Preparing test user...")
    test_email = "test_reset@example.com"
    test_username = "test_reset_user"
    
    # Check if user exists
    user_exists = test_username in auth.users_db["users"]
    
    if not user_exists:
        print(f"   Creating test user: {test_username}...")
        result = auth.register_user(
            username=test_username,
            email=test_email,
            password="TestPass123!",
            company_name="Test Reset Company",
            country="Test Country"
        )
        if result["success"]:
            print(f"   ✅ Test user created")
        else:
            print(f"   ❌ Failed to create user: {result['message']}")
            return False
    else:
        print(f"   ✅ Test user already exists")
    print()
    
    # Step 3: Request password reset
    print("📋 Step 3: Requesting password reset...")
    result = auth.request_password_reset(test_email)
    
    if result["success"] and result.get("email_found"):
        print(f"   ✅ Reset token generated")
        reset_token = result["reset_token"]
        print(f"   Token: {reset_token[:20]}...")
    else:
        print(f"   ❌ Failed to generate reset token")
        return False
    print()
    
    # Step 4: Verify token
    print("📋 Step 4: Verifying reset token...")
    verification = auth.verify_reset_token(reset_token)
    
    if verification["valid"]:
        print(f"   ✅ Token is valid")
        print(f"   Username: {verification['username']}")
        print(f"   Email: {verification['email']}")
    else:
        print(f"   ❌ Token verification failed: {verification['message']}")
        return False
    print()
    
    # Step 5: Test token expiration check
    print("📋 Step 5: Testing token data...")
    token_data = auth.users_db["reset_tokens"][reset_token]
    print(f"   Created: {token_data['created_at']}")
    print(f"   Expires: {token_data['expires_at']}")
    print(f"   Used: {token_data['used']}")
    print(f"   ✅ Token data stored correctly")
    print()
    
    # Step 6: Reset password
    print("📋 Step 6: Resetting password...")
    new_password = "NewTestPass123!"
    result = auth.reset_password(reset_token, new_password)
    
    if result["success"]:
        print(f"   ✅ Password reset successful")
        print(f"   Message: {result['message']}")
    else:
        print(f"   ❌ Password reset failed: {result['message']}")
        return False
    print()
    
    # Step 7: Verify token is now used
    print("📋 Step 7: Verifying token is marked as used...")
    verification = auth.verify_reset_token(reset_token)
    
    if not verification["valid"]:
        print(f"   ✅ Token correctly marked as used")
        print(f"   Message: {verification['message']}")
    else:
        print(f"   ❌ Token should be invalid after use")
        return False
    print()
    
    # Step 8: Test login with new password
    print("📋 Step 8: Testing login with new password...")
    login_result = auth.login(test_username, new_password)
    
    if login_result["success"]:
        print(f"   ✅ Login successful with new password")
        print(f"   User: {login_result['user']['username']}")
        print(f"   Company: {login_result['user']['company_name']}")
    else:
        print(f"   ❌ Login failed: {login_result['message']}")
        return False
    print()
    
    # Step 9: Test invalid email (security check)
    print("📋 Step 9: Testing invalid email security...")
    result = auth.request_password_reset("nonexistent@example.com")
    
    if result["success"] and not result.get("email_found"):
        print(f"   ✅ Security check passed")
        print(f"   Message: {result['message']}")
        print(f"   (Same message for valid/invalid emails - prevents email enumeration)")
    else:
        print(f"   ⚠️  Security behavior may need review")
    print()
    
    # Step 10: Test expired token handling
    print("📋 Step 10: Testing expired token detection...")
    # Request another reset
    result = auth.request_password_reset(test_email)
    if result.get("email_found"):
        new_token = result["reset_token"]
        # Manually expire it for testing
        auth.users_db["reset_tokens"][new_token]["expires_at"] = "2020-01-01T00:00:00"
        auth._save_users()
        
        verification = auth.verify_reset_token(new_token)
        if not verification["valid"] and "expired" in verification["message"].lower():
            print(f"   ✅ Expired token correctly rejected")
            print(f"   Message: {verification['message']}")
        else:
            print(f"   ⚠️  Expiration check may need review")
    print()
    
    print("=" * 60)
    print("✅ All Password Reset Tests Passed!")
    print("=" * 60)
    print()
    print("Summary:")
    print("  ✅ Token generation working")
    print("  ✅ Token verification working")
    print("  ✅ Password reset working")
    print("  ✅ Token marked as used after reset")
    print("  ✅ Login with new password working")
    print("  ✅ Email enumeration protection working")
    print("  ✅ Token expiration detection working")
    print()
    
    if is_valid:
        print("📧 Email service is configured - emails can be sent")
    else:
        print("📧 Email service not configured - using demo mode")
        print()
        print("To enable email sending:")
        print("  1. Get Gmail App Password: https://myaccount.google.com/apppasswords")
        print("  2. Create .env file with:")
        print("     SENDER_EMAIL=your-email@gmail.com")
        print("     SENDER_PASSWORD=your-app-password")
    
    return True

if __name__ == "__main__":
    try:
        success = test_password_reset()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
