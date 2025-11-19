# Password Reset Functionality - Setup Guide

## 📧 Overview

PowerAI now includes a complete password reset system with email functionality. Users can request password reset links that are sent to their registered email addresses.

## ✅ Features Added

### 1. **Password Reset Request**
- Users can request password reset from login page
- Email validation before sending reset link
- Secure token generation (URL-safe, 32 bytes)
- Token expires after 1 hour
- One-time use tokens (cannot be reused)

### 2. **Email Notifications**
- **Password Reset Email** - Professional HTML email with reset link
- **Welcome Email** - Sent to new users upon registration
- Beautiful email templates with branding
- Plain text fallback for email clients

### 3. **Security Features**
- ✅ Secure token generation using `secrets.token_urlsafe()`
- ✅ Token expiration (1 hour validity)
- ✅ One-time use enforcement
- ✅ Automatic cleanup of expired tokens
- ✅ No email enumeration (same message for valid/invalid emails)
- ✅ Password strength validation on reset

## 🔧 Setup Instructions

### Step 1: Install Dependencies

```bash
pip install python-dotenv
```

Or install from requirements:
```bash
pip install -r requirements.txt
```

### Step 2: Configure Gmail App Password

1. **Go to Google Account Settings:**
   - Visit: https://myaccount.google.com/apppasswords
   - Sign in to your Google account

2. **Create App Password:**
   - Select "App": Choose "Mail"
   - Select "Device": Choose "Other (Custom name)"
   - Enter name: "PowerAI Streamlit App"
   - Click "Generate"
   - **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

3. **Important:**
   - You need 2-Factor Authentication enabled
   - Regular Gmail password won't work
   - App Password is different from your Gmail password

### Step 3: Set Environment Variables

**Option A: Create .env file (Local Development)**

Create a `.env` file in the project root:

```env
# Email Configuration
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=abcdefghijklmnop

# Application URL
APP_URL=http://localhost:8501

# Optional SMTP Settings
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

**Option B: Streamlit Cloud (Production)**

1. Go to your app dashboard on Streamlit Cloud
2. Click on "Settings" → "Secrets"
3. Add secrets in TOML format:

```toml
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "abcdefghijklmnop"
APP_URL = "https://powerai-lesotho.streamlit.app"
```

**Option C: System Environment Variables (Windows)**

```powershell
$env:SENDER_EMAIL="your-email@gmail.com"
$env:SENDER_PASSWORD="abcdefghijklmnop"
$env:APP_URL="http://localhost:8501"
```

**Option C: System Environment Variables (Linux/Mac)**

```bash
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="abcdefghijklmnop"
export APP_URL="http://localhost:8501"
```

### Step 4: Test Email Configuration

```bash
python email_service.py
```

Expected output:
```
✅ Email service configured correctly
```

If not configured:
```
⚠️  Email service not configured: SENDER_EMAIL not configured

To enable email functionality, set these environment variables:
  SENDER_EMAIL=your-email@gmail.com
  SENDER_PASSWORD=your-app-password
```

## 🚀 Usage

### For End Users

#### Forgot Password:

1. **Go to Login Page**
2. **Click "Forgot Password?"**
3. **Enter your email address**
4. **Check your email inbox**
5. **Click the reset link** (valid for 1 hour)
6. **Create new password**
7. **Login with new password**

#### First Time Registration:

1. **Register your account**
2. **Check email** for welcome message (optional)
3. **Login immediately** (auto-login after registration)

### For Developers

#### Request Password Reset:

```python
from auth_system import AuthSystem
from email_service import EmailService

auth = AuthSystem()
result = auth.request_password_reset("user@example.com")

if result["email_found"]:
    # Send email
    email_service = EmailService()
    email_service.send_password_reset_email(
        to_email=result["email"],
        username=result["username"],
        reset_token=result["reset_token"]
    )
```

#### Verify Reset Token:

```python
verification = auth.verify_reset_token(token)

if verification["valid"]:
    print(f"Valid for user: {verification['username']}")
else:
    print(f"Invalid: {verification['message']}")
```

#### Reset Password:

```python
result = auth.reset_password(token, "NewPassword123!")

if result["success"]:
    print(f"Password reset for: {result['username']}")
else:
    print(f"Failed: {result['message']}")
```

## 📁 Files Added/Modified

### New Files:
- ✅ `email_service.py` - Email sending functionality
- ✅ `.env.example` - Environment configuration template
- ✅ `PASSWORD_RESET_GUIDE.md` - This documentation

### Modified Files:
- ✅ `auth_system.py` - Added password reset methods
- ✅ `auth_pages.py` - Added forgot/reset password UI
- ✅ `streamlit_app.py` - Added reset token handling
- ✅ `requirements.txt` - Added python-dotenv
- ✅ `users_data.json` - Added reset_tokens storage

## 🔒 Security Features

### Token Security:
- **Cryptographically secure** random tokens
- **URL-safe** encoding
- **32-byte length** (256 bits of entropy)
- **One-time use** enforcement
- **Time-limited** (1 hour expiration)

### Email Enumeration Protection:
- Same success message for valid/invalid emails
- Prevents attackers from discovering registered emails
- Follows security best practices

### Password Validation:
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- Enforced on reset

## 📧 Email Templates

### Password Reset Email Features:
- ✅ Professional HTML design
- ✅ Green energy-themed branding
- ✅ Clear call-to-action button
- ✅ Copy-paste link option
- ✅ Security warnings
- ✅ Expiration notice
- ✅ Plain text fallback

### Welcome Email Features:
- ✅ Welcoming message
- ✅ Feature highlights
- ✅ Free trial information
- ✅ Launch dashboard button
- ✅ Contact information

## 🧪 Testing

### Test Password Reset Flow:

1. **Start the app:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Register a test account** with your real email

3. **Logout** and go to login page

4. **Click "Forgot Password?"**

5. **Enter your email** and submit

6. **Check your email** for reset link

7. **Click the link** and create new password

8. **Login** with new password

### Test Without Email (Demo Mode):

If email is not configured, the system will display the reset token directly on the page for testing purposes.

## ⚠️ Troubleshooting

### Issue: "Email authentication failed"

**Solution:**
- Verify you're using an **App Password**, not your regular Gmail password
- Ensure 2-Factor Authentication is enabled on your Google account
- Check the password has no spaces (remove spaces from 16-char password)

### Issue: "Email service not configured"

**Solution:**
- Check `.env` file exists and is in the correct location
- Verify environment variables are set correctly
- Restart the Streamlit app after setting variables

### Issue: "SMTP connection failed"

**Solution:**
- Check your internet connection
- Verify SMTP settings (smtp.gmail.com, port 587)
- Try using a different email provider
- Check firewall settings

### Issue: "Reset link expired"

**Solution:**
- Request a new reset link (tokens expire after 1 hour)
- Links are one-time use only

### Issue: "Link doesn't work in Streamlit Cloud"

**Solution:**
- Ensure `APP_URL` is set to your Streamlit Cloud URL
- Check secrets are properly configured in Streamlit Cloud dashboard
- Links must include the full domain

## 🎯 Demo Mode

If email is **not configured**, the system operates in **demo mode**:

- ✅ Password reset tokens are still generated
- ✅ Reset links are displayed directly on the page
- ✅ You can manually copy the token parameter to URL
- ⚠️ No emails are sent
- ℹ️ Instructions shown for configuring email

This allows testing the feature without email setup.

## 🌐 Using Other Email Providers

### Microsoft Outlook/Office 365:

```env
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
SENDER_EMAIL=your-email@outlook.com
SENDER_PASSWORD=your-password
```

### Yahoo Mail:

```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SENDER_EMAIL=your-email@yahoo.com
SENDER_PASSWORD=your-app-password
```

### Custom SMTP Server:

```env
SMTP_SERVER=smtp.yourdomain.com
SMTP_PORT=587
SENDER_EMAIL=noreply@yourdomain.com
SENDER_PASSWORD=your-password
```

## 📊 Data Storage

Reset tokens are stored in `users_data.json`:

```json
{
  "users": { ... },
  "companies": { ... },
  "reset_tokens": {
    "token_abc123...": {
      "username": "john_doe",
      "email": "john@example.com",
      "created_at": "2025-11-19T10:00:00",
      "expires_at": "2025-11-19T11:00:00",
      "used": false
    }
  }
}
```

Tokens are automatically cleaned up 24 hours after expiration.

## 🔄 Token Cleanup

Expired tokens are automatically cleaned up:

```python
from auth_system import AuthSystem

auth = AuthSystem()
auth.cleanup_expired_tokens()
```

Run this periodically (e.g., daily cron job) to keep the database clean.

## 📝 Best Practices

1. **Always use HTTPS** in production (APP_URL)
2. **Use App Passwords** instead of regular passwords
3. **Keep secrets secure** - never commit .env file
4. **Test email delivery** before deploying
5. **Monitor email quotas** (Gmail: 500 emails/day)
6. **Set up error logging** for email failures
7. **Provide clear error messages** to users
8. **Regular token cleanup** to prevent database bloat

## 🎉 Summary

You now have a complete, production-ready password reset system with:

- ✅ Secure token generation and validation
- ✅ Professional email templates
- ✅ User-friendly UI flow
- ✅ Comprehensive error handling
- ✅ Demo mode for testing
- ✅ Full security features
- ✅ Easy configuration
- ✅ Multi-provider support

**Need help?** Contact: hlomohangsethuntsa3@gmail.com

---

**Date**: November 19, 2025  
**Author**: PowerAI Development Team  
**Project**: PowerAI Lesotho - UN SDG 7 Compliant Energy Management System
