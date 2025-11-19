#!/usr/bin/env python3
"""
Test script to verify company registration integration with company data viewing
"""

import json
from config_multi_tenant import MultiTenantConfig
from auth_system import AuthSystem

def test_company_registration_integration():
    """Test that registered companies appear in the company view dropdown"""
    
    print("=" * 60)
    print("Testing Company Registration Integration")
    print("=" * 60)
    print()
    
    # 1. Check existing registered companies in users_data.json
    print("📋 Step 1: Reading registered companies from users_data.json...")
    try:
        with open('users_data.json', 'r') as f:
            users_data = json.load(f)
            registered_companies = users_data.get('companies', {})
            
        print(f"   ✅ Found {len(registered_companies)} registered companies:")
        for company_id, company_info in registered_companies.items():
            print(f"      - {company_info['company_name']} ({company_info['country']})")
            print(f"        ID: {company_id}")
            print(f"        Owner: {company_info['owner']}")
            print(f"        Tier: {company_info['subscription_tier']}")
            print()
    except FileNotFoundError:
        print("   ⚠️  users_data.json not found")
        registered_companies = {}
    except Exception as e:
        print(f"   ❌ Error: {e}")
        registered_companies = {}
    
    print()
    
    # 2. Load companies using MultiTenantConfig
    print("📋 Step 2: Loading companies via MultiTenantConfig...")
    config = MultiTenantConfig()
    all_companies = config.get_all_companies()
    
    print(f"   ✅ Loaded {len(all_companies)} companies into config:")
    for company_id, company_config in all_companies.items():
        print(f"      - {company_config.company_name} ({company_config.country})")
        print(f"        ID: {company_id}")
        print(f"        Renewable Types: {', '.join(company_config.renewable_types)}")
        print()
    
    print()
    
    # 3. Verify integration
    print("📋 Step 3: Verifying integration...")
    missing_companies = []
    
    for company_id in registered_companies.keys():
        if company_id not in all_companies:
            missing_companies.append(company_id)
    
    if not missing_companies:
        print("   ✅ SUCCESS: All registered companies are available in company view!")
    else:
        print(f"   ❌ FAILED: {len(missing_companies)} companies missing from view:")
        for company_id in missing_companies:
            print(f"      - {company_id}")
    
    print()
    
    # 4. Test refresh functionality
    print("📋 Step 4: Testing refresh functionality...")
    refreshed_companies = config.get_all_companies(refresh=True)
    print(f"   ✅ After refresh: {len(refreshed_companies)} companies available")
    
    print()
    print("=" * 60)
    print("Test Complete!")
    print("=" * 60)
    
    return len(missing_companies) == 0

def test_new_registration():
    """Test registering a new company and verifying it appears"""
    
    print("\n" + "=" * 60)
    print("Testing New Company Registration")
    print("=" * 60)
    print()
    
    # Create a test company
    auth = AuthSystem()
    test_username = "test_solar_company"
    test_company = "Test Solar Energy Co."
    
    # Check if already exists
    try:
        with open('users_data.json', 'r') as f:
            users_data = json.load(f)
            if test_username in users_data.get('users', {}):
                print(f"   ℹ️  Test user '{test_username}' already exists")
                print("   Skipping registration test")
                return True
    except:
        pass
    
    print(f"📝 Registering test company: {test_company}...")
    result = auth.register_user(
        username=test_username,
        email="test@solartestco.com",
        password="TestPass123!",
        company_name=test_company,
        country="Test Country"
    )
    
    if result['success']:
        print(f"   ✅ Registration successful!")
        print(f"      Company ID: {result['company_id']}")
        
        # Verify it appears in config
        config = MultiTenantConfig()
        all_companies = config.get_all_companies(refresh=True)
        
        if result['company_id'] in all_companies:
            print(f"   ✅ New company appears in company view!")
            company_config = all_companies[result['company_id']]
            print(f"      Name: {company_config.company_name}")
            print(f"      Country: {company_config.country}")
            return True
        else:
            print(f"   ❌ New company NOT found in company view")
            return False
    else:
        print(f"   ❌ Registration failed: {result['message']}")
        return False

if __name__ == "__main__":
    # Run tests
    test1_passed = test_company_registration_integration()
    test2_passed = test_new_registration()
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    print(f"Integration Test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"New Registration Test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print("=" * 60)
