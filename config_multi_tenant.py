#!/usr/bin/env python3
"""
PowerAI - Multi-Tenant Configuration System
==========================================

This configuration system allows PowerAI to be used by different renewable energy companies
while maintaining data isolation, custom branding, and company-specific settings.

Supports UN SDG 7: Affordable and Clean Energy objectives for any energy company.
"""

import os
from datetime import timedelta
from typing import Dict, Any, Optional
import json


class CompanyConfig:
    """Configuration for individual energy companies"""
    
    def __init__(self, company_id: str, config_data: Dict[str, Any]):
        self.company_id = company_id
        self.company_name = config_data.get('company_name', 'Energy Company')
        self.company_description = config_data.get('company_description', 'Renewable Energy Solutions')
        self.address = config_data.get('address', 'Energy City, Renewable District')
        self.country = config_data.get('country', 'Unknown')
        self.currency = config_data.get('currency', 'USD')
        self.timezone = config_data.get('timezone', 'UTC')
        
        # Branding
        self.brand_color_primary = config_data.get('brand_color_primary', '#2E7D32')
        self.brand_color_secondary = config_data.get('brand_color_secondary', '#4CAF50')
        self.logo_url = config_data.get('logo_url', '/static/img/default_logo.png')
        self.website_url = config_data.get('website_url', '#')
        
        # Energy specifications
        self.grid_voltage = config_data.get('grid_voltage', 230)  # Volts
        self.grid_frequency = config_data.get('grid_frequency', 50)  # Hz
        self.renewable_types = config_data.get('renewable_types', ['solar', 'wind'])
        
        # Business metrics
        self.customer_segments = config_data.get('customer_segments', ['residential', 'commercial', 'industrial'])
        self.tariff_structure = config_data.get('tariff_structure', 'time_of_use')
        self.capacity_mw = config_data.get('capacity_mw', 50.0)  # Default capacity in MW
        
        # AI/ML settings
        self.forecast_horizon_hours = config_data.get('forecast_horizon_hours', 24)
        self.prediction_interval_minutes = config_data.get('prediction_interval_minutes', 15)
        self.enable_lstm_models = config_data.get('enable_lstm_models', True)
        self.enable_prophet_models = config_data.get('enable_prophet_models', True)
        
        # Dashboard settings
        self.dashboard_refresh_seconds = config_data.get('dashboard_refresh_seconds', 30)
        self.show_executive_dashboard = config_data.get('show_executive_dashboard', True)
        self.custom_kpis = config_data.get('custom_kpis', [])
    
    @property
    def branding(self):
        """Return branding configuration as an object for template access"""
        class BrandingConfig:
            def __init__(self, config):
                self.primary_color = config.brand_color_primary
                self.secondary_color = config.brand_color_secondary
                self.logo_url = config.logo_url
                self.website_url = config.website_url
                self.company_name = config.company_name
        
        return BrandingConfig(self)


class MultiTenantConfig:
    """Main configuration class for multi-tenant PowerAI system"""
    
    def __init__(self):
        self.companies = {}
        self.default_company_id = os.environ.get('DEFAULT_COMPANY_ID', 'demo_company')
        self._load_company_configs()
    
    def _load_company_configs(self):
        """Load company configurations from environment or files"""
        # Try to load from companies.json file
        config_file = os.environ.get('COMPANIES_CONFIG_FILE', 'companies.json')
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    companies_data = json.load(f)
                    
                for company_id, config_data in companies_data.items():
                    self.companies[company_id] = CompanyConfig(company_id, config_data)
            except Exception as e:
                print(f"Error loading companies config: {e}")
        
        # If no companies loaded, create default demo company
        if not self.companies:
            self._create_default_companies()
    
    def _create_default_companies(self):
        """Create default company configurations for demonstration"""
        
        # Demo Company 1: SolarTech Solutions
        solartech_config = {
            'company_name': 'SolarTech Solutions',
            'company_description': 'Leading solar energy solutions in Kenya',
            'address': 'Nairobi Technology Park, Kenya',
            'country': 'Kenya',
            'currency': 'KES',
            'timezone': 'Africa/Nairobi',
            'brand_color_primary': '#FF9800',
            'brand_color_secondary': '#FFC107',
            'renewable_types': ['solar', 'wind', 'hydro'],
            'grid_voltage': 240,
            'grid_frequency': 50,
            'customer_segments': ['residential', 'commercial', 'industrial', 'agricultural'],
            'capacity_mw': 125.5,
            'enable_lstm_models': True,
            'enable_prophet_models': True,
            'forecast_horizon_hours': 48
        }
        
        # Demo Company 2: WindPower International
        windpower_config = {
            'company_name': 'WindPower International',
            'company_description': 'Advanced wind energy solutions across Africa',
            'address': 'Cape Town Energy Hub, South Africa',
            'country': 'South Africa',
            'currency': 'ZAR',
            'timezone': 'Africa/Johannesburg',
            'brand_color_primary': '#2196F3',
            'brand_color_secondary': '#03A9F4',
            'renewable_types': ['wind', 'solar'],
            'grid_voltage': 230,
            'grid_frequency': 50,
            'customer_segments': ['residential', 'commercial', 'industrial'],
            'capacity_mw': 87.3,
            'enable_lstm_models': True,
            'enable_prophet_models': True,
            'forecast_horizon_hours': 24
        }
        
        # Demo Company 3: GreenGrid Energy
        greengrid_config = {
            'company_name': 'GreenGrid Energy',
            'company_description': 'Sustainable energy grid solutions for Ghana',
            'address': 'Accra Business District, Ghana',
            'country': 'Ghana',
            'currency': 'GHS',
            'timezone': 'Africa/Accra',
            'brand_color_primary': '#4CAF50',
            'brand_color_secondary': '#8BC34A',
            'renewable_types': ['solar', 'wind', 'biomass'],
            'grid_voltage': 230,
            'grid_frequency': 50,
            'customer_segments': ['residential', 'commercial', 'industrial', 'community'],
            'capacity_mw': 92.7,
            'enable_lstm_models': True,
            'enable_prophet_models': True,
            'forecast_horizon_hours': 24
        }
        
        # OnePower Lesotho (original)
        onepower_config = {
            'company_name': 'OnePower Lesotho',
            'company_description': 'Renewable energy solutions for Lesotho',
            'address': 'Maseru Central, Lesotho',
            'country': 'Lesotho',
            'currency': 'LSL',
            'timezone': 'Africa/Maseru',
            'brand_color_primary': '#2E7D32',
            'brand_color_secondary': '#4CAF50',
            'renewable_types': ['solar', 'wind'],
            'grid_voltage': 230,
            'grid_frequency': 50,
            'customer_segments': ['residential', 'commercial', 'industrial'],
            'capacity_mw': 65.2,
            'enable_lstm_models': True,
            'enable_prophet_models': True,
            'forecast_horizon_hours': 24
        }
        
        self.companies['solartech'] = CompanyConfig('solartech', solartech_config)
        self.companies['windpower'] = CompanyConfig('windpower', windpower_config)
        self.companies['greengrid'] = CompanyConfig('greengrid', greengrid_config)
        self.companies['onepower'] = CompanyConfig('onepower', onepower_config)
        
        # Set default to onepower for backward compatibility
        self.default_company_id = 'onepower'
    
    def get_company(self, company_id: Optional[str] = None) -> CompanyConfig:
        """Get company configuration by ID"""
        if not company_id:
            company_id = self.default_company_id
        
        return self.companies.get(company_id, self.companies[self.default_company_id])
    
    def get_all_companies(self) -> Dict[str, CompanyConfig]:
        """Get all company configurations"""
        return self.companies
    
    def add_company(self, company_id: str, config_data: Dict[str, Any]) -> bool:
        """Add a new company configuration"""
        try:
            self.companies[company_id] = CompanyConfig(company_id, config_data)
            return True
        except Exception as e:
            print(f"Error adding company {company_id}: {e}")
            return False
    
    def save_companies_config(self, file_path: str = 'companies.json') -> bool:
        """Save current company configurations to file"""
        try:
            companies_data = {}
            for company_id, company_config in self.companies.items():
                companies_data[company_id] = {
                    'company_name': company_config.company_name,
                    'company_description': company_config.company_description,
                    'address': company_config.address,
                    'country': company_config.country,
                    'currency': company_config.currency,
                    'timezone': company_config.timezone,
                    'brand_color_primary': company_config.brand_color_primary,
                    'brand_color_secondary': company_config.brand_color_secondary,
                    'logo_url': company_config.logo_url,
                    'website_url': company_config.website_url,
                    'grid_voltage': company_config.grid_voltage,
                    'grid_frequency': company_config.grid_frequency,
                    'renewable_types': company_config.renewable_types,
                    'customer_segments': company_config.customer_segments,
                    'tariff_structure': company_config.tariff_structure,
                    'capacity_mw': company_config.capacity_mw,
                    'forecast_horizon_hours': company_config.forecast_horizon_hours,
                    'prediction_interval_minutes': company_config.prediction_interval_minutes,
                    'enable_lstm_models': company_config.enable_lstm_models,
                    'enable_prophet_models': company_config.enable_prophet_models,
                    'dashboard_refresh_seconds': company_config.dashboard_refresh_seconds,
                    'show_executive_dashboard': company_config.show_executive_dashboard,
                    'custom_kpis': company_config.custom_kpis
                }
            
            with open(file_path, 'w') as f:
                json.dump(companies_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving companies config: {e}")
            return False


class PowerAIConfig:
    """Enhanced Flask configuration with multi-tenant support"""
    
    def __init__(self):
        self.multi_tenant = MultiTenantConfig()
    
    # Base Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'sqlite:///powerai_multi_tenant.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-string')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM = 'HS256'
    
    # Redis Configuration
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # Celery Configuration
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', REDIS_URL)
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', REDIS_URL)
    
    # AI/ML Configuration
    MODEL_DATA_PATH = os.environ.get('MODEL_DATA_PATH', 'data/models/')
    TRAINING_DATA_PATH = os.environ.get('TRAINING_DATA_PATH', 'data/training/')
    ENABLE_AI_TRAINING = os.environ.get('ENABLE_AI_TRAINING', 'true').lower() == 'true'
    
    # API Configuration
    API_RATE_LIMIT = os.environ.get('API_RATE_LIMIT', '1000 per hour')
    API_VERSION = '1.0'
    ENABLE_API_DOCS = os.environ.get('ENABLE_API_DOCS', 'true').lower() == 'true'
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = {'csv', 'json', 'xlsx'}
    
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # External API Keys
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'powerai.log')
    
    # Security Configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Multi-tenant Configuration
    ENABLE_MULTI_TENANT = os.environ.get('ENABLE_MULTI_TENANT', 'true').lower() == 'true'
    DEFAULT_COMPANY_ID = os.environ.get('DEFAULT_COMPANY_ID', 'onepower')
    COMPANY_ISOLATION_ENABLED = os.environ.get('COMPANY_ISOLATION_ENABLED', 'true').lower() == 'true'
    
    @classmethod
    def get_company_config(cls, company_id: Optional[str] = None) -> CompanyConfig:
        """Get company-specific configuration"""
        if not hasattr(cls, '_multi_tenant'):
            cls._multi_tenant = MultiTenantConfig()
        return cls._multi_tenant.get_company(company_id)


class DevelopmentConfig(PowerAIConfig):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
    # Override for development
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL',
        'sqlite:///powerai_dev.db'
    )


class TestingConfig(PowerAIConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    
    # Use in-memory database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    
    # Disable external services during testing
    ENABLE_AI_TRAINING = False
    REDIS_URL = 'redis://localhost:6379/1'  # Different Redis DB


class ProductionConfig(PowerAIConfig):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Production database (must be set via environment variable)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Enhanced security for production
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_ENABLED = True
    
    # Production logging
    LOG_LEVEL = 'WARNING'


# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(config_name: str = None) -> PowerAIConfig:
    """Get configuration class by name"""
    if not config_name:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config_map.get(config_name, config_map['default'])