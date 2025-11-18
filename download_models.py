"""
Download Pre-trained Models from Google Drive
==============================================

This script downloads pre-trained ML models from Google Drive for PowerAI.
Models are stored separately due to GitHub file size limitations.

Usage:
    python download_models.py
"""

import os
import requests
from pathlib import Path
import sys

# Google Drive file IDs for each model
# Replace these with your actual Google Drive file IDs
MODEL_URLS = {
    'arima_model.pkl': {
        'id': 'YOUR_ARIMA_FILE_ID',  # Replace with actual file ID
        'size_mb': 50
    },
    'lstm_model.h5': {
        'id': 'YOUR_LSTM_FILE_ID',  # Replace with actual file ID
        'size_mb': 4000
    },
    'lstm_scaler.pkl': {
        'id': 'YOUR_SCALER_FILE_ID',  # Replace with actual file ID
        'size_mb': 0.001
    },
    # SARIMAX model (1.2GB) - optional, may be too large
    # 'sarimax_model.pkl': {
    #     'id': 'YOUR_SARIMAX_FILE_ID',
    #     'size_mb': 1200
    # }
}

def download_file_from_google_drive(file_id, destination):
    """Download a file from Google Drive"""
    URL = "https://drive.google.com/uc?export=download"
    
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)
    
    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    
    save_response_content(response, destination)

def get_confirm_token(response):
    """Extract confirmation token from response"""
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    """Save downloaded content to file"""
    CHUNK_SIZE = 32768
    
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

def download_models():
    """Download all models from Google Drive"""
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("PowerAI Model Downloader")
    print("=" * 60)
    print()
    
    total_size = sum(info['size_mb'] for info in MODEL_URLS.values())
    print(f"📦 Total download size: ~{total_size:.1f} MB")
    print(f"📁 Models will be saved to: {models_dir.absolute()}")
    print()
    
    # Check if file IDs are configured
    if any('YOUR_' in info['id'] for info in MODEL_URLS.values()):
        print("⚠️  ERROR: Google Drive file IDs not configured!")
        print()
        print("Please edit download_models.py and replace:")
        print("  - YOUR_ARIMA_FILE_ID")
        print("  - YOUR_LSTM_FILE_ID")
        print("  - YOUR_SCALER_FILE_ID")
        print()
        print("To get file IDs:")
        print("1. Upload model files to Google Drive")
        print("2. Right-click file → Share → Change to 'Anyone with the link'")
        print("3. Copy the sharing link")
        print("4. Extract ID from: https://drive.google.com/file/d/FILE_ID/view")
        print()
        return False
    
    # Download each model
    for filename, info in MODEL_URLS.items():
        destination = models_dir / filename
        
        if destination.exists():
            print(f"⏭️  Skipping {filename} (already exists)")
            continue
        
        print(f"⬇️  Downloading {filename} (~{info['size_mb']} MB)...")
        
        try:
            download_file_from_google_drive(info['id'], destination)
            
            # Verify file was downloaded
            if destination.exists() and destination.stat().st_size > 1000:
                print(f"✅ {filename} downloaded successfully")
            else:
                print(f"❌ {filename} download failed (file too small or missing)")
                if destination.exists():
                    destination.unlink()
                    
        except Exception as e:
            print(f"❌ Error downloading {filename}: {e}")
        
        print()
    
    print("=" * 60)
    print("Download complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Verify model files in models/ directory")
    print("2. Run: streamlit run streamlit_app.py")
    print()
    
    return True

if __name__ == "__main__":
    print()
    success = download_models()
    
    if not success:
        sys.exit(1)
