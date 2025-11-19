"""
PowerAI Authentication and User Management System
Handles user registration, login, company management, and password reset
"""
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)

class AuthSystem:
    """Authentication system for PowerAI"""
    
    def __init__(self, data_file: str = "users_data.json"):
        self.data_file = Path(data_file)
        self.users_db = self._load_users()
        # Initialize reset tokens storage if not exists
        if "reset_tokens" not in self.users_db:
            self.users_db["reset_tokens"] = {}
    
    def _load_users(self) -> Dict:
        """Load users from JSON file"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading users: {e}")
                return {"users": {}, "companies": {}, "reset_tokens": {}}
        return {"users": {}, "companies": {}, "reset_tokens": {}}
    
    def _save_users(self):
        """Save users to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.users_db, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving users: {e}")
    
    def _hash_password(self, password: str, salt: str = None) -> tuple:
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', 
                                       password.encode('utf-8'),
                                       salt.encode('utf-8'),
                                       100000)
        return pwd_hash.hex(), salt
    
    def register_user(self, username: str, email: str, password: str, 
                     company_name: str, country: str, role: str = "admin") -> Dict:
        """Register a new user and company"""
        # Validate inputs
        if not all([username, email, password, company_name, country]):
            return {"success": False, "message": "All fields are required"}
        
        if username in self.users_db["users"]:
            return {"success": False, "message": "Username already exists"}
        
        if email in [u["email"] for u in self.users_db["users"].values()]:
            return {"success": False, "message": "Email already registered"}
        
        # Create company ID
        company_id = company_name.lower().replace(' ', '_').replace('-', '_')
        
        if company_id in self.users_db["companies"]:
            return {"success": False, "message": "Company name already taken"}
        
        # Hash password
        pwd_hash, salt = self._hash_password(password)
        
        # Create user
        user_id = secrets.token_hex(8)
        self.users_db["users"][username] = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "password_hash": pwd_hash,
            "salt": salt,
            "company_id": company_id,
            "role": role,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "is_active": True
        }
        
        # Create company with free tier
        self.users_db["companies"][company_id] = {
            "company_id": company_id,
            "company_name": company_name,
            "country": country,
            "subscription_tier": "free",
            "created_at": datetime.now().isoformat(),
            "owner": username,
            "users": [username],
            "settings": {
                "currency": "USD",
                "timezone": "UTC",
                "renewable_types": ["solar", "wind", "hydro"],
                "grid_capacity_mw": 100
            }
        }
        
        self._save_users()
        
        return {
            "success": True,
            "message": "Registration successful! You have a 14-day free trial.",
            "user_id": user_id,
            "company_id": company_id
        }
    
    def login(self, username: str, password: str) -> Dict:
        """Authenticate user"""
        if username not in self.users_db["users"]:
            return {"success": False, "message": "Invalid username or password"}
        
        user = self.users_db["users"][username]
        
        if not user["is_active"]:
            return {"success": False, "message": "Account is deactivated"}
        
        # Verify password
        pwd_hash, _ = self._hash_password(password, user["salt"])
        
        if pwd_hash != user["password_hash"]:
            return {"success": False, "message": "Invalid username or password"}
        
        # Update last login
        user["last_login"] = datetime.now().isoformat()
        self._save_users()
        
        # Get company info
        company = self.users_db["companies"][user["company_id"]]
        
        return {
            "success": True,
            "message": "Login successful",
            "user": {
                "username": username,
                "email": user["email"],
                "role": user["role"],
                "company_id": user["company_id"],
                "company_name": company["company_name"],
                "subscription_tier": company["subscription_tier"]
            }
        }
    
    def get_user_info(self, username: str) -> Optional[Dict]:
        """Get user information"""
        if username not in self.users_db["users"]:
            return None
        
        user = self.users_db["users"][username]
        company = self.users_db["companies"][user["company_id"]]
        
        return {
            "username": username,
            "email": user["email"],
            "role": user["role"],
            "company_id": user["company_id"],
            "company_name": company["company_name"],
            "country": company["country"],
            "subscription_tier": company["subscription_tier"],
            "created_at": user["created_at"],
            "last_login": user["last_login"]
        }
    
    def get_company_info(self, company_id: str) -> Optional[Dict]:
        """Get company information"""
        if company_id not in self.users_db["companies"]:
            return None
        return self.users_db["companies"][company_id]
    
    def update_subscription(self, company_id: str, tier: str) -> bool:
        """Update company subscription tier"""
        if company_id not in self.users_db["companies"]:
            return False
        
        self.users_db["companies"][company_id]["subscription_tier"] = tier
        self.users_db["companies"][company_id]["upgraded_at"] = datetime.now().isoformat()
        self._save_users()
        return True
    
    def get_all_companies(self) -> List[Dict]:
        """Get all registered companies (admin function)"""
        return [
            {
                "company_id": cid,
                "company_name": info["company_name"],
                "country": info["country"],
                "subscription_tier": info["subscription_tier"],
                "created_at": info["created_at"],
                "user_count": len(info["users"])
            }
            for cid, info in self.users_db["companies"].items()
        ]
    
    def request_password_reset(self, email: str) -> Dict:
        """Generate password reset token for user"""
        # Find user by email
        username = None
        for uname, user in self.users_db["users"].items():
            if user["email"].lower() == email.lower():
                username = uname
                break
        
        if not username:
            # Don't reveal if email exists for security
            return {
                "success": True,
                "message": "If this email is registered, you will receive a password reset link.",
                "email_found": False
            }
        
        # Generate secure reset token
        reset_token = secrets.token_urlsafe(32)
        
        # Store token with expiration (1 hour)
        self.users_db["reset_tokens"][reset_token] = {
            "username": username,
            "email": email,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=1)).isoformat(),
            "used": False
        }
        
        self._save_users()
        
        return {
            "success": True,
            "message": "If this email is registered, you will receive a password reset link.",
            "email_found": True,
            "username": username,
            "reset_token": reset_token
        }
    
    def verify_reset_token(self, token: str) -> Dict:
        """Verify if reset token is valid"""
        if token not in self.users_db["reset_tokens"]:
            return {"valid": False, "message": "Invalid or expired reset token"}
        
        token_data = self.users_db["reset_tokens"][token]
        
        # Check if already used
        if token_data["used"]:
            return {"valid": False, "message": "This reset link has already been used"}
        
        # Check if expired
        expires_at = datetime.fromisoformat(token_data["expires_at"])
        if datetime.now() > expires_at:
            return {"valid": False, "message": "This reset link has expired. Please request a new one."}
        
        return {
            "valid": True,
            "username": token_data["username"],
            "email": token_data["email"]
        }
    
    def reset_password(self, token: str, new_password: str) -> Dict:
        """Reset user password using token"""
        # Verify token
        verification = self.verify_reset_token(token)
        if not verification["valid"]:
            return {"success": False, "message": verification["message"]}
        
        username = verification["username"]
        
        # Update password
        pwd_hash, salt = self._hash_password(new_password)
        self.users_db["users"][username]["password_hash"] = pwd_hash
        self.users_db["users"][username]["salt"] = salt
        
        # Mark token as used
        self.users_db["reset_tokens"][token]["used"] = True
        self.users_db["reset_tokens"][token]["used_at"] = datetime.now().isoformat()
        
        self._save_users()
        
        return {
            "success": True,
            "message": "Password reset successful! You can now login with your new password.",
            "username": username
        }
    
    def cleanup_expired_tokens(self):
        """Remove expired reset tokens"""
        current_time = datetime.now()
        tokens_to_remove = []
        
        for token, data in self.users_db["reset_tokens"].items():
            expires_at = datetime.fromisoformat(data["expires_at"])
            # Remove tokens older than 24 hours
            if current_time > expires_at + timedelta(hours=23):
                tokens_to_remove.append(token)
        
        for token in tokens_to_remove:
            del self.users_db["reset_tokens"][token]
        
        if tokens_to_remove:
            self._save_users()
            logger.info(f"Cleaned up {len(tokens_to_remove)} expired reset tokens")


if __name__ == "__main__":
    # Demo usage
    auth = AuthSystem()
    
    # Register demo company
    result = auth.register_user(
        username="demo_admin",
        email="admin@democompany.com",
        password="SecurePass123!",
        company_name="Demo Energy Co",
        country="Demo Country"
    )
    print("Registration:", result)
    
    # Login
    login_result = auth.login("demo_admin", "SecurePass123!")
    print("Login:", login_result)
