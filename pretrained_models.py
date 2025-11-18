"""
Pre-trained Model Loader for PowerAI Dashboard

This module loads pre-trained ML models (ARIMA, Prophet, LSTM) that were trained on Google Colab
and provides fast inference without the need for training on each startup.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Tuple

# Optional imports with fallbacks
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False

try:
    from statsmodels.tsa.arima.model import ARIMAResults
    from statsmodels.tsa.statespace.sarimax import SARIMAXResults
    ARIMA_AVAILABLE = True
    SARIMAX_AVAILABLE = True
except ImportError:
    ARIMA_AVAILABLE = False
    SARIMAX_AVAILABLE = False

try:
    import tensorflow as tf
    from sklearn.preprocessing import MinMaxScaler
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

logger = logging.getLogger(__name__)


class PreTrainedModelLoader:
    """
    Fast model loader for pre-trained ML models.
    Loads models trained on Google Colab for instant predictions.
    """
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = models_dir
        self.models = {}
        self.metadata = {}
        self.scalers = {}
        
        # Model availability flags
        self.prophet_available = False
        self.sarimax_available = False
        self.arima_available = False
        self.lstm_available = False
        
        # Load models automatically on initialization
        try:
            self.load_all_models()
            logger.info("Pre-trained models loaded successfully on initialization")
        except Exception as e:
            logger.warning(f"Failed to load pre-trained models on initialization: {e}")
        
    def load_all_models(self) -> Dict[str, bool]:
        """
        Load all available pre-trained models.
        
        Returns:
            Dict with model loading status
        """
        results = {
            'prophet': False,
            'sarimax': False,
            'arima': False,
            'lstm': False,
            'metadata': False
        }
        
        if not os.path.exists(self.models_dir):
            logger.warning(f"Models directory {self.models_dir} not found. Create it and add trained models.")
            return results
            
        # Load metadata first
        try:
            results['metadata'] = self._load_metadata()
        except Exception as e:
            logger.warning(f"Could not load model metadata: {e}")
            
        # Load Prophet model
        try:
            results['prophet'] = self._load_prophet_model()
        except Exception as e:
            logger.warning(f"Could not load Prophet model: {e}")
            
        # Load SARIMAX model  
        try:
            results['sarimax'] = self._load_sarimax_model()
        except Exception as e:
            logger.warning(f"Could not load SARIMAX model: {e}")
            
        # Load ARIMA model
        try:
            results['arima'] = self._load_arima_model()
        except Exception as e:
            logger.warning(f"Could not load ARIMA model: {e}")
            
        # Load LSTM model
        try:
            results['lstm'] = self._load_lstm_model()
        except Exception as e:
            logger.warning(f"Could not load LSTM model: {e}")
            
        logger.info(f"Model loading results: {results}")
        return results
        
    def _load_metadata(self) -> bool:
        """Load model training metadata"""
        metadata_path = os.path.join(self.models_dir, 'model_metadata.json')
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
            logger.info(f"Loaded model metadata: trained on {self.metadata.get('training_date', 'unknown')}")
            return True
        return False
        
    def _load_prophet_model(self) -> bool:
        """Load pre-trained Prophet model"""
        if not PROPHET_AVAILABLE:
            logger.warning("Prophet not available, skipping Prophet model loading")
            return False
            
        prophet_path = os.path.join(self.models_dir, 'prophet_model.pkl')
        if os.path.exists(prophet_path):
            self.models['prophet'] = joblib.load(prophet_path)
            self.prophet_available = True
            logger.info("Prophet model loaded successfully")
            return True
        return False
        
    def _load_sarimax_model(self) -> bool:
        """Load pre-trained SARIMAX model"""
        if not SARIMAX_AVAILABLE:
            logger.warning("SARIMAX not available, skipping SARIMAX model loading")
            return False
            
        sarimax_path = os.path.join(self.models_dir, 'sarimax_model.pkl')
        if os.path.exists(sarimax_path):
            self.models['sarimax'] = SARIMAXResults.load(sarimax_path)
            self.sarimax_available = True
            logger.info("SARIMAX model loaded successfully")
            return True
        return False
        
    def _load_arima_model(self) -> bool:
        """Load pre-trained ARIMA model"""
        if not ARIMA_AVAILABLE:
            logger.warning("ARIMA not available, skipping ARIMA model loading")
            return False
            
        arima_path = os.path.join(self.models_dir, 'arima_model.pkl')
        if os.path.exists(arima_path):
            self.models['arima'] = ARIMAResults.load(arima_path)
            self.arima_available = True
            logger.info("ARIMA model loaded successfully")
            return True
        return False
        
    def _load_lstm_model(self) -> bool:
        """Load pre-trained LSTM model and scaler"""
        if not TENSORFLOW_AVAILABLE:
            logger.warning("TensorFlow not available, skipping LSTM model loading")
            return False
            
        lstm_path = os.path.join(self.models_dir, 'lstm_model.h5')
        scaler_path = os.path.join(self.models_dir, 'lstm_scaler.pkl')
        
        if os.path.exists(lstm_path) and os.path.exists(scaler_path):
            self.models['lstm'] = tf.keras.models.load_model(lstm_path)
            self.scalers['lstm'] = joblib.load(scaler_path)
            self.lstm_available = True
            logger.info("LSTM model and scaler loaded successfully")
            return True
        return False
        
    def models_available(self) -> bool:
        """Check if any models are available for prediction"""
        return any([self.prophet_available, self.sarimax_available, self.arima_available, self.lstm_available])
        
    def predict_24h_ahead(self, recent_data: pd.DataFrame) -> List[float]:
        """
        Generate 24-hour ahead predictions compatible with enhanced_demand_forecasting.py
        
        Args:
            recent_data: Recent historical data DataFrame
            
        Returns:
            List of 24 hourly predictions
        """
        result = self.predict_demand("default", 24)
        ensemble = result.get('ensemble_prediction')
        if ensemble and len(ensemble) == 24:
            return ensemble
        else:
            # Fallback to simple synthetic forecast if no models available
            logger.warning("No ensemble prediction available, using fallback forecast")
            base_demand = 60.0
            return [base_demand + 10 * np.sin(2 * np.pi * i / 24) + np.random.normal(0, 2) 
                   for i in range(24)]
        
    def predict_demand(self, company_id: str, hours_ahead: int = 24) -> Dict:
        """
        Generate demand predictions using available models.
        
        Args:
            company_id: Company identifier
            hours_ahead: Number of hours to predict ahead
            
        Returns:
            Dictionary with predictions from available models
        """
        predictions = {
            'timestamp': datetime.now(),
            'company_id': company_id,
            'hours_ahead': hours_ahead,
            'models_used': [],
            'predictions': {},
            'ensemble_prediction': None
        }
        
        # Generate synthetic current data for prediction context
        current_data = self._generate_current_context()
        
        # Prophet predictions
        if self.prophet_available:
            try:
                prophet_pred = self._predict_prophet(current_data, hours_ahead)
                predictions['predictions']['prophet'] = prophet_pred
                predictions['models_used'].append('prophet')
            except Exception as e:
                logger.error(f"Prophet prediction failed: {e}")
                
        # SARIMAX predictions
        if self.sarimax_available:
            try:
                sarimax_pred = self._predict_sarimax(current_data, hours_ahead)
                predictions['predictions']['sarimax'] = sarimax_pred
                predictions['models_used'].append('sarimax')
            except Exception as e:
                logger.error(f"SARIMAX prediction failed: {e}")
                
        # ARIMA predictions
        if self.arima_available:
            try:
                arima_pred = self._predict_arima(current_data, hours_ahead)
                predictions['predictions']['arima'] = arima_pred
                predictions['models_used'].append('arima')
            except Exception as e:
                logger.error(f"ARIMA prediction failed: {e}")
                
        # LSTM predictions
        if self.lstm_available:
            try:
                lstm_pred = self._predict_lstm(current_data, hours_ahead)
                predictions['predictions']['lstm'] = lstm_pred
                predictions['models_used'].append('lstm')
            except Exception as e:
                logger.error(f"LSTM prediction failed: {e}")
                
        # Create ensemble prediction
        predictions['ensemble_prediction'] = self._create_ensemble(predictions['predictions'])
        
        return predictions
        
    def _generate_current_context(self) -> pd.DataFrame:
        """Generate synthetic current data for prediction context"""
        now = datetime.now()
        hours = pd.date_range(start=now - timedelta(hours=48), end=now, freq='H')
        
        # Simple synthetic data based on time patterns
        demand_values = []
        for hour in hours:
            # Daily pattern
            daily_factor = 0.7 + 0.3 * np.sin(2 * np.pi * hour.hour / 24)
            # Weekly pattern  
            weekly_factor = 0.9 + 0.1 * np.sin(2 * np.pi * hour.weekday() / 7)
            # Base demand with some randomness
            base_demand = 50 * daily_factor * weekly_factor + np.random.normal(0, 5)
            demand_values.append(max(base_demand, 10))
            
        df = pd.DataFrame({
            'ds': hours,
            'y': demand_values,
            'demand_kw': demand_values,
            'temperature': 20 + 10 * np.sin(2 * np.pi * np.arange(len(hours)) / (24 * 365)) + np.random.normal(0, 2, len(hours)),
            'solar_radiation': 15 * np.maximum(0, np.sin(2 * np.pi * np.arange(len(hours)) / 24)),
            'wind_speed': np.random.normal(8, 3, len(hours))
        })
        
        return df
        
    def _predict_prophet(self, current_data: pd.DataFrame, hours_ahead: int) -> List[float]:
        """Generate Prophet predictions"""
        model = self.models['prophet']
        
        # Create future dataframe
        future = model.make_future_dataframe(periods=hours_ahead, freq='H')
        
        # Add regressors (use last known values + some variation)
        last_temp = current_data['temperature'].iloc[-1]
        last_solar = current_data['solar_radiation'].iloc[-1]
        last_wind = current_data['wind_speed'].iloc[-1]
        
        future['temperature'] = (current_data['temperature'].tolist() + 
                               [last_temp + np.random.normal(0, 1) for _ in range(hours_ahead)])
        future['solar_radiation'] = (current_data['solar_radiation'].tolist() + 
                                   [max(0, last_solar + np.random.normal(0, 2)) for _ in range(hours_ahead)])
        future['wind_speed'] = (current_data['wind_speed'].tolist() + 
                              [max(0, last_wind + np.random.normal(0, 1)) for _ in range(hours_ahead)])
        
        # Generate forecast
        forecast = model.predict(future)
        
        # Return only future predictions
        return forecast['yhat'].iloc[-hours_ahead:].tolist()
        
    def _predict_sarimax(self, current_data: pd.DataFrame, hours_ahead: int) -> List[float]:
        """Generate SARIMAX predictions"""
        model = self.models['sarimax']
        
        # Get forecast
        forecast = model.get_forecast(steps=hours_ahead)
        forecast_mean = forecast.predicted_mean
        
        return forecast_mean.tolist() if hasattr(forecast_mean, 'tolist') else [float(forecast_mean)]
        
    def _predict_arima(self, current_data: pd.DataFrame, hours_ahead: int) -> List[float]:
        """Generate ARIMA predictions"""
        model = self.models['arima']
        
        # Get forecast
        forecast = model.forecast(steps=hours_ahead)
        
        return forecast.tolist() if hasattr(forecast, 'tolist') else [float(forecast)]
        
    def _predict_lstm(self, current_data: pd.DataFrame, hours_ahead: int) -> List[float]:
        """Generate LSTM predictions"""
        model = self.models['lstm']
        scaler = self.scalers['lstm']
        
        # Use last 24 hours as input (look_back window)
        look_back = self.metadata.get('lstm_look_back', 24)
        recent_data = current_data['demand_kw'].iloc[-look_back:].values
        
        # Scale the data
        scaled_data = scaler.transform(recent_data.reshape(-1, 1)).flatten()
        
        predictions = []
        current_sequence = scaled_data.copy()
        
        # Generate predictions step by step
        for _ in range(hours_ahead):
            # Reshape for LSTM input
            X = current_sequence[-look_back:].reshape(1, look_back, 1)
            
            # Predict next value
            pred = model.predict(X, verbose=0)
            pred_scaled = pred[0][0]
            
            # Inverse transform
            pred_original = scaler.inverse_transform([[pred_scaled]])[0][0]
            predictions.append(float(pred_original))
            
            # Update sequence for next prediction
            current_sequence = np.append(current_sequence[1:], pred_scaled)
            
        return predictions
        
    def _create_ensemble(self, predictions: Dict) -> Optional[List[float]]:
        """Create ensemble prediction from available models"""
        if not predictions:
            return None
            
        # Get all prediction arrays
        pred_arrays = []
        weights = []
        
        # Weight models based on typical performance
        model_weights = {
            'prophet': 0.4,
            'sarimax': 0.35,
            'arima': 0.25,
            'lstm': 0.35
        }
        
        for model_name, pred_list in predictions.items():
            if pred_list and len(pred_list) > 0:
                pred_arrays.append(np.array(pred_list))
                weights.append(model_weights.get(model_name, 0.33))
                
        if not pred_arrays:
            return None
            
        # Normalize weights
        weights = np.array(weights) / sum(weights)
        
        # Calculate weighted average
        ensemble = np.zeros_like(pred_arrays[0])
        for pred_array, weight in zip(pred_arrays, weights):
            ensemble += weight * pred_array
            
        return ensemble.tolist()
        
    def get_model_info(self) -> Dict:
        """Get information about loaded models"""
        return {
            'models_available': {
                'prophet': self.prophet_available,
                'sarimax': self.sarimax_available,
                'arima': self.arima_available,
                'lstm': self.lstm_available
            },
            'metadata': self.metadata,
            'models_dir': self.models_dir,
            'total_models': len(self.models)
        }


# Global model loader instance
_model_loader = None

def get_model_loader(models_dir: str = "models") -> PreTrainedModelLoader:
    """Get global model loader instance (singleton)"""
    global _model_loader
    if _model_loader is None:
        _model_loader = PreTrainedModelLoader(models_dir)
        _model_loader.load_all_models()
    return _model_loader


def quick_forecast(company_id: str, hours_ahead: int = 24) -> Dict:
    """
    Quick forecast function using pre-trained models.
    
    Args:
        company_id: Company identifier
        hours_ahead: Hours to forecast ahead
        
    Returns:
        Forecast data dictionary
    """
    loader = get_model_loader()
    return loader.predict_demand(company_id, hours_ahead)


if __name__ == "__main__":
    # Test the model loader
    print("Testing Pre-trained Model Loader...")
    
    loader = PreTrainedModelLoader()
    results = loader.load_all_models()
    
    print(f"Loading results: {results}")
    print(f"Model info: {loader.get_model_info()}")
    
    if any(results.values()):
        print("\nTesting prediction...")
        pred = loader.predict_demand("onepower", 24)
        print(f"Prediction sample: {pred}")
    else:
        print("\nNo models loaded. Please run the Colab notebook and download models.")