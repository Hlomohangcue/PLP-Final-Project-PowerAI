"""
PowerAI Authentication and Subscription Pages for Streamlit
Enhanced UI for registration, login, subscription management, and password reset
"""
import streamlit as st
from auth_system import AuthSystem
from subscription_system import SubscriptionManager, format_price, get_tier_badge
from email_service import EmailService
import re
import logging

logger = logging.getLogger(__name__)

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> tuple:
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Password is strong"

def show_registration_page():
    """Registration page with freemium signup"""
    st.markdown('<h1 class="main-header">🌟 Join PowerAI - Start Your Free Trial</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <p style='font-size: 1.2rem; color: #555;'>
            Get 14 days of free access to intelligent energy management powered by AI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Benefits section
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("### ⚡ AI Forecasting")
        st.write("24-hour demand predictions")
    with col2:
        st.markdown("### 📊 Real-time Monitoring")
        st.write("Live energy tracking")
    with col3:
        st.markdown("### 💰 Cost Savings")
        st.write("Optimize energy usage")
    with col4:
        st.markdown("### 🌍 SDG 7 Aligned")
        st.write("Sustainable energy")
    
    st.markdown("---")
    
    # Registration form
    with st.form("registration_form"):
        st.markdown("### Create Your Account")
        
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username*", placeholder="johndoe")
            email = st.text_input("Email*", placeholder="john@company.com")
            company_name = st.text_input("Company Name*", placeholder="Green Energy Corp")
        
        with col2:
            password = st.text_input("Password*", type="password", 
                                    placeholder="Min 8 chars, 1 upper, 1 number")
            confirm_password = st.text_input("Confirm Password*", type="password")
            country = st.selectbox("Country*", [
                "Select Country",
                "Lesotho", "South Africa", "Kenya", "Tanzania", "Botswana", "Namibia",
                "Zimbabwe", "Zambia", "Malawi", "Mozambique", "Other"
            ])
        
        # Terms and conditions
        agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        submit_button = st.form_submit_button("🚀 Start Free Trial", use_container_width=True)
        
        if submit_button:
            # Validation
            errors = []
            
            if not username or len(username) < 3:
                errors.append("Username must be at least 3 characters")
            
            if not validate_email(email):
                errors.append("Please enter a valid email address")
            
            is_strong, msg = validate_password(password)
            if not is_strong:
                errors.append(msg)
            
            if password != confirm_password:
                errors.append("Passwords do not match")
            
            if not company_name or len(company_name) < 2:
                errors.append("Please enter a valid company name")
            
            if country == "Select Country":
                errors.append("Please select a country")
            
            if not agree_terms:
                errors.append("You must agree to the Terms of Service")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Register user
                auth = AuthSystem()
                result = auth.register_user(
                    username=username,
                    email=email,
                    password=password,
                    company_name=company_name,
                    country=country
                )
                
                if result["success"]:
                    st.success("🎉 " + result["message"])
                    st.balloons()
                    
                    # Try to send welcome email
                    try:
                        email_service = EmailService()
                        email_service.send_welcome_email(
                            to_email=email,
                            username=username,
                            company_name=company_name
                        )
                    except Exception as e:
                        logger.warning(f"Failed to send welcome email: {e}")
                    
                    # Auto login
                    login_result = auth.login(username, password)
                    if login_result["success"]:
                        st.session_state.authenticated = True
                        st.session_state.user = login_result["user"]
                        st.session_state.page = "dashboard"
                        st.rerun()
                else:
                    st.error(result["message"])
    
    # Existing user
    st.markdown("---")
    st.markdown("### Already have an account?")
    if st.button("Sign In", use_container_width=True):
        st.session_state.page = "login"
        st.rerun()

def show_login_page():
    """Login page"""
    st.markdown('<h1 class="main-header">🔐 Sign In to PowerAI</h1>', 
                unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.markdown("### Enter Your Credentials")
            
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", 
                                    placeholder="Enter your password")
            
            remember_me = st.checkbox("Remember me")
            
            submit_button = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit_button:
                if not username or not password:
                    st.error("Please enter both username and password")
                else:
                    auth = AuthSystem()
                    result = auth.login(username, password)
                    
                    if result["success"]:
                        st.success("✅ " + result["message"])
                        st.session_state.authenticated = True
                        st.session_state.user = result["user"]
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error("❌ " + result["message"])
        
        st.markdown("---")
        
        col_forgot, col_register = st.columns(2)
        with col_forgot:
            if st.button("Forgot Password?"):
                st.session_state.page = "forgot_password"
                st.rerun()
        with col_register:
            if st.button("Create Account"):
                st.session_state.page = "register"
                st.rerun()

def show_forgot_password_page():
    """Forgot password page - request reset email"""
    st.markdown('<h1 class="main-header">🔐 Reset Your Password</h1>', 
                unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <p>Enter your email address and we'll send you a link to reset your password.</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("forgot_password_form"):
            email = st.text_input("Email Address", placeholder="your-email@example.com")
            
            submit_button = st.form_submit_button("Send Reset Link", use_container_width=True)
            
            if submit_button:
                if not email:
                    st.error("Please enter your email address")
                elif not validate_email(email):
                    st.error("Please enter a valid email address")
                else:
                    # Request password reset
                    auth = AuthSystem()
                    result = auth.request_password_reset(email)
                    
                    if result["success"]:
                        # Send email if user found
                        if result.get("email_found"):
                            email_service = EmailService()
                            email_result = email_service.send_password_reset_email(
                                to_email=email,
                                username=result["username"],
                                reset_token=result["reset_token"]
                            )
                            
                            if email_result["success"]:
                                st.success("✅ Password reset link sent! Check your email inbox.")
                                st.info("💡 The link will expire in 1 hour.")
                            elif email_result.get("demo_mode"):
                                # Email service not configured - show token directly
                                st.warning("⚠️ Email service not configured. Here's your reset link:")
                                reset_link = f"?reset_token={result['reset_token']}"
                                st.code(reset_link, language=None)
                                st.info("Copy this and add it to your browser URL after the main URL")
                                st.markdown("---")
                                st.markdown("**To enable email functionality:**")
                                st.markdown("1. Get a Gmail App Password from: https://myaccount.google.com/apppasswords")
                                st.markdown("2. Set environment variables:")
                                st.code("SENDER_EMAIL=your-email@gmail.com\nSENDER_PASSWORD=your-app-password")
                            else:
                                st.error(f"Failed to send email: {email_result['message']}")
                        else:
                            # Show same message for security
                            st.success("✅ If this email is registered, you will receive a password reset link.")
        
        st.markdown("---")
        
        col_back, col_register = st.columns(2)
        with col_back:
            if st.button("← Back to Login"):
                st.session_state.page = "login"
                st.rerun()
        with col_register:
            if st.button("Create Account"):
                st.session_state.page = "register"
                st.rerun()

def show_reset_password_page(reset_token: str):
    """Reset password page - create new password"""
    st.markdown('<h1 class="main-header">🔐 Create New Password</h1>', 
                unsafe_allow_html=True)
    
    # Verify token first
    auth = AuthSystem()
    verification = auth.verify_reset_token(reset_token)
    
    if not verification["valid"]:
        st.error(f"❌ {verification['message']}")
        st.markdown("---")
        if st.button("Request New Reset Link"):
            st.session_state.page = "forgot_password"
            st.rerun()
        return
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.success(f"✅ Resetting password for: **{verification['username']}**")
        st.info(f"📧 Email: {verification['email']}")
        
        st.markdown("---")
        
        with st.form("reset_password_form"):
            new_password = st.text_input("New Password", type="password",
                                        placeholder="Min 8 chars, 1 upper, 1 number")
            confirm_password = st.text_input("Confirm New Password", type="password")
            
            submit_button = st.form_submit_button("Reset Password", use_container_width=True)
            
            if submit_button:
                # Validation
                errors = []
                
                is_strong, msg = validate_password(new_password)
                if not is_strong:
                    errors.append(msg)
                
                if new_password != confirm_password:
                    errors.append("Passwords do not match")
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    # Reset password
                    result = auth.reset_password(reset_token, new_password)
                    
                    if result["success"]:
                        st.success("🎉 " + result["message"])
                        st.balloons()
                        
                        # Auto-redirect to login after 3 seconds
                        st.info("Redirecting to login page...")
                        import time
                        time.sleep(2)
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error(result["message"])
        
        st.markdown("---")
        
        if st.button("← Back to Login"):
            st.session_state.page = "login"
            st.rerun()

def show_subscription_page(user_info: dict):
    """Subscription management and upgrade page"""
    st.markdown('<h1 class="main-header">💎 Subscription & Billing</h1>', 
                unsafe_allow_html=True)
    
    current_tier = user_info.get("subscription_tier", "free")
    company_name = user_info.get("company_name", "Your Company")
    
    # Current plan
    st.markdown(f"### Current Plan: {get_tier_badge(current_tier)} {SubscriptionManager.TIERS[current_tier].name}")
    
    current_tier_info = SubscriptionManager.get_tier_info(current_tier)
    
    if current_tier == "free":
        # Show trial info
        created_at = user_info.get("created_at", "")
        if created_at:
            days_remaining = SubscriptionManager.get_trial_days_remaining(created_at)
            
            if days_remaining > 0:
                st.info(f"⏰ You have **{days_remaining} days** remaining in your free trial")
            else:
                st.warning("⚠️ Your free trial has expired. Upgrade to continue using PowerAI.")
    
    st.markdown("---")
    
    # Show all plans
    st.markdown("### Choose Your Plan")
    
    plans = SubscriptionManager.get_all_tiers()
    cols = st.columns(4)
    
    for idx, plan in enumerate(plans):
        with cols[idx]:
            tier_id = plan["tier_id"]
            is_current = tier_id == current_tier
            
            # Plan card
            st.markdown(f"""
            <div style='
                border: 2px solid {"#2c5530" if is_current else "#ddd"};
                border-radius: 10px;
                padding: 1.5rem;
                background: {"#f0f8f0" if is_current else "white"};
                height: 100%;
            '>
                <h3 style='text-align: center;'>{get_tier_badge(tier_id)} {plan['name']}</h3>
                <h2 style='text-align: center; color: #2c5530;'>{format_price(plan['price_monthly'])}</h2>
                <p style='text-align: center; color: #666; font-size: 0.9rem;'>
                    {f"${plan['price_yearly']}/year (Save ${plan['savings_yearly']})" if plan['price_yearly'] > 0 else "14-day trial"}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**Features:**")
            for feature, enabled in plan['features'].items():
                icon = "✅" if enabled else "❌"
                st.markdown(f"{icon} {feature.replace('_', ' ').title()}")
            
            st.markdown("**Limits:**")
            st.markdown(f"• Forecast: {plan['limits']['forecast_hours']}h")
            st.markdown(f"• Data: {plan['limits']['data_retention_days']} days")
            st.markdown(f"• Users: {plan['limits']['users'] if plan['limits']['users'] > 0 else 'Unlimited'}")
            
            if is_current:
                st.success("✓ Current Plan")
            elif tier_id == "free":
                if st.button("Start Free Trial", key=f"trial_{tier_id}", use_container_width=True):
                    st.info("You're already on a free trial!")
            else:
                if st.button(f"Upgrade to {plan['name']}", key=f"upgrade_{tier_id}", 
                           use_container_width=True):
                    st.session_state.selected_upgrade_tier = tier_id
                    st.session_state.show_upgrade_modal = True
                    st.rerun()
    
    # Show upgrade modal if selected
    if st.session_state.get("show_upgrade_modal"):
        show_upgrade_modal(current_tier, st.session_state.get("selected_upgrade_tier"))
    
    # Features comparison
    st.markdown("---")
    st.markdown("### Feature Comparison")
    
    comparison_data = []
    all_features = list(plans[0]['features'].keys())
    
    for feature in all_features:
        row = {
            "Feature": feature.replace('_', ' ').title(),
            "Free": "✅" if plans[0]['features'][feature] else "❌",
            "Starter": "✅" if plans[1]['features'][feature] else "❌",
            "Professional": "✅" if plans[2]['features'][feature] else "❌",
            "Enterprise": "✅" if plans[3]['features'][feature] else "❌"
        }
        comparison_data.append(row)
    
    import pandas as pd
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, hide_index=True, use_container_width=True)

def show_upgrade_modal(current_tier: str, target_tier: str):
    """Show upgrade confirmation modal"""
    st.markdown("---")
    st.markdown("### Confirm Upgrade")
    
    comparison = SubscriptionManager.compare_tiers(current_tier, target_tier)
    target_info = SubscriptionManager.get_tier_info(target_tier)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### What's Included:")
        for feature in comparison['new_features']:
            st.markdown(f"✨ {feature}")
        
        st.markdown("#### Improved Limits:")
        for limit, values in comparison['improved_limits'].items():
            st.markdown(f"📈 {limit}: {values['from']} → {values['to']}")
    
    with col2:
        st.markdown("#### Billing Summary:")
        st.markdown(f"**Plan:** {target_info['name']}")
        st.markdown(f"**Monthly:** ${target_info['price_monthly']}")
        st.markdown(f"**Yearly:** ${target_info['price_yearly']} (Save ${target_info['savings_yearly']})")
        
        billing_cycle = st.radio("Billing Cycle", ["Monthly", "Yearly (Save 17%)"])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", use_container_width=True):
            st.session_state.show_upgrade_modal = False
            st.rerun()
    with col2:
        if st.button("Confirm Upgrade", use_container_width=True, type="primary"):
            # In a real app, integrate with payment gateway here
            st.success("🎉 Upgrade successful! (Demo mode - no payment processed)")
            
            # Update subscription
            auth = AuthSystem()
            username = st.session_state.user["username"]
            user_info = auth.get_user_info(username)
            auth.update_subscription(user_info["company_id"], target_tier)
            
            # Update session
            st.session_state.user["subscription_tier"] = target_tier
            st.session_state.show_upgrade_modal = False
            st.balloons()
            st.rerun()
