"""
PowerAI Demo Script
Quick demonstration of key features for presentations
"""
from auth_system import AuthSystem
from subscription_system import SubscriptionManager
import json

def demo_user_registration():
    """Demo 1: User Registration"""
    print("\n" + "="*60)
    print("DEMO 1: User Registration & Free Trial")
    print("="*60)
    
    auth = AuthSystem()
    
    # Register a demo company
    print("\n📝 Registering new company...")
    result = auth.register_user(
        username="demo_energy",
        email="admin@demoenergy.com",
        password="SecurePass123!",
        company_name="Demo Energy Solutions",
        country="South Africa"
    )
    
    print(f"✓ Registration: {result['message']}")
    if result['success']:
        print(f"  - User ID: {result['user_id']}")
        print(f"  - Company ID: {result['company_id']}")
        print(f"  - Trial: 14 days")

def demo_login():
    """Demo 2: User Login"""
    print("\n" + "="*60)
    print("DEMO 2: User Login")
    print("="*60)
    
    auth = AuthSystem()
    
    print("\n🔐 Logging in...")
    result = auth.login("demo_energy", "SecurePass123!")
    
    if result['success']:
        user = result['user']
        print(f"✓ Login successful!")
        print(f"  - Username: {user['username']}")
        print(f"  - Company: {user['company_name']}")
        print(f"  - Subscription: {user['subscription_tier']}")
        print(f"  - Role: {user['role']}")

def demo_subscription_tiers():
    """Demo 3: Subscription Tiers"""
    print("\n" + "="*60)
    print("DEMO 3: Subscription Tiers & Pricing")
    print("="*60)
    
    tiers = SubscriptionManager.get_all_tiers()
    
    for tier in tiers:
        print(f"\n📦 {tier['name']}")
        print(f"   Price: ${tier['price_monthly']}/month")
        if tier['price_yearly'] > 0:
            print(f"   Yearly: ${tier['price_yearly']}/year (Save ${tier['savings_yearly']})")
        print(f"   Features enabled: {sum(tier['features'].values())}/{len(tier['features'])}")
        print(f"   Forecast hours: {tier['limits']['forecast_hours']}")
        print(f"   Max users: {tier['limits']['users'] if tier['limits']['users'] > 0 else 'Unlimited'}")

def demo_feature_access():
    """Demo 4: Feature Access Control"""
    print("\n" + "="*60)
    print("DEMO 4: Feature Access Control")
    print("="*60)
    
    features = ['forecasting', 'api_access', 'advanced_models', 'white_label']
    tiers = ['free', 'starter', 'professional', 'enterprise']
    
    print("\nFeature Access Matrix:")
    print(f"{'Feature':<20} {'Free':<8} {'Starter':<10} {'Pro':<8} {'Enterprise':<12}")
    print("-" * 60)
    
    for feature in features:
        row = f"{feature:<20}"
        for tier in tiers:
            has_access = SubscriptionManager.check_feature_access(tier, feature)
            row += f" {'✅' if has_access else '❌':<8}"
        print(row)

def demo_upgrade_comparison():
    """Demo 5: Upgrade Benefits"""
    print("\n" + "="*60)
    print("DEMO 5: Upgrade Comparison (Free → Professional)")
    print("="*60)
    
    comparison = SubscriptionManager.compare_tiers("free", "professional")
    
    print(f"\n📈 Upgrading from {comparison['current_tier']} to {comparison['target_tier']}")
    print(f"\n💰 Cost: +${comparison['price_increase_monthly']}/month")
    
    print(f"\n✨ New Features:")
    for feature in comparison['new_features']:
        print(f"   • {feature}")
    
    print(f"\n📊 Improved Limits:")
    for limit, values in comparison['improved_limits'].items():
        to_value = "Unlimited" if values['to'] == -1 else values['to']
        print(f"   • {limit}: {values['from']} → {to_value}")

def demo_trial_management():
    """Demo 6: Trial Expiration"""
    print("\n" + "="*60)
    print("DEMO 6: Trial Expiration Management")
    print("="*60)
    
    auth = AuthSystem()
    user_info = auth.get_user_info("demo_energy")
    
    if user_info and user_info['subscription_tier'] == "free":
        days_remaining = SubscriptionManager.get_trial_days_remaining(user_info['created_at'])
        is_expired = SubscriptionManager.is_trial_expired(user_info['created_at'], "free")
        
        print(f"\n⏰ Trial Status for {user_info['username']}:")
        print(f"   Days remaining: {days_remaining}")
        print(f"   Status: {'Expired' if is_expired else 'Active'}")
        
        if days_remaining <= 3 and not is_expired:
            print(f"\n⚠️  Warning: Only {days_remaining} days left!")
            print("   Upgrade now to continue accessing all features")

def demo_company_statistics():
    """Demo 7: Platform Statistics"""
    print("\n" + "="*60)
    print("DEMO 7: Platform Statistics")
    print("="*60)
    
    auth = AuthSystem()
    companies = auth.get_all_companies()
    
    print(f"\n📊 Total registered companies: {len(companies)}")
    
    # Subscription breakdown
    subscription_counts = {}
    for company in companies:
        tier = company['subscription_tier']
        subscription_counts[tier] = subscription_counts.get(tier, 0) + 1
    
    print(f"\n💎 Subscription Breakdown:")
    for tier, count in subscription_counts.items():
        print(f"   {tier.title()}: {count} companies")
    
    # Revenue estimation (demo mode)
    total_revenue = 0
    for company in companies:
        tier = company['subscription_tier']
        if tier != 'free':
            tier_info = SubscriptionManager.get_tier_info(tier)
            total_revenue += tier_info['price_monthly']
    
    print(f"\n💰 Estimated Monthly Revenue: ${total_revenue:,}")
    print(f"   Annual (MRR × 12): ${total_revenue * 12:,}")

def run_full_demo():
    """Run complete demo sequence"""
    print("\n" + "="*70)
    print(" " * 15 + "PowerAI Enhanced - Feature Demo")
    print(" " * 10 + "Competition Edition with Authentication & Subscriptions")
    print("="*70)
    
    try:
        demo_user_registration()
        demo_login()
        demo_subscription_tiers()
        demo_feature_access()
        demo_upgrade_comparison()
        demo_trial_management()
        demo_company_statistics()
        
        print("\n" + "="*70)
        print(" " * 20 + "✅ Demo Complete!")
        print(" " * 15 + "Ready for competition presentation")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_full_demo()
    
    print("\n💡 Next Steps:")
    print("   1. Run: streamlit run streamlit_app.py")
    print("   2. Register a new account")
    print("   3. Explore the 14-day free trial")
    print("   4. View subscription plans")
    print("   5. Test forecasting features")
    print("\n🏆 Ready to win! Good luck!")
