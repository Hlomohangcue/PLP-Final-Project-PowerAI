# Password Reset Feature - Quick Start

## ✅ What Was Added

Your PowerAI application now has **complete password reset functionality** with real email support!

## 🚀 Quick Setup (3 Steps)

### 1. Get Gmail App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Sign in to your Google account
3. Create App Password:
   - App: **Mail**
   - Device: **Other (PowerAI)**
4. Copy the 16-character password

### 2. Configure Environment

Create `.env` file in project root:

```env
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=abcd efgh ijkl mnop
APP_URL=http://localhost:8501
```

### 3. Test It

```bash
# Test email configuration
python email_service.py

# Test password reset flow
python test_password_reset.py

# Run the app
streamlit run streamlit_app.py
```

## 🎯 How Users Reset Password

1. **Login Page** → Click "Forgot Password?"
2. **Enter email** → Click "Send Reset Link"
3. **Check email** → Click reset link (or copy token if demo mode)
4. **Create new password** → Submit
5. **Login** with new password ✅

## 📧 Email Examples

### Password Reset Email:
- Professional HTML template
- Green energy branding
- Clear reset button
- Security warnings
- 1-hour expiration notice

### Welcome Email (Bonus):
- Sent on new registration
- Feature highlights
- Free trial info
- Launch dashboard button

## 🔒 Security Features

- ✅ Cryptographically secure tokens (32 bytes)
- ✅ 1-hour token expiration
- ✅ One-time use enforcement
- ✅ No email enumeration
- ✅ Password strength validation
- ✅ Automatic cleanup of old tokens

## 📁 New Files

```
email_service.py           - Email sending functionality
.env.example              - Configuration template
PASSWORD_RESET_GUIDE.md   - Complete documentation
test_password_reset.py    - Testing suite
```

## 🎨 Modified Files

```
auth_system.py     - Added reset methods
auth_pages.py      - Added reset UI pages  
streamlit_app.py   - Added token handling
requirements.txt   - Added python-dotenv
```

## 💡 Demo Mode

**No email configured?** No problem!

The system works in **demo mode**:
- Reset tokens displayed on screen
- Copy token parameter to URL manually
- Test full flow without email
- Perfect for development

## 🌐 Streamlit Cloud Setup

Add to your app secrets:

```toml
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-app-password"
APP_URL = "https://powerai-lesotho.streamlit.app"
```

## ✅ Test Results

```
✅ Token generation working
✅ Token verification working  
✅ Password reset working
✅ Token marked as used after reset
✅ Login with new password working
✅ Email enumeration protection working
✅ Token expiration detection working
```

## 🆘 Need Help?

Full guide: `PASSWORD_RESET_GUIDE.md`

Contact: hlomohangsethuntsa3@gmail.com

---

**Ready to use!** The feature is fully functional and tested. 🎉
