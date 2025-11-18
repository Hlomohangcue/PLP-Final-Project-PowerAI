"""
PowerAI Subscription Management System
Freemium model with tiered pricing
"""
from datetime import datetime, timedelta
from typing import Dict, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class SubscriptionTier:
    """Subscription tier definition"""
    name: str
    price_monthly: float
    price_yearly: float
    features: Dict
    limits: Dict
    
class SubscriptionManager:
    """Manage subscription tiers and features"""
    
    TIERS = {
        "free": SubscriptionTier(
            name="Free Trial",
            price_monthly=0,
            price_yearly=0,
            features={
                "forecasting": True,
                "real_time_monitoring": True,
                "basic_analytics": True,
                "data_export": False,
                "api_access": False,
                "advanced_models": False,
                "custom_alerts": False,
                "priority_support": False,
                "white_label": False,
                "multi_user": False
            },
            limits={
                "forecast_hours": 24,
                "data_retention_days": 7,
                "api_calls_per_day": 0,
                "users": 1,
                "trial_days": 14
            }
        ),
        "starter": SubscriptionTier(
            name="Starter",
            price_monthly=49,
            price_yearly=490,  # 2 months free
            features={
                "forecasting": True,
                "real_time_monitoring": True,
                "basic_analytics": True,
                "data_export": True,
                "api_access": True,
                "advanced_models": False,
                "custom_alerts": True,
                "priority_support": False,
                "white_label": False,
                "multi_user": True
            },
            limits={
                "forecast_hours": 168,  # 7 days
                "data_retention_days": 90,
                "api_calls_per_day": 1000,
                "users": 5,
                "trial_days": 0
            }
        ),
        "professional": SubscriptionTier(
            name="Professional",
            price_monthly=149,
            price_yearly=1490,  # 2 months free
            features={
                "forecasting": True,
                "real_time_monitoring": True,
                "basic_analytics": True,
                "data_export": True,
                "api_access": True,
                "advanced_models": True,
                "custom_alerts": True,
                "priority_support": True,
                "white_label": False,
                "multi_user": True
            },
            limits={
                "forecast_hours": 720,  # 30 days
                "data_retention_days": 365,
                "api_calls_per_day": 10000,
                "users": 20,
                "trial_days": 0
            }
        ),
        "enterprise": SubscriptionTier(
            name="Enterprise",
            price_monthly=499,
            price_yearly=4990,  # 2 months free
            features={
                "forecasting": True,
                "real_time_monitoring": True,
                "basic_analytics": True,
                "data_export": True,
                "api_access": True,
                "advanced_models": True,
                "custom_alerts": True,
                "priority_support": True,
                "white_label": True,
                "multi_user": True
            },
            limits={
                "forecast_hours": 8760,  # 1 year
                "data_retention_days": 1825,  # 5 years
                "api_calls_per_day": 100000,
                "users": -1,  # unlimited
                "trial_days": 0
            }
        )
    }
    
    @classmethod
    def get_tier_info(cls, tier_name: str) -> Dict:
        """Get information about a subscription tier"""
        if tier_name not in cls.TIERS:
            tier_name = "free"
        
        tier = cls.TIERS[tier_name]
        return {
            "name": tier.name,
            "tier_id": tier_name,
            "price_monthly": tier.price_monthly,
            "price_yearly": tier.price_yearly,
            "savings_yearly": tier.price_monthly * 12 - tier.price_yearly,
            "features": tier.features,
            "limits": tier.limits
        }
    
    @classmethod
    def get_all_tiers(cls) -> List[Dict]:
        """Get all subscription tiers"""
        return [cls.get_tier_info(tier_name) for tier_name in cls.TIERS.keys()]
    
    @classmethod
    def check_feature_access(cls, tier_name: str, feature: str) -> bool:
        """Check if a tier has access to a feature"""
        if tier_name not in cls.TIERS:
            tier_name = "free"
        return cls.TIERS[tier_name].features.get(feature, False)
    
    @classmethod
    def get_limit(cls, tier_name: str, limit_name: str) -> int:
        """Get a specific limit for a tier"""
        if tier_name not in cls.TIERS:
            tier_name = "free"
        return cls.TIERS[tier_name].limits.get(limit_name, 0)
    
    @classmethod
    def is_trial_expired(cls, created_at: str, tier_name: str) -> bool:
        """Check if free trial has expired"""
        if tier_name != "free":
            return False
        
        created_date = datetime.fromisoformat(created_at)
        trial_days = cls.TIERS["free"].limits["trial_days"]
        expiry_date = created_date + timedelta(days=trial_days)
        
        return datetime.now() > expiry_date
    
    @classmethod
    def get_trial_days_remaining(cls, created_at: str) -> int:
        """Get remaining trial days"""
        created_date = datetime.fromisoformat(created_at)
        trial_days = cls.TIERS["free"].limits["trial_days"]
        expiry_date = created_date + timedelta(days=trial_days)
        
        remaining = (expiry_date - datetime.now()).days
        return max(0, remaining)
    
    @classmethod
    def compare_tiers(cls, current_tier: str, target_tier: str) -> Dict:
        """Compare two tiers to show upgrade benefits"""
        current = cls.get_tier_info(current_tier)
        target = cls.get_tier_info(target_tier)
        
        new_features = []
        improved_limits = {}
        
        # Check new features
        for feature, enabled in target["features"].items():
            if enabled and not current["features"][feature]:
                new_features.append(feature.replace('_', ' ').title())
        
        # Check improved limits
        for limit, value in target["limits"].items():
            current_value = current["limits"][limit]
            if value > current_value or value == -1:  # -1 means unlimited
                improved_limits[limit.replace('_', ' ').title()] = {
                    "from": current_value,
                    "to": value
                }
        
        return {
            "current_tier": current["name"],
            "target_tier": target["name"],
            "price_increase_monthly": target["price_monthly"] - current["price_monthly"],
            "new_features": new_features,
            "improved_limits": improved_limits,
            "recommended": len(new_features) > 3
        }


def format_price(price: float) -> str:
    """Format price for display"""
    if price == 0:
        return "Free"
    return f"${price:,.0f}/month"


def get_tier_badge(tier_name: str) -> str:
    """Get emoji badge for tier"""
    badges = {
        "free": "🆓",
        "starter": "🚀",
        "professional": "⭐",
        "enterprise": "👑"
    }
    return badges.get(tier_name, "📦")


if __name__ == "__main__":
    # Demo
    print("PowerAI Subscription Tiers:\n")
    
    for tier in SubscriptionManager.get_all_tiers():
        print(f"{get_tier_badge(tier['tier_id'])} {tier['name']}")
        print(f"   Price: {format_price(tier['price_monthly'])}")
        print(f"   Features: {sum(tier['features'].values())} enabled")
        print(f"   Forecast: {tier['limits']['forecast_hours']} hours")
        print()
    
    # Compare tiers
    comparison = SubscriptionManager.compare_tiers("free", "professional")
    print("Upgrade from Free to Professional:")
    print(f"New features: {', '.join(comparison['new_features'])}")
    print(f"Price: ${comparison['price_increase_monthly']}/month")
