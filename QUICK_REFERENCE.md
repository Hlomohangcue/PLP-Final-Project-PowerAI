# PowerAI Quick Reference Guide

## 🚀 Getting Started (30 seconds)

```bash
# 1. Navigate to project
cd AI-For-Software-Engineering-Final-Project

# 2. Activate virtual environment
.venv\Scripts\activate

# 3. Run application
streamlit run streamlit_app.py
```

Open browser to `http://localhost:8501`

---

## 📁 Essential Files

| File | Purpose |
|------|---------|
| `streamlit_app.py` | Main application (600+ lines) |
| `config_multi_tenant.py` | Company configurations |
| `pretrained_models.py` | Model loading utilities |
| `enhanced_demand_forecasting.py` | ML forecasting engine |
| `requirements-streamlit.txt` | Python dependencies |
| `models/` | Pre-trained ML models |
| `DOCUMENTATION.md` | Full user guide |
| `README.md` | Project overview |

---

## 🎯 Key Features Quick Access

### Dashboard
- **Location**: Home page (default)
- **Features**: Real-time KPIs, demand chart, renewable mix
- **Companies**: Select from sidebar dropdown

### Forecasting
- **Location**: "Forecasting" page
- **Action**: Click "Generate 24-Hour Forecast"
- **Models**: ARIMA, LSTM (pre-trained)
- **Output**: Line chart with predictions + metrics

### Monitoring
- **Location**: "Real-time Monitoring" page
- **Features**: Live metrics, system health, alerts
- **Update**: Refreshes automatically

### Analytics
- **Location**: "Analytics & Reports" page
- **Features**: Historical trends, performance metrics
- **Charts**: Line charts, bar charts

---

## 🏢 Companies

| Company | Country | Focus | Renewable Types |
|---------|---------|-------|----------------|
| OnePower | Lesotho | Solar | Solar, Wind, Hydro |
| SolarTech | South Africa | Multi-source | Solar, Wind, Hydro |
| WindPower | Kenya | Wind | Wind, Solar, Biomass |
| GreenGrid | Tanzania | Hydro | Hydro, Solar, Wind |

---

## 🔧 Common Commands

### Development
```bash
# Run app
streamlit run streamlit_app.py

# Run with custom port
streamlit run streamlit_app.py --server.port 8502

# Debug mode
streamlit run streamlit_app.py --logger.level=debug
```

### Installation
```bash
# Install dependencies
pip install -r requirements-streamlit.txt

# Upgrade specific package
pip install streamlit --upgrade

# Check installed packages
pip list
```

### Docker
```bash
# Build image
docker build -t powerai .

# Run container
docker run -p 8501:8501 powerai

# Docker Compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

## 📊 Model Files

| File | Type | Size | Purpose |
|------|------|------|---------|
| `arima_model.pkl` | Pickle | ~2MB | ARIMA forecasting |
| `sarimax_model.pkl` | Pickle | ~3MB | SARIMAX (seasonal) |
| `lstm_model.h5` | H5 | ~5MB | LSTM neural network |
| `lstm_scaler.pkl` | Pickle | ~1MB | Data normalization |
| `model_metadata.json` | JSON | ~5KB | Model information |

---

## 🎨 Customization

### Theme (in `.streamlit/config.toml`)
```toml
[theme]
primaryColor = "#2c5530"        # OnePower green
backgroundColor = "#f8f9fa"      # Light gray
secondaryBackgroundColor = "#e0e0e0"
textColor = "#262730"
```

### Company Config (in `config_multi_tenant.py`)
```python
'onepower': {
    'name': 'OnePower',
    'country': 'Lesotho',
    'currency': 'LSL',
    'renewable_types': ['solar', 'wind', 'hydro'],
    'grid_capacity_mw': 500,
    'primary_color': '#2c5530'
}
```

---

## 🐛 Troubleshooting

### Problem: Port already in use
```bash
# Windows
netstat -ano | findstr :8501
taskkill /PID <pid> /F

# Alternative port
streamlit run streamlit_app.py --server.port 8502
```

### Problem: Module not found
```bash
pip install -r requirements-streamlit.txt --force-reinstall
```

### Problem: Models not loading
```bash
# Check if models exist
dir models  # Windows
ls models/  # Linux/Mac

# Verify in Python
python -c "from pretrained_models import PreTrainedModelLoader; print(PreTrainedModelLoader().models_available())"
```

### Problem: Slow performance
```python
# Add caching in streamlit_app.py
@st.cache_data
def expensive_function():
    return result
```

---

## 📦 Dependencies (Major)

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.29.0 | Web framework |
| pandas | Latest | Data manipulation |
| numpy | Latest | Numerical computing |
| plotly | Latest | Interactive charts |
| scikit-learn | Latest | ML algorithms |
| statsmodels | Latest | ARIMA/SARIMAX |
| tensorflow | Latest | LSTM models |

---

## 🚀 Deployment Quick Start

### Streamlit Cloud
1. Push to GitHub
2. Visit streamlit.io/cloud
3. Connect repository
4. Click "Deploy"

### Local Production
```bash
streamlit run streamlit_app.py --server.headless true
```

### Docker
```bash
docker-compose up -d
```

---

## 📞 Quick Help

| Need | Resource |
|------|----------|
| Installation help | See DOCUMENTATION.md |
| Deployment guide | See DEPLOYMENT.md |
| Project overview | See README.md |
| Complete summary | See PROJECT_SUMMARY.md |
| Code reference | See streamlit_app.py comments |

---

## ⚡ Pro Tips

1. **Use sidebar** - Company selection affects all pages
2. **Generate forecast first** - Loads models into memory
3. **Check console** - Logs show what's happening
4. **Use caching** - Speeds up repeated operations
5. **Test with different companies** - Each has unique configs
6. **Monitor memory** - Large models need 4GB+ RAM
7. **Keep models folder** - Required for predictions
8. **Check documentation** - Comprehensive guides available

---

## 📝 Presentation Tips

1. **Start with Dashboard** - Shows real-time capabilities
2. **Demo Forecasting** - Highlight AI/ML models
3. **Switch Companies** - Show multi-tenant architecture
4. **Explain SDG 7** - Connect to UN goals
5. **Show Code Quality** - Mention documentation
6. **Discuss Deployment** - Multiple platform support
7. **Highlight Business Value** - Cost savings, reliability

---

## 🎯 Project Highlights

- ✅ **600+ lines** of main application code
- ✅ **5 interactive pages** with full functionality
- ✅ **4 companies** with multi-tenant support
- ✅ **3 ML models** (ARIMA, SARIMAX, LSTM)
- ✅ **Pre-trained models** for instant predictions
- ✅ **Comprehensive docs** (3 major markdown files)
- ✅ **Docker ready** with compose configuration
- ✅ **Cloud deployable** to multiple platforms
- ✅ **Production ready** with proper architecture
- ✅ **UN SDG 7 aligned** for sustainability

---

## 🏆 Submission Checklist

- ✅ All files created and tested
- ✅ Application runs successfully
- ✅ Models load correctly
- ✅ Documentation is complete
- ⬜ Code committed to Git (optional)
- ⬜ Deployed to Streamlit Cloud (optional)
- ⬜ Presentation prepared
- ⬜ Demo practiced

---

**Your PowerAI project is ready for submission!** 🎉

For detailed information, see:
- **README.md** - Quick start & overview
- **DOCUMENTATION.md** - Complete guide
- **DEPLOYMENT.md** - Deployment instructions
- **PROJECT_SUMMARY.md** - Full summary

**Live Demo**: [powerai-lesotho.streamlit.app](https://powerai-lesotho.streamlit.app/)  
**Email**: hlomohangsethuntsa3@gmail.com  
**GitHub**: [github.com/Hlomohangcue/PLP-Final-Project-PowerAI](https://github.com/Hlomohangcue/PLP-Final-Project-PowerAI)

**© 2025 PowerAI Lesotho**
