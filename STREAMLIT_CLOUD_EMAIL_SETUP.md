# Streamlit Cloud Email Configuration Guide

## 🎯 Quick Setup for Password Reset on Streamlit Cloud

Your email is already configured locally. Now let's add it to Streamlit Cloud so password reset works on your deployed app.

---

## 📋 Step 1: Access Streamlit Cloud Secrets

1. **Go to:** https://share.streamlit.io/
2. **Sign in** to your Streamlit Cloud account
3. **Navigate to your app:** `PLP-Final-Project-PowerAI`
4. Click the **⚙️ Settings** button (top right)
5. Click **Secrets** in the left sidebar

---

## 🔑 Step 2: Add Your Email Configuration

Copy and paste this into the Secrets section:

```toml
# Email Configuration for Password Reset
SENDER_EMAIL = "hlomohangsethuntsa3@gmail.com"
SENDER_PASSWORD = "ojgn wshu hlrf wuhv"

# SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = "587"

# Application URL
APP_URL = "https://powerai-lesotho.streamlit.app"

# Company Configuration
DEFAULT_COMPANY_ID = "demo_company"
COMPANIES_CONFIG_FILE = "companies.json"
```

**Important Notes:**
- Streamlit Cloud uses TOML format (different from .env)
- Your Gmail App Password is already in the format above
- Keep the quotes around values
- Password has spaces - that's normal for Gmail App Passwords

---

## ✅ Step 3: Save and Reboot

1. Click **"Save"** button at the bottom
2. Your app will automatically **reboot** (takes ~30 seconds)
3. Password reset will now work on the deployed version! 🎉

---

## 🧪 Step 4: Test It

1. **Go to:** https://powerai-lesotho.streamlit.app/
2. **Click:** "Forgot Password?" on login page
3. **Enter:** Any registered user's email
4. **Check:** Your Gmail inbox for the reset email
5. **Click:** The reset link in the email
6. **Create:** New password
7. **Login:** Success! ✅

---

## 🔒 Security Best Practices

### ✅ Your Setup is Secure
- ✅ Using Gmail App Password (not your main password)
- ✅ App Password is 16 characters long
- ✅ 2-Factor Authentication is enabled on your Gmail
- ✅ Secrets are encrypted on Streamlit Cloud
- ✅ Never committed to Git

### 🚨 Keep Safe
- Don't share your App Password with anyone
- Don't commit .env file to Git (already in .gitignore)
- Regenerate App Password if compromised
- Monitor your Gmail sent folder

---

## 📧 What Will Happen

### Password Reset Email:
```
From: PowerAI Lesotho <hlomohangsethuntsa3@gmail.com>
To: user@example.com
Subject: PowerAI Lesotho - Password Reset Request

[Beautiful HTML email with:]
- Professional PowerAI branding
- "Reset Password" button
- Security warnings
- 1-hour expiration notice
```

### Welcome Email (on Registration):
```
From: PowerAI Lesotho <hlomohangsethuntsa3@gmail.com>
To: newuser@example.com
Subject: Welcome to PowerAI Lesotho! 🎉

[Professional welcome email with:]
- Feature highlights
- Free trial information
- Launch dashboard button
```

---

## 🆘 Troubleshooting

### Issue: "Email service not configured" message

**Solution:**
1. Check Streamlit Cloud secrets are saved correctly
2. Reboot the app from Settings → Reboot app
3. Wait 30 seconds for full restart

### Issue: Emails not being received

**Check:**
1. ✅ Gmail inbox (not spam)
2. ✅ Correct email entered
3. ✅ App Password has no extra spaces
4. ✅ Format in Streamlit Cloud is TOML (with quotes)

### Issue: "Email authentication failed"

**Solution:**
1. Verify App Password is correct (16 characters, includes spaces)
2. Check 2FA is enabled on your Gmail account
3. Regenerate App Password if needed
4. Update both .env and Streamlit Cloud secrets

---

## 📊 Gmail Sending Limits

**Free Gmail Account:**
- ✅ 500 emails per day
- ✅ More than enough for your app
- ✅ Resets every 24 hours

**Monitor Usage:**
- Check Gmail "Sent" folder
- Enable email notifications in Gmail
- Set up quota alerts if needed

---

## 🔄 Updating Configuration Later

### Change Email Address:
1. Get new Gmail App Password
2. Update `.env` locally
3. Update Streamlit Cloud secrets
4. Reboot app

### Change App Password:
1. Go to: https://myaccount.google.com/apppasswords
2. Revoke old password
3. Create new App Password
4. Update both .env and Streamlit Cloud secrets
5. Reboot app

---

## ✨ Testing Checklist

After configuring on Streamlit Cloud, test:

- [ ] Go to https://powerai-lesotho.streamlit.app/
- [ ] Click "Forgot Password?" on login page
- [ ] Enter registered email address
- [ ] See success message
- [ ] Check email inbox (and spam folder)
- [ ] Receive password reset email within 1 minute
- [ ] Click reset link in email
- [ ] Create new password
- [ ] Login successfully with new password
- [ ] Optionally: Register new user and check welcome email

---

## 🎉 Summary

**Your Configuration:**
```
✅ Email: hlomohangsethuntsa3@gmail.com
✅ SMTP: Gmail (smtp.gmail.com:587)
✅ App Password: Configured
✅ App URL: https://powerai-lesotho.streamlit.app
✅ Local: Working (.env configured)
⏳ Cloud: Needs secrets added (follow steps above)
```

**After Adding Secrets:**
```
✅ Password reset fully functional
✅ Welcome emails on registration
✅ Professional HTML templates
✅ Secure token system (1-hour expiry)
✅ Production-ready deployment
```

---

## 📞 Need Help?

**Documentation:**
- Full Guide: `PASSWORD_RESET_GUIDE.md`
- Quick Start: `PASSWORD_RESET_QUICKSTART.md`

**Contact:**
- Email: hlomohangsethuntsa3@gmail.com
- GitHub: https://github.com/Hlomohangcue/PLP-Final-Project-PowerAI

---

**Ready to deploy!** Follow the steps above and your password reset will work on Streamlit Cloud in minutes. 🚀
