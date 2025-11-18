# Google Drive Model Setup Guide

## 📤 Step 1: Upload Models to Google Drive

1. **Create a folder** in your Google Drive called "PowerAI Models"

2. **Upload these model files** (if you have them locally):
   - `arima_model.pkl` (~50 MB)
   - `lstm_model.h5` (~4 GB)
   - `lstm_scaler.pkl` (~1 KB)
   - ~~`sarimax_model.pkl`~~ (Skip - too large at 1.2GB)

## 🔗 Step 2: Get Shareable Links

For **each file** you uploaded:

1. **Right-click** the file in Google Drive
2. Click **"Share"** or **"Get link"**
3. Change access to: **"Anyone with the link"** → **"Viewer"**
4. Click **"Copy link"**
5. The link will look like:
   ```
   https://drive.google.com/file/d/1a2B3c4D5e6F7g8H9i0J1k2L3m4N5o6P7q/view?usp=sharing
   ```

## 🔑 Step 3: Extract File IDs

From each link, extract the **FILE_ID** (the part between `/d/` and `/view`):

**Example:**
```
Link: https://drive.google.com/file/d/1a2B3c4D5e6F7g8H9i0J1k2L3m4N5o6P7q/view
File ID: 1a2B3c4D5e6F7g8H9i0J1k2L3m4N5o6P7q
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

## ⚙️ Step 4: Update download_models.py

Edit `download_models.py` and replace the placeholders:

```python
MODEL_URLS = {
    'arima_model.pkl': {
        'id': '1a2B3c4D5e6F7g8H9i0J1k2L3m4N5o6P7q',  # ← Your ARIMA file ID
        'size_mb': 50
    },
    'lstm_model.h5': {
        'id': '2b3C4d5E6f7G8h9I0j1K2l3M4n5O6p7Q8r',  # ← Your LSTM file ID
        'size_mb': 4000
    },
    'lstm_scaler.pkl': {
        'id': '3c4D5e6F7g8H9i0J1k2L3m4N5o6P7q8R9s',  # ← Your Scaler file ID
        'size_mb': 0.001
    }
}
```

## 🚀 Step 5: Run the Download Script

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install requests if needed
pip install requests

# Download models
python download_models.py
```

## ✅ Verification

After download completes, check:

```bash
dir models\        # Windows
ls -lh models/     # Linux/Mac
```

You should see:
```
arima_model.pkl     (~50 MB)
lstm_model.h5       (~4 GB)
lstm_scaler.pkl     (~1 KB)
```

## 🌐 For Streamlit Cloud Deployment

**Option A: Runtime Download (Recommended)**

Add this to the beginning of `streamlit_app.py`:

```python
import os
import subprocess

# Download models on first run
if not os.path.exists('models/arima_model.pkl'):
    subprocess.run(['python', 'download_models.py'])
```

**Option B: Secrets Management**

1. In Streamlit Cloud dashboard, go to app settings
2. Add secrets in `.streamlit/secrets.toml` format:
   ```toml
   [gdrive]
   arima_id = "1a2B3c4D5e6F7g8H9i0J1k2L3m4N5o6P7q"
   lstm_id = "2b3C4d5E6f7G8h9I0j1K2l3M4n5O6p7Q8r"
   scaler_id = "3c4D5e6F7g8H9i0J1k2L3m4N5o6P7q8R9s"
   ```

3. Update script to read from `st.secrets`

## ⚠️ Important Notes

1. **File Size Limits**: 
   - Google Drive: No limit with direct links
   - Streamlit Cloud: May timeout on large downloads (>1GB)
   - Recommendation: Skip SARIMAX model for cloud deployment

2. **Privacy**: 
   - Files are view-only
   - Anyone with link can download
   - Don't share sensitive data this way

3. **Alternative**: 
   - Use AWS S3, Azure Blob Storage, or Hugging Face Hub
   - Better for production deployments

## 🆘 Troubleshooting

**"Download failed" error:**
- Verify file ID is correct
- Check file sharing is set to "Anyone with the link"
- Try downloading manually to test link

**"File too small" warning:**
- Google Drive may return HTML instead of file
- File needs to be publicly accessible
- Check sharing permissions

**Timeout on Streamlit Cloud:**
- LSTM model (4GB) may timeout
- Consider using smaller model
- Or host models on CDN/S3

---

**Need help?** Contact: support@powerai.co.ls
