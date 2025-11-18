# PowerAI Pre-trained Models

This directory contains pre-trained machine learning models for energy demand forecasting.

## 📦 Model Files (Not Included in Repository)

Due to GitHub file size limitations, the following model files are **not included** in this repository:

- `arima_model.pkl` (~50 MB)
- `sarimax_model.pkl` (~1.2 GB) 
- `lstm_model.h5` (~4 GB)
- `lstm_scaler.pkl` (~1 KB)

## 🔧 How to Get the Models

### Option 1: Train Models Yourself (Recommended)

Use the provided Jupyter notebook to train fresh models:

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Launch Jupyter
jupyter notebook notebooks/PowerAI_Model_Training.ipynb

# Follow the notebook to train all models
# Models will be saved to this directory automatically
```

### Option 2: Use Demo/Synthetic Data

The application will run without pre-trained models, but forecasting accuracy will be limited. The app will generate predictions using basic algorithms.

### Option 3: Download Pre-trained Models

If you have access to pre-trained models from the original developer:

1. Contact: support@powerai.co.ls
2. Request model files
3. Place them in this `models/` directory

## 📊 Model Information

### ARIMA Model
- **File**: `arima_model.pkl`
- **Algorithm**: AutoRegressive Integrated Moving Average
- **Best for**: Short-term forecasts (1-24 hours)
- **Training time**: ~2 minutes
- **Size**: ~50 MB

### SARIMAX Model  
- **File**: `sarimax_model.pkl`
- **Algorithm**: Seasonal ARIMA with eXogenous variables
- **Best for**: Seasonal patterns with external factors
- **Training time**: ~4 minutes
- **Size**: ~1.2 GB

### LSTM Model
- **File**: `lstm_model.h5` 
- **Algorithm**: Long Short-Term Memory Neural Network
- **Best for**: Complex patterns and long-term forecasts
- **Training time**: ~15-20 minutes (GPU recommended)
- **Size**: ~4 GB

### Scaler
- **File**: `lstm_scaler.pkl`
- **Purpose**: Normalize data for LSTM model
- **Size**: ~1 KB

## 🚀 Quick Setup

```powershell
# 1. Clone repository
git clone https://github.com/Hlomohangcue/PLP-Final-Project-PowerAI.git
cd PLP-Final-Project-PowerAI

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements-streamlit.txt

# 4. Train models (optional but recommended)
jupyter notebook notebooks/PowerAI_Model_Training.ipynb

# 5. Run application
streamlit run streamlit_app.py
```

## 📝 Model Metadata

Check `model_metadata.json` for information about when models were trained and their performance metrics.

## ⚠️ Important Notes

- **Storage**: Ensure you have at least **6 GB** free space for all models
- **Training**: Model training requires significant computational resources
- **GPU**: Highly recommended for LSTM training (reduces time from 20min to 2min)
- **Memory**: At least **8 GB RAM** recommended for model training

## 🆘 Troubleshooting

### "Model file not found" Error
✅ **Solution**: Train models using the Jupyter notebook or run app in demo mode

### Out of Memory Error
✅ **Solution**: Close other applications, use GPU if available, or reduce batch size

### Slow Training
✅ **Solution**: Use GPU acceleration or reduce dataset size for testing

---

**© 2025 PowerAI Lesotho**
