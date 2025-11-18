#!/usr/bin/env python3
"""
Enhanced PowerAI Demand Forecasting Engine
==========================================

Comprehensive energy demand forecasting system implementing multiple state-of-the-art
time-series models for UN SDG 7: Affordable and Clean Energy objectives.

Features:
- ARIMA (AutoRegressive Integrated Moving Average)
- Prophet (Facebook's time series forecasting)
- LSTM (Long Short-Term Memory neural networks)
- Ensemble methods combining multiple models
- 24-hour ahead forecasting
- Building and grid-level predictions
- Weather-aware forecasting
- Renewable energy integration optimization
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Union
import logging
import warnings
import joblib
from dataclasses import dataclass

# Traditional ML and statistical models
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

# Prophet for time series forecasting
try:
    from prophet import Prophet
    from prophet.diagnostics import cross_validation, performance_metrics
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    logging.warning("Prophet not available. Facebook Prophet models will be disabled.")

# Pre-trained model loader
try:
    from pretrained_models import PreTrainedModelLoader
    PRETRAINED_MODELS_AVAILABLE = True
except ImportError:
    PRETRAINED_MODELS_AVAILABLE = False
    logging.warning("Pre-trained model loader not available. Will fall back to training models.")

# TensorFlow/Keras for deep learning
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential, Model
    from tensorflow.keras.layers import LSTM, Dense, Dropout, Conv1D, MaxPooling1D, Flatten, Input
    from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
    try:
        from tensorflow.keras.optimizers import Adam
    except ImportError:
        from tensorflow.keras.optimizers.legacy import Adam
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    logging.warning("TensorFlow not available. LSTM models will be disabled.")

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


@dataclass
class ForecastResult:
    """Data class for forecast results"""
    timestamp: datetime
    predicted_demand: float
    confidence_lower: float
    confidence_upper: float
    model_used: str
    horizon_hours: int
    location: str = "default"
    renewable_contribution: float = 0.0
    grid_stability_score: float = 1.0


@dataclass
class ModelPerformance:
    """Data class for model performance metrics"""
    model_name: str
    mae: float  # Mean Absolute Error
    rmse: float  # Root Mean Square Error
    mape: float  # Mean Absolute Percentage Error
    r2: float  # R-squared
    training_time: float
    prediction_time: float


class AdvancedFeatureEngineering:
    """Advanced feature engineering for energy demand forecasting"""
    
    @staticmethod
    def create_temporal_features(df: pd.DataFrame, timestamp_col: str = 'timestamp') -> pd.DataFrame:
        """Create comprehensive temporal features"""
        df = df.copy()
        df[timestamp_col] = pd.to_datetime(df[timestamp_col])
        
        # Basic temporal features
        df['hour'] = df[timestamp_col].dt.hour
        df['day_of_week'] = df[timestamp_col].dt.dayofweek
        df['day_of_month'] = df[timestamp_col].dt.day
        df['month'] = df[timestamp_col].dt.month
        df['quarter'] = df[timestamp_col].dt.quarter
        df['year'] = df[timestamp_col].dt.year
        df['week_of_year'] = df[timestamp_col].dt.isocalendar().week
        
        # Cyclical encoding for periodic features
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        
        # Business calendar features
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        df['is_business_hour'] = ((df['hour'] >= 9) & (df['hour'] <= 17) & ~df['is_weekend']).astype(int)
        df['is_peak_hour'] = df['hour'].isin([17, 18, 19, 20]).astype(int)
        df['is_night'] = ((df['hour'] >= 22) | (df['hour'] <= 6)).astype(int)
        
        # Seasonal indicators
        df['is_summer'] = df['month'].isin([12, 1, 2]).astype(int)  # Southern hemisphere
        df['is_winter'] = df['month'].isin([6, 7, 8]).astype(int)
        
        return df
    
    @staticmethod
    def create_lag_features(df: pd.DataFrame, target_col: str, lags: List[int]) -> pd.DataFrame:
        """Create lag features for target variable"""
        df = df.copy()
        for lag in lags:
            df[f'{target_col}_lag_{lag}'] = df[target_col].shift(lag)
        return df
    
    @staticmethod
    def create_rolling_features(df: pd.DataFrame, target_col: str, windows: List[int]) -> pd.DataFrame:
        """Create rolling statistical features"""
        df = df.copy()
        for window in windows:
            df[f'{target_col}_rolling_mean_{window}'] = df[target_col].rolling(window=window, min_periods=1).mean()
            df[f'{target_col}_rolling_std_{window}'] = df[target_col].rolling(window=window, min_periods=1).std()
            df[f'{target_col}_rolling_min_{window}'] = df[target_col].rolling(window=window, min_periods=1).min()
            df[f'{target_col}_rolling_max_{window}'] = df[target_col].rolling(window=window, min_periods=1).max()
        return df
    
    @staticmethod
    def create_weather_features(df: pd.DataFrame) -> pd.DataFrame:
        """Create weather-based features for energy demand"""
        df = df.copy()
        
        if 'temperature' in df.columns:
            # Temperature-based features
            df['temp_squared'] = df['temperature'] ** 2
            df['cooling_degree_days'] = np.maximum(df['temperature'] - 18, 0)  # Base 18°C
            df['heating_degree_days'] = np.maximum(18 - df['temperature'], 0)
            
            # Temperature categories
            df['is_hot'] = (df['temperature'] > 25).astype(int)
            df['is_cold'] = (df['temperature'] < 10).astype(int)
            df['is_moderate'] = ((df['temperature'] >= 10) & (df['temperature'] <= 25)).astype(int)
        
        if 'humidity' in df.columns:
            df['humidity_temp_interaction'] = df.get('temperature', 20) * df['humidity'] / 100
        
        if 'wind_speed' in df.columns:
            df['wind_power_potential'] = df['wind_speed'] ** 3  # Wind power is proportional to wind speed cubed
        
        if 'solar_irradiance' in df.columns:
            df['solar_power_potential'] = df['solar_irradiance'] / 1000  # Normalize to kW/m²
            df['daylight_indicator'] = (df['solar_irradiance'] > 50).astype(int)
        
        return df


class ARIMAForecaster:
    """ARIMA (AutoRegressive Integrated Moving Average) forecaster"""
    
    def __init__(self):
        self.model = None
        self.order = None
        self.seasonal_order = None
        self.is_fitted = False
    
    def find_optimal_order(self, series: pd.Series, max_p: int = 5, max_d: int = 2, max_q: int = 5) -> Tuple[int, int, int]:
        """Find optimal ARIMA order using AIC criterion"""
        best_aic = float('inf')
        best_order = (1, 1, 1)
        
        # Check stationarity
        adf_result = adfuller(series.dropna())
        if adf_result[1] > 0.05:  # Non-stationary
            d_range = range(1, max_d + 1)
        else:
            d_range = range(0, max_d + 1)
        
        for p in range(0, max_p + 1):
            for d in d_range:
                for q in range(0, max_q + 1):
                    if p == 0 and d == 0 and q == 0:
                        continue
                    
                    try:
                        model = ARIMA(series, order=(p, d, q))
                        fitted_model = model.fit()
                        
                        if fitted_model.aic < best_aic:
                            best_aic = fitted_model.aic
                            best_order = (p, d, q)
                    except:
                        continue
        
        return best_order
    
    def fit(self, series: pd.Series) -> Dict:
        """Fit ARIMA model to time series"""
        try:
            # Find optimal order if not specified
            if self.order is None:
                self.order = self.find_optimal_order(series)
            
            self.model = ARIMA(series, order=self.order)
            self.fitted_model = self.model.fit()
            self.is_fitted = True
            
            return {
                'order': self.order,
                'aic': self.fitted_model.aic,
                'bic': self.fitted_model.bic,
                'success': True
            }
        except Exception as e:
            logger.error(f"ARIMA fitting failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def forecast(self, steps: int = 24) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Generate forecasts with confidence intervals"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before forecasting")
        
        forecast_result = self.fitted_model.forecast(steps=steps, alpha=0.05)  # 95% confidence
        
        forecasts = forecast_result
        conf_int = self.fitted_model.get_forecast(steps=steps).conf_int()
        
        return forecasts, conf_int.iloc[:, 0].values, conf_int.iloc[:, 1].values


class ProphetForecaster:
    """Facebook Prophet forecaster for time series with seasonality"""
    
    def __init__(self, yearly_seasonality: bool = True, weekly_seasonality: bool = True, 
                 daily_seasonality: bool = True):
        if not PROPHET_AVAILABLE:
            raise ImportError("Prophet is not available. Install with: pip install prophet")
        
        self.model = Prophet(
            yearly_seasonality=yearly_seasonality,
            weekly_seasonality=weekly_seasonality,
            daily_seasonality=daily_seasonality,
            interval_width=0.95
        )
        self.is_fitted = False
    
    def add_custom_seasonalities(self):
        """Add custom seasonalities relevant to energy demand"""
        # Business hours seasonality
        self.model.add_seasonality(name='business_hours', period=1, fourier_order=3)
        
        # Monthly seasonality for billing cycles
        self.model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    
    def fit(self, df: pd.DataFrame, target_col: str = 'consumption_kwh', 
            timestamp_col: str = 'timestamp') -> Dict:
        """Fit Prophet model"""
        try:
            # Prepare data in Prophet format
            prophet_df = df[[timestamp_col, target_col]].copy()
            prophet_df.columns = ['ds', 'y']
            prophet_df = prophet_df.dropna()
            
            # Add custom seasonalities
            self.add_custom_seasonalities()
            
            # Add external regressors if available
            if 'temperature' in df.columns:
                prophet_df['temperature'] = df['temperature']
                self.model.add_regressor('temperature')
            
            if 'humidity' in df.columns:
                prophet_df['humidity'] = df['humidity']
                self.model.add_regressor('humidity')
            
            # Generate synthetic weather data if not available
            if 'temperature' not in df.columns:
                # Generate realistic temperature patterns for Lesotho climate
                dates = pd.to_datetime(prophet_df['ds'])
                day_of_year = dates.dt.dayofyear
                hour_of_day = dates.dt.hour if hasattr(dates.dt, 'hour') else 12
                
                # Seasonal temperature pattern (Southern Hemisphere)
                seasonal_temp = 15 + 10 * np.sin(2 * np.pi * (day_of_year - 80) / 365)
                # Daily temperature variation
                daily_temp = 5 * np.sin(2 * np.pi * hour_of_day / 24)
                # Add some random noise
                noise = np.random.normal(0, 2, len(prophet_df))
                
                prophet_df['temperature'] = seasonal_temp + daily_temp + noise
                self.model.add_regressor('temperature')
            
            self.model.fit(prophet_df)
            self.is_fitted = True
            
            return {'success': True, 'components': self.model.seasonalities}
            
        except Exception as e:
            logger.error(f"Prophet fitting failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def forecast(self, periods: int = 24, freq: str = 'H') -> pd.DataFrame:
        """Generate forecasts"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before forecasting")
        
        future = self.model.make_future_dataframe(periods=periods, freq=freq)
        
        # Add regressor data for future periods if regressors were used
        if 'temperature' in [regressor for regressor in getattr(self.model, 'extra_regressors', {}).keys()]:
            # Generate synthetic temperature data for future periods
            dates = pd.to_datetime(future['ds'])
            day_of_year = dates.dt.dayofyear
            hour_of_day = dates.dt.hour if hasattr(dates.dt, 'hour') else 12
            
            # Seasonal temperature pattern (Southern Hemisphere)
            seasonal_temp = 15 + 10 * np.sin(2 * np.pi * (day_of_year - 80) / 365)
            # Daily temperature variation
            daily_temp = 5 * np.sin(2 * np.pi * hour_of_day / 24)
            # Add some random noise for future predictions
            noise = np.random.normal(0, 1, len(future))  # Less noise for predictions
            
            future['temperature'] = seasonal_temp + daily_temp + noise
        
        if 'humidity' in [regressor for regressor in getattr(self.model, 'extra_regressors', {}).keys()]:
            # Generate synthetic humidity data correlated with temperature
            base_humidity = 60 + 20 * np.sin(2 * np.pi * dates.dt.dayofyear / 365)
            daily_humidity = -10 * np.sin(2 * np.pi * dates.dt.hour / 24)  # Lower during day
            humidity_noise = np.random.normal(0, 5, len(future))
            future['humidity'] = np.clip(base_humidity + daily_humidity + humidity_noise, 20, 90)
        
        forecast = self.model.predict(future)
        
        return forecast.tail(periods)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]


class LSTMForecaster:
    """LSTM neural network forecaster for complex patterns"""
    
    def __init__(self, sequence_length: int = 24, lstm_units: List[int] = [128, 64], 
                 dropout_rate: float = 0.2):
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow is not available")
        
        self.sequence_length = sequence_length
        self.lstm_units = lstm_units
        self.dropout_rate = dropout_rate
        self.model = None
        self.scaler_X = StandardScaler()
        self.scaler_y = MinMaxScaler()
        self.is_fitted = False
    
    def create_sequences(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Create sequences for LSTM training"""
        X_seq, y_seq = [], []
        
        for i in range(self.sequence_length, len(X)):
            X_seq.append(X[i-self.sequence_length:i])
            y_seq.append(y[i])
        
        return np.array(X_seq), np.array(y_seq)
    
    def build_model(self, n_features: int) -> Model:
        """Build LSTM architecture"""
        model = Sequential()
        
        # First LSTM layer
        model.add(LSTM(self.lstm_units[0], return_sequences=True, 
                      input_shape=(self.sequence_length, n_features)))
        model.add(Dropout(self.dropout_rate))
        
        # Additional LSTM layers
        for units in self.lstm_units[1:]:
            model.add(LSTM(units, return_sequences=len(self.lstm_units) > 2))
            model.add(Dropout(self.dropout_rate))
        
        # Dense layers
        model.add(Dense(50, activation='relu'))
        model.add(Dense(1, activation='linear'))
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def fit(self, X: np.ndarray, y: np.ndarray, validation_split: float = 0.2, 
            epochs: int = 100, batch_size: int = 32) -> Dict:
        """Fit LSTM model"""
        try:
            # Scale features
            X_scaled = self.scaler_X.fit_transform(X)
            y_scaled = self.scaler_y.fit_transform(y.reshape(-1, 1)).flatten()
            
            # Create sequences
            X_seq, y_seq = self.create_sequences(X_scaled, y_scaled)
            
            if len(X_seq) < 50:  # Not enough data
                return {'success': False, 'error': 'Insufficient data for LSTM training'}
            
            # Build model
            self.model = self.build_model(X_seq.shape[2])
            
            # Callbacks
            early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
            reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6)
            
            # Train model
            history = self.model.fit(
                X_seq, y_seq,
                validation_split=validation_split,
                epochs=epochs,
                batch_size=batch_size,
                callbacks=[early_stopping, reduce_lr],
                verbose=0
            )
            
            self.is_fitted = True
            
            return {
                'success': True,
                'final_loss': history.history['loss'][-1],
                'final_val_loss': history.history['val_loss'][-1],
                'epochs_trained': len(history.history['loss'])
            }
            
        except Exception as e:
            logger.error(f"LSTM fitting failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def forecast(self, X: np.ndarray, steps: int = 24) -> np.ndarray:
        """Generate LSTM forecasts"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before forecasting")
        
        # Scale input
        X_scaled = self.scaler_X.transform(X)
        
        # Get last sequence
        last_sequence = X_scaled[-self.sequence_length:].reshape(1, self.sequence_length, -1)
        
        forecasts = []
        current_sequence = last_sequence.copy()
        
        for _ in range(steps):
            # Predict next step
            pred_scaled = self.model.predict(current_sequence, verbose=0)[0, 0]
            pred = self.scaler_y.inverse_transform([[pred_scaled]])[0, 0]
            forecasts.append(pred)
            
            # Update sequence (simplified - in practice, you'd update with new features)
            current_sequence = np.roll(current_sequence, -1, axis=1)
            current_sequence[0, -1, 0] = pred_scaled  # Update only target variable
        
        return np.array(forecasts)


class EnsembleForecaster:
    """Ensemble forecaster combining multiple models"""
    
    def __init__(self, models: Dict[str, object], weights: Optional[Dict[str, float]] = None):
        self.models = models
        self.weights = weights or {name: 1.0 for name in models.keys()}
        self.performance_history = {}
        self.adaptive_weights = False
        
    def enable_adaptive_weighting(self):
        """Enable adaptive weighting based on recent performance"""
        self.adaptive_weights = True
    
    def update_weights_by_performance(self, performances: Dict[str, float]):
        """Update weights based on model performances (lower error = higher weight)"""
        if not performances:
            return
        
        # Convert errors to weights (inverse relationship)
        total_inverse_error = sum(1 / (error + 1e-8) for error in performances.values())
        
        for model_name, error in performances.items():
            self.weights[model_name] = (1 / (error + 1e-8)) / total_inverse_error
    
    def combine_forecasts(self, forecasts: Dict[str, np.ndarray]) -> np.ndarray:
        """Combine forecasts using weighted average"""
        if not forecasts:
            raise ValueError("No forecasts to combine")
        
        # Normalize weights
        total_weight = sum(self.weights[name] for name in forecasts.keys() if name in self.weights)
        
        combined = np.zeros_like(list(forecasts.values())[0])
        
        for model_name, forecast in forecasts.items():
            weight = self.weights.get(model_name, 0) / total_weight
            combined += weight * forecast
        
        return combined
    
    def get_confidence_intervals(self, forecasts: Dict[str, np.ndarray], 
                               confidence_intervals: Dict[str, Tuple[np.ndarray, np.ndarray]]) -> Tuple[np.ndarray, np.ndarray]:
        """Combine confidence intervals from multiple models"""
        if not confidence_intervals:
            # Simple approach: use 10% of forecast as confidence interval
            combined_forecast = self.combine_forecasts(forecasts)
            margin = 0.1 * np.abs(combined_forecast)
            return combined_forecast - margin, combined_forecast + margin
        
        # Weighted combination of confidence intervals
        lower_bounds = []
        upper_bounds = []
        
        for model_name, (lower, upper) in confidence_intervals.items():
            if model_name in self.weights:
                weight = self.weights[model_name]
                lower_bounds.append(weight * lower)
                upper_bounds.append(weight * upper)
        
        return np.sum(lower_bounds, axis=0), np.sum(upper_bounds, axis=0)


class ComprehensiveDemandForecaster:
    """Main comprehensive demand forecasting system for SDG 7 implementation"""
    
    def __init__(self, company_config: Optional[object] = None):
        self.company_config = company_config
        self.models = {}
        self.ensemble = None
        self.feature_columns = []
        self.performance_metrics = {}
        self.is_trained = False
        self.last_training_date = None
        
        # Pre-trained model loader
        self.pretrained_loader = None
        if PRETRAINED_MODELS_AVAILABLE:
            try:
                self.pretrained_loader = PreTrainedModelLoader()
                logger.info("Pre-trained model loader initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize pre-trained model loader: {e}")
                self.pretrained_loader = None
        
        # Initialize models based on configuration
        self.enable_arima = True
        self.enable_prophet = PROPHET_AVAILABLE and (company_config is None or 
                                                    getattr(company_config, 'enable_prophet_models', True))
        self.enable_lstm = TENSORFLOW_AVAILABLE and (company_config is None or 
                                                    getattr(company_config, 'enable_lstm_models', True))
        
        logger.info(f"Initialized forecaster - ARIMA: {self.enable_arima}, "
                   f"Prophet: {self.enable_prophet}, LSTM: {self.enable_lstm}, "
                   f"Pre-trained: {self.pretrained_loader is not None}")
    
    def prepare_comprehensive_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare comprehensive feature set for forecasting"""
        logger.info("Preparing comprehensive features for demand forecasting...")
        
        df = df.copy()
        
        # Temporal features
        df = AdvancedFeatureEngineering.create_temporal_features(df)
        
        # Lag features for energy consumption
        if 'consumption_kwh' in df.columns:
            df = AdvancedFeatureEngineering.create_lag_features(
                df, 'consumption_kwh', [1, 2, 3, 6, 12, 24, 48, 168]  # Various lags
            )
            
            # Rolling features
            df = AdvancedFeatureEngineering.create_rolling_features(
                df, 'consumption_kwh', [6, 12, 24, 48, 168]  # Various windows
            )
        
        # Weather features
        df = AdvancedFeatureEngineering.create_weather_features(df)
        
        # Renewable generation features if available
        if 'renewable_generation' in df.columns:
            df = AdvancedFeatureEngineering.create_lag_features(
                df, 'renewable_generation', [1, 6, 12, 24]
            )
        
        return df
    
    def train_all_models(self, df: pd.DataFrame, target_column: str = 'consumption_kwh') -> Dict:
        """Train all available forecasting models"""
        logger.info("Training comprehensive forecasting models...")
        
        # Prepare features
        df = self.prepare_comprehensive_features(df)
        df = df.dropna()
        
        if len(df) < 100:
            raise ValueError("Insufficient data for training (need at least 100 samples)")
        
        training_results = {}
        
        # Prepare data splits
        split_idx = int(len(df) * 0.8)
        train_df = df.iloc[:split_idx]
        test_df = df.iloc[split_idx:]
        
        # Feature columns (excluding target and identifiers)
        exclude_cols = [target_column, 'timestamp', 'id', 'customer_id', 'created_at']
        self.feature_columns = [col for col in df.columns if col not in exclude_cols]
        
        X_train = train_df[self.feature_columns].fillna(0)
        y_train = train_df[target_column]
        X_test = test_df[self.feature_columns].fillna(0)
        y_test = test_df[target_column]
        
        # Train ARIMA
        if self.enable_arima:
            logger.info("Training ARIMA model...")
            try:
                arima_forecaster = ARIMAForecaster()
                arima_result = arima_forecaster.fit(y_train)
                
                if arima_result['success']:
                    self.models['arima'] = arima_forecaster
                    
                    # Make predictions
                    forecasts, lower, upper = arima_forecaster.forecast(len(y_test))
                    
                    # Calculate metrics
                    mae = mean_absolute_error(y_test, forecasts)
                    rmse = np.sqrt(mean_squared_error(y_test, forecasts))
                    mape = mean_absolute_percentage_error(y_test, forecasts)
                    r2 = r2_score(y_test, forecasts)
                    
                    training_results['arima'] = ModelPerformance(
                        'arima', mae, rmse, mape, r2, 0, 0
                    )
                    
                    logger.info(f"ARIMA - MAE: {mae:.2f}, RMSE: {rmse:.2f}, MAPE: {mape:.4f}")
                    
            except Exception as e:
                logger.error(f"ARIMA training failed: {e}")
        
        # Train Prophet
        if self.enable_prophet:
            logger.info("Training Prophet model...")
            try:
                prophet_forecaster = ProphetForecaster()
                prophet_result = prophet_forecaster.fit(train_df, target_column)
                
                if prophet_result['success']:
                    self.models['prophet'] = prophet_forecaster
                    
                    # Make predictions
                    prophet_forecast = prophet_forecaster.forecast(len(y_test))
                    forecasts = prophet_forecast['yhat'].values
                    
                    # Calculate metrics
                    mae = mean_absolute_error(y_test, forecasts)
                    rmse = np.sqrt(mean_squared_error(y_test, forecasts))
                    mape = mean_absolute_percentage_error(y_test, forecasts)
                    r2 = r2_score(y_test, forecasts)
                    
                    training_results['prophet'] = ModelPerformance(
                        'prophet', mae, rmse, mape, r2, 0, 0
                    )
                    
                    logger.info(f"Prophet - MAE: {mae:.2f}, RMSE: {rmse:.2f}, MAPE: {mape:.4f}")
                    
            except Exception as e:
                logger.error(f"Prophet training failed: {e}")
        
        # Train LSTM
        if self.enable_lstm:
            logger.info("Training LSTM model...")
            try:
                lstm_forecaster = LSTMForecaster(sequence_length=min(24, len(X_train)//4))
                lstm_result = lstm_forecaster.fit(X_train.values, y_train.values)
                
                if lstm_result['success']:
                    self.models['lstm'] = lstm_forecaster
                    
                    # Make predictions
                    forecasts = lstm_forecaster.forecast(X_test.values, len(y_test))
                    
                    # Calculate metrics
                    mae = mean_absolute_error(y_test, forecasts)
                    rmse = np.sqrt(mean_squared_error(y_test, forecasts))
                    mape = mean_absolute_percentage_error(y_test, forecasts)
                    r2 = r2_score(y_test, forecasts)
                    
                    training_results['lstm'] = ModelPerformance(
                        'lstm', mae, rmse, mape, r2, 0, 0
                    )
                    
                    logger.info(f"LSTM - MAE: {mae:.2f}, RMSE: {rmse:.2f}, MAPE: {mape:.4f}")
                    
            except Exception as e:
                logger.error(f"LSTM training failed: {e}")
        
        # Create ensemble
        if self.models:
            # Calculate weights based on performance (inverse of MAE)
            weights = {}
            for model_name, performance in training_results.items():
                weights[model_name] = 1.0 / (performance.mae + 1e-8)
            
            # Normalize weights
            total_weight = sum(weights.values())
            weights = {k: v/total_weight for k, v in weights.items()}
            
            self.ensemble = EnsembleForecaster(self.models, weights)
            
            logger.info(f"Ensemble weights: {weights}")
        
        self.performance_metrics = training_results
        self.is_trained = True
        self.last_training_date = datetime.now()
        
        logger.info("Training completed successfully!")
        return training_results
    
    def predict_24h_demand(self, recent_data: pd.DataFrame, 
                          location: str = "default") -> List[ForecastResult]:
        """Generate 24-hour ahead demand forecasts - core SDG 7 feature"""
        
        # Try pre-trained models first for faster predictions
        if self.pretrained_loader and self.pretrained_loader.models_available():
            logger.info("Using pre-trained models for fast predictions...")
            try:
                predictions = self.pretrained_loader.predict_24h_ahead(recent_data.copy())
                
                # Convert to ForecastResult format
                results = []
                current_time = datetime.now()
                
                for i, pred in enumerate(predictions):
                    forecast_time = current_time + timedelta(hours=i+1)
                    
                    # Use ensemble prediction if available, otherwise use the prediction value
                    if isinstance(pred, dict) and 'ensemble' in pred:
                        predicted_demand = pred['ensemble']
                        confidence_lower = predicted_demand * 0.95  # Simple confidence bounds
                        confidence_upper = predicted_demand * 1.05
                        model_used = "pretrained_ensemble"
                    else:
                        predicted_demand = float(pred)
                        confidence_lower = predicted_demand * 0.95
                        confidence_upper = predicted_demand * 1.05
                        model_used = "pretrained"
                    
                    results.append(ForecastResult(
                        timestamp=forecast_time,
                        predicted_demand=predicted_demand,
                        confidence_lower=confidence_lower,
                        confidence_upper=confidence_upper,
                        model_used=model_used,
                        horizon_hours=i+1,
                        location=location,
                        renewable_contribution=0.3,  # Default SDG 7 target
                        grid_stability_score=0.95
                    ))
                
                logger.info(f"Generated {len(results)} pre-trained forecasts successfully")
                return results
                
            except Exception as e:
                logger.warning(f"Pre-trained model prediction failed: {e}, falling back to training")
        
        # Fall back to training models if pre-trained models aren't available
        if not self.is_trained:
            logger.info("No pre-trained models available, training models...")
            # Generate synthetic data for training if no real data is available
            if recent_data.empty or len(recent_data) < 24:
                synthetic_data = self._generate_synthetic_training_data()
                self.train_all_models(synthetic_data, target_column='demand')
            else:
                # Use recent data for quick training
                extended_data = self._extend_data_for_training(recent_data)
                self.train_all_models(extended_data, target_column='demand')
        
        logger.info("Generating 24-hour demand forecasts using trained models...")
        
        # Prepare features
        data = self.prepare_comprehensive_features(recent_data)
        
        # Generate forecasts from all models
        model_forecasts = {}
        confidence_intervals = {}
        
        current_time = datetime.now()
        
        # ARIMA forecasts
        if 'arima' in self.models:
            try:
                forecasts, lower, upper = self.models['arima'].forecast(24)
                model_forecasts['arima'] = forecasts
                confidence_intervals['arima'] = (lower, upper)
            except Exception as e:
                logger.warning(f"ARIMA prediction failed: {e}")
        
        # Prophet forecasts
        if 'prophet' in self.models:
            try:
                prophet_forecast = self.models['prophet'].forecast(24)
                model_forecasts['prophet'] = prophet_forecast['yhat'].values
                confidence_intervals['prophet'] = (
                    prophet_forecast['yhat_lower'].values,
                    prophet_forecast['yhat_upper'].values
                )
            except Exception as e:
                logger.warning(f"Prophet prediction failed: {e}")
        
        # LSTM forecasts
        if 'lstm' in self.models:
            try:
                X = data[self.feature_columns].fillna(0).tail(48)  # Use recent data
                forecasts = self.models['lstm'].forecast(X.values, 24)
                model_forecasts['lstm'] = forecasts
                # Simple confidence interval for LSTM
                margin = 0.1 * np.abs(forecasts)
                confidence_intervals['lstm'] = (forecasts - margin, forecasts + margin)
            except Exception as e:
                logger.warning(f"LSTM prediction failed: {e}")
        
        if not model_forecasts:
            raise RuntimeError("No models available for prediction")
        
        # Combine forecasts using ensemble
        final_forecasts = self.ensemble.combine_forecasts(model_forecasts)
        lower_bounds, upper_bounds = self.ensemble.get_confidence_intervals(
            model_forecasts, confidence_intervals
        )
        
        # Create forecast results
        results = []
        for i in range(24):
            timestamp = current_time + timedelta(hours=i+1)
            
            # Calculate renewable contribution estimate (simplified)
            renewable_contribution = 0.2 if 6 <= timestamp.hour <= 18 else 0.05
            
            # Grid stability score (simplified)
            grid_stability = 0.95 if 8 <= timestamp.hour <= 22 else 0.98
            
            # Handle different forecast formats (list vs pandas Series)
            if isinstance(final_forecasts, list):
                forecast_value = final_forecasts[i]
                lower_value = lower_bounds[i] if len(lower_bounds) > i else forecast_value * 0.9
                upper_value = upper_bounds[i] if len(upper_bounds) > i else forecast_value * 1.1
            else:
                # pandas Series or similar
                forecast_value = final_forecasts.iloc[i] if hasattr(final_forecasts, 'iloc') else final_forecasts[i]
                lower_value = lower_bounds.iloc[i] if (hasattr(lower_bounds, 'iloc') and len(lower_bounds) > i) else forecast_value * 0.9
                upper_value = upper_bounds.iloc[i] if (hasattr(upper_bounds, 'iloc') and len(upper_bounds) > i) else forecast_value * 1.1
            
            result = ForecastResult(
                timestamp=timestamp,
                predicted_demand=float(forecast_value),
                confidence_lower=float(lower_value),
                confidence_upper=float(upper_value),
                model_used="ensemble",
                horizon_hours=i+1,
                location=location,
                renewable_contribution=renewable_contribution,
                grid_stability_score=grid_stability
            )
            
            results.append(result)
        
        logger.info(f"Generated 24-hour forecast for {location}")
        return results
    
    def _generate_synthetic_training_data(self) -> pd.DataFrame:
        """Generate synthetic training data when no historical data is available"""
        logger.info("Generating synthetic training data for fallback training...")
        
        # Generate 30 days of synthetic data
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=30),
            end=datetime.now(),
            freq='H'
        )
        
        # Create synthetic demand patterns
        synthetic_data = []
        for i, date in enumerate(dates):
            # Base demand with daily and weekly patterns
            hour = date.hour
            day_of_week = date.weekday()
            
            # Daily pattern (higher during day, lower at night)
            daily_pattern = 0.7 + 0.3 * np.sin(2 * np.pi * (hour - 6) / 24)
            
            # Weekly pattern (higher on weekdays)
            weekly_pattern = 1.0 if day_of_week < 5 else 0.8
            
            # Seasonal variation
            seasonal_pattern = 1.0 + 0.2 * np.sin(2 * np.pi * i / (24 * 7))
            
            # Add some noise
            noise = np.random.normal(0, 0.05)
            
            demand = 100 * daily_pattern * weekly_pattern * seasonal_pattern * (1 + noise)
            
            synthetic_data.append({
                'timestamp': date,
                'demand': max(demand, 10),  # Ensure positive demand
                'temperature': 20 + 10 * np.sin(2 * np.pi * hour / 24) + np.random.normal(0, 2),
                'humidity': 50 + 20 * np.random.random(),
                'renewable_generation': max(0, 30 * np.sin(2 * np.pi * (hour - 6) / 24) + np.random.normal(0, 5))
            })
        
        df = pd.DataFrame(synthetic_data)
        logger.info(f"Generated {len(df)} hours of synthetic training data")
        return df
    
    def _extend_data_for_training(self, recent_data: pd.DataFrame) -> pd.DataFrame:
        """Extend recent data with synthetic historical data for training"""
        logger.info("Extending recent data with synthetic historical data...")
        
        if len(recent_data) < 24:
            # Generate additional synthetic data
            synthetic_data = self._generate_synthetic_training_data()
            # Combine with recent data
            extended_data = pd.concat([synthetic_data, recent_data], ignore_index=True)
        else:
            extended_data = recent_data.copy()
        
        return extended_data
    
    def get_model_performance_summary(self) -> Dict:
        """Get comprehensive model performance summary"""
        return {
            'models_trained': list(self.models.keys()),
            'best_model': min(self.performance_metrics.items(), 
                            key=lambda x: x[1].mae)[0] if self.performance_metrics else None,
            'performance_metrics': self.performance_metrics,
            'ensemble_weights': self.ensemble.weights if self.ensemble else {},
            'last_training_date': self.last_training_date,
            'features_used': len(self.feature_columns),
            'pretrained_available': self.pretrained_loader is not None and self.pretrained_loader.models_available()
        }
    
    def optimize_renewable_integration(self, forecast_results: List[ForecastResult], 
                                     renewable_capacity: float) -> Dict:
        """Optimize renewable energy integration based on demand forecast"""
        total_demand = sum(r.predicted_demand for r in forecast_results)
        total_renewable_potential = sum(r.renewable_contribution * r.predicted_demand 
                                      for r in forecast_results)
        
        renewable_percentage = min(total_renewable_potential / total_demand * 100, 
                                 renewable_capacity / total_demand * 24 * 100)
        
        return {
            'total_demand_24h': total_demand,
            'renewable_potential_24h': total_renewable_potential,
            'renewable_percentage': renewable_percentage,
            'peak_demand_hour': max(forecast_results, key=lambda x: x.predicted_demand).timestamp.hour,
            'optimal_storage_charging_hours': [r.timestamp.hour for r in forecast_results 
                                             if r.renewable_contribution > 0.15],
            'grid_stability_avg': np.mean([r.grid_stability_score for r in forecast_results])
        }
    
    def save_model(self, filepath: str) -> bool:
        """Save the complete forecasting system"""
        try:
            model_data = {
                'feature_columns': self.feature_columns,
                'performance_metrics': self.performance_metrics,
                'last_training_date': self.last_training_date,
                'is_trained': self.is_trained,
                'company_config': self.company_config.__dict__ if self.company_config else None
            }
            
            # Save sklearn/statistical models
            joblib.dump(model_data, filepath)
            
            # Save deep learning models separately
            if 'lstm' in self.models:
                self.models['lstm'].model.save(filepath.replace('.pkl', '_lstm.h5'))
            
            logger.info(f"Comprehensive forecasting model saved to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            return False


# Export the main forecasting class
__all__ = ['ComprehensiveDemandForecaster', 'ForecastResult', 'ModelPerformance']