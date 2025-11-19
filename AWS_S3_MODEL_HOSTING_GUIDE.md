# Hosting Large AI Models on AWS S3

This guide explains how to host large machine learning models (like your 4GB LSTM model) on AWS S3 for production deployments.

---

## 🎯 Why Use AWS S3?

**Benefits:**
- ✅ No file size limits (unlike Google Drive, GitHub)
- ✅ Fast download speeds with CloudFront CDN
- ✅ Pay only for storage and bandwidth used
- ✅ High availability (99.99% uptime SLA)
- ✅ Secure with fine-grained access control
- ✅ Industry standard for ML model hosting

**Cost Estimate:**
- **Storage**: ~$0.023 per GB/month ($0.09/month for 4GB LSTM model)
- **Data Transfer**: ~$0.09 per GB downloaded (first 10GB/month free)
- **Total**: Less than $1/month for typical usage

---

## 📋 Prerequisites

1. **AWS Account** (Free tier available)
   - Sign up at: https://aws.amazon.com/free/
   - Credit/debit card required (but free tier is generous)

2. **AWS CLI** (Optional but recommended)
   - Install: https://aws.amazon.com/cli/

3. **Your Model Files**
   - `lstm_model.h5` (4GB)
   - `arima_model.pkl` (50MB)
   - `lstm_scaler.pkl` (1KB)
   - `sarimax_model.pkl` (1.2GB) - optional

---

## 🚀 Step-by-Step Setup

### Step 1: Create AWS Account

1. Go to https://aws.amazon.com/
2. Click **"Create an AWS Account"**
3. Follow signup process (requires credit card but won't charge for free tier)
4. Verify your email and phone number

### Step 2: Create S3 Bucket

**Via AWS Console (Web Interface):**

1. **Login** to AWS Console: https://console.aws.amazon.com/
2. **Search** for "S3" in the top search bar
3. Click **"Create bucket"**
4. **Configure bucket:**
   ```
   Bucket name: powerai-models-lesotho  (must be globally unique)
   AWS Region: us-east-1  (or closest to your users)
   
   Object Ownership: ACLs disabled (recommended)
   Block Public Access: UNCHECK "Block all public access"
   ⚠️ Check "I acknowledge..." (models will be publicly downloadable)
   
   Bucket Versioning: Disable (save costs)
   Encryption: Enable (Server-side encryption with Amazon S3 managed keys)
   ```
5. Click **"Create bucket"**

### Step 3: Upload Model Files

**Via AWS Console:**

1. **Open your bucket** (click on bucket name)
2. Click **"Upload"** button
3. Click **"Add files"** and select:
   - `lstm_model.h5`
   - `arima_model.pkl`
   - `lstm_scaler.pkl`
   - `sarimax_model.pkl` (optional)
4. Click **"Upload"** and wait for completion
   - 4GB file will take 5-15 minutes depending on your internet speed
   - You can close the browser - upload continues in background

**Via AWS CLI (Faster for large files):**

```bash
# Configure AWS CLI (one-time setup)
aws configure
# Enter: Access Key ID, Secret Access Key, Region (us-east-1), Output format (json)

# Upload files
aws s3 cp models/lstm_model.h5 s3://powerai-models-lesotho/lstm_model.h5
aws s3 cp models/arima_model.pkl s3://powerai-models-lesotho/arima_model.pkl
aws s3 cp models/lstm_scaler.pkl s3://powerai-models-lesotho/lstm_scaler.pkl
aws s3 cp models/sarimax_model.pkl s3://powerai-models-lesotho/sarimax_model.pkl
```

### Step 4: Make Files Publicly Accessible

**Important:** Models need to be publicly readable for your app to download them.

**Option A: Make Individual Files Public**

1. In S3 console, select a file (e.g., `lstm_model.h5`)
2. Click **"Actions"** → **"Make public using ACL"**
3. Confirm by clicking **"Make public"**
4. Repeat for each model file

**Option B: Create Bucket Policy (Recommended)**

1. Go to bucket → **"Permissions"** tab
2. Scroll to **"Bucket policy"**
3. Click **"Edit"** and paste this policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::powerai-models-lesotho/*"
        }
    ]
}
```

4. Replace `powerai-models-lesotho` with your actual bucket name
5. Click **"Save changes"**

### Step 5: Get Download URLs

Your models are now accessible at:

```
https://powerai-models-lesotho.s3.us-east-1.amazonaws.com/lstm_model.h5
https://powerai-models-lesotho.s3.us-east-1.amazonaws.com/arima_model.pkl
https://powerai-models-lesotho.s3.us-east-1.amazonaws.com/lstm_scaler.pkl
https://powerai-models-lesotho.s3.us-east-1.amazonaws.com/sarimax_model.pkl
```

**Format:**
```
https://<bucket-name>.s3.<region>.amazonaws.com/<file-name>
```

**Test the URL:**
Open in browser or use curl:
```bash
curl -I https://powerai-models-lesotho.s3.us-east-1.amazonaws.com/lstm_model.h5
# Should return: HTTP/1.1 200 OK
```

---

## 🔧 Update Your Download Script

Update `download_models.py` to use S3 URLs:

```python
"""
Download Pre-trained Models from AWS S3
"""

import os
import requests
from pathlib import Path
import sys

# AWS S3 URLs for models
MODEL_URLS = {
    'arima_model.pkl': {
        'url': 'https://powerai-models-lesotho.s3.us-east-1.amazonaws.com/arima_model.pkl',
        'size_mb': 50
    },
    'lstm_model.h5': {
        'url': 'https://powerai-models-lesotho.s3.us-east-1.amazonaws.com/lstm_model.h5',
        'size_mb': 4000
    },
    'lstm_scaler.pkl': {
        'url': 'https://powerai-models-lesotho.s3.us-east-1.amazonaws.com/lstm_scaler.pkl',
        'size_mb': 0.001
    },
    'sarimax_model.pkl': {
        'url': 'https://powerai-models-lesotho.s3.us-east-1.amazonaws.com/sarimax_model.pkl',
        'size_mb': 1200
    }
}

def download_file(url, destination):
    """Download file from URL with progress indication"""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192
    
    with open(destination, 'wb') as f:
        downloaded = 0
        for chunk in response.iter_content(block_size):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\rDownloading: {percent:.1f}%", end='')
    
    print()  # New line after download

def download_models():
    """Download all models from AWS S3"""
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("PowerAI Model Downloader (AWS S3)")
    print("=" * 60)
    print()
    
    total_size = sum(info['size_mb'] for info in MODEL_URLS.values())
    print(f"📦 Total download size: ~{total_size:.1f} MB")
    print(f"📁 Models will be saved to: {models_dir.absolute()}")
    print()
    
    for filename, info in MODEL_URLS.items():
        destination = models_dir / filename
        
        if destination.exists():
            print(f"⏭️  Skipping {filename} (already exists)")
            continue
        
        print(f"⬇️  Downloading {filename} (~{info['size_mb']} MB)...")
        
        try:
            download_file(info['url'], destination)
            
            if destination.exists() and destination.stat().st_size > 1000:
                print(f"✅ {filename} downloaded successfully")
            else:
                print(f"❌ {filename} download failed")
                if destination.exists():
                    destination.unlink()
                    
        except Exception as e:
            print(f"❌ Error downloading {filename}: {e}")
        
        print()
    
    print("=" * 60)
    print("Download complete!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    print()
    download_models()
```

---

## 🌐 Add CloudFront CDN (Optional - For Better Performance)

CloudFront is AWS's CDN that caches your models globally for faster downloads.

### Benefits:
- ✅ 50% faster downloads worldwide
- ✅ Reduces S3 bandwidth costs
- ✅ Free tier: 1TB data transfer/month

### Setup:

1. **Go to CloudFront Console**: https://console.aws.amazon.com/cloudfront/
2. Click **"Create distribution"**
3. **Configure:**
   ```
   Origin domain: powerai-models-lesotho.s3.us-east-1.amazonaws.com
   Origin path: (leave empty)
   Name: powerai-models-cdn
   
   Viewer protocol policy: Redirect HTTP to HTTPS
   Allowed HTTP methods: GET, HEAD
   Cache policy: CachingOptimized
   
   Price class: Use only North America and Europe (cheapest)
   ```
4. Click **"Create distribution"**
5. Wait 5-10 minutes for deployment
6. **Get CloudFront URL**: `https://d1234abcd5678.cloudfront.net/`

**Update your URLs:**
```python
'url': 'https://d1234abcd5678.cloudfront.net/lstm_model.h5'
```

---

## 💰 Cost Management

### Free Tier (First 12 Months):
- ✅ 5GB S3 storage
- ✅ 20,000 GET requests
- ✅ 2,000 PUT requests
- ✅ 100GB data transfer out

### After Free Tier:
**Monthly Costs for PowerAI:**
```
Storage (5.2GB):     $0.12
GET Requests (100):  $0.00
Data Transfer (10GB): Free (within free tier)
------------------------
Total:               ~$0.12/month (12 cents!)
```

### Cost Optimization Tips:
1. **Use CloudFront** - First 1TB/month free
2. **Compress models** - Use model quantization to reduce size
3. **Lifecycle policies** - Auto-delete old model versions
4. **Set up billing alerts** - Get notified if costs exceed $1

---

## 🔒 Security Best Practices

### 1. Use IAM Credentials Properly
```bash
# Never commit AWS credentials to Git!
# Add to .gitignore:
.aws/
*.pem
credentials.json
```

### 2. Enable S3 Bucket Logging
- Track who downloads your models
- Monitor for suspicious activity

### 3. Set Up CORS (for browser downloads)
Bucket → Permissions → CORS:
```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "HEAD"],
        "AllowedOrigins": ["https://powerai-lesotho.streamlit.app"],
        "ExposeHeaders": []
    }
]
```

### 4. Use Signed URLs (Optional - for private models)
If models should be private:
```python
import boto3
from botocore.exceptions import ClientError

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object"""
    s3_client = boto3.client('s3')
    
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expiration
        )
    except ClientError as e:
        print(f"Error: {e}")
        return None
    
    return response

# Usage
url = generate_presigned_url('powerai-models-lesotho', 'lstm_model.h5')
# URL expires after 1 hour (3600 seconds)
```

---

## 🆘 Troubleshooting

### Error: "403 Forbidden"
**Solution:** Check bucket policy allows public access:
```bash
aws s3api get-bucket-policy --bucket powerai-models-lesotho
```

### Error: "Slow Download Speed"
**Solution:** Use CloudFront CDN or choose region closer to users

### Error: "Download Interrupted"
**Solution:** Add retry logic:
```python
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=3, backoff_factor=0.3)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

response = session.get(url, stream=True)
```

### Error: "High Costs"
**Solution:** 
1. Check CloudWatch metrics
2. Enable S3 analytics
3. Set up budget alerts (free)

---

## 📊 Monitoring & Analytics

### CloudWatch Metrics (Built-in):
- Total storage size
- Number of requests
- Data transfer (in/out)
- Error rates

### Setup Billing Alert:
1. Go to **AWS Billing Dashboard**
2. Click **"Budgets"**
3. Create budget: $5/month
4. Email alert when exceeds $1

---

## 🔄 Alternative: Hugging Face Hub (Free Alternative)

If you want **completely free** hosting:

### Pros:
- ✅ 100% free for public models
- ✅ No credit card required
- ✅ Built for ML models
- ✅ Git-based versioning

### Cons:
- ❌ Slower download speeds
- ❌ Less control
- ❌ 10GB file size limit

### Quick Setup:
```bash
# Install
pip install huggingface_hub

# Upload
from huggingface_hub import HfApi
api = HfApi()
api.upload_file(
    path_or_fileobj="models/lstm_model.h5",
    path_in_repo="lstm_model.h5",
    repo_id="Hlomohangcue/powerai-models",
    repo_type="model"
)

# Download URL:
# https://huggingface.co/Hlomohangcue/powerai-models/resolve/main/lstm_model.h5
```

---

## 📝 Summary Comparison

| Feature | AWS S3 | CloudFront CDN | Hugging Face | Google Drive |
|---------|--------|----------------|--------------|--------------|
| **Cost** | ~$0.12/mo | ~$0.05/mo | Free | Free |
| **Speed** | Fast | Very Fast | Medium | Slow |
| **Reliability** | 99.99% | 99.99% | 99.9% | 95% |
| **File Size** | Unlimited | Unlimited | 10GB | 15GB total |
| **Setup Time** | 15 min | 30 min | 10 min | 5 min |
| **Production Ready** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |

**Recommendation:** 
- **For Production**: AWS S3 + CloudFront
- **For Development/Demo**: Hugging Face Hub
- **For Quick Tests**: Google Drive

---

## 📞 Need Help?

**AWS Support:**
- Free tier support: https://aws.amazon.com/free/
- Documentation: https://docs.aws.amazon.com/s3/

**PowerAI Contact:**
- Email: hlomohangsethuntsa3@gmail.com
- GitHub: https://github.com/Hlomohangcue/PLP-Final-Project-PowerAI

---

**Ready to deploy your models professionally!** 🚀
