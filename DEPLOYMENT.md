# PowerAI Deployment Guide

Complete guide for deploying PowerAI to various environments.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Production Deployment](#production-deployment)
4. [Cloud Platforms](#cloud-platforms)
5. [Docker Deployment](#docker-deployment)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

### System Requirements

- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB free space
- **OS**: Windows, Linux, or macOS
- **Network**: Internet connection for initial setup

### Required Software

```bash
# Python
python --version  # Should be 3.8+

# pip
pip --version

# git (optional)
git --version
```

---

## 💻 Local Development

### Setup Steps

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/powerai.git
cd powerai
```

2. **Create Virtual Environment**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements-streamlit.txt
```

4. **Verify Models**
```bash
# Check if pre-trained models exist
dir models  # Windows
ls models/  # Linux/Mac

# Should see:
# - sarimax_model.pkl
# - arima_model.pkl
# - lstm_model.h5
# - lstm_scaler.pkl
# - model_metadata.json
```

5. **Run Application**
```bash
streamlit run streamlit_app.py
```

6. **Access Application**
- Open browser to `http://localhost:8501`
- Application should load automatically

### Development Mode

Enable debug features:

```bash
# Set environment variable
export STREAMLIT_SERVER_DEBUG=true  # Linux/Mac
set STREAMLIT_SERVER_DEBUG=true     # Windows

# Run with file watcher
streamlit run streamlit_app.py --server.fileWatcherType poll
```

---

## 🚀 Production Deployment

### Configuration

1. **Environment Variables**

Create `.env` file:
```bash
# Application
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/powerai/app.log

# Database (if using)
DATABASE_URL=mysql://user:pass@localhost/powerai
```

2. **Streamlit Configuration**

Create `.streamlit/config.toml`:
```toml
[server]
port = 8501
address = "0.0.0.0"
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#2c5530"
backgroundColor = "#f8f9fa"
secondaryBackgroundColor = "#e0e0e0"
textColor = "#262730"
font = "sans serif"
```

### Running in Production

#### Option 1: Systemd Service (Linux)

Create `/etc/systemd/system/powerai.service`:

```ini
[Unit]
Description=PowerAI Renewable Energy Management
After=network.target

[Service]
Type=simple
User=powerai
WorkingDirectory=/opt/powerai
Environment="PATH=/opt/powerai/.venv/bin"
ExecStart=/opt/powerai/.venv/bin/streamlit run streamlit_app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable powerai
sudo systemctl start powerai
sudo systemctl status powerai
```

#### Option 2: Supervisor (Cross-platform)

Install Supervisor:
```bash
pip install supervisor
```

Create `/etc/supervisor/conf.d/powerai.conf`:
```ini
[program:powerai]
command=/opt/powerai/.venv/bin/streamlit run streamlit_app.py
directory=/opt/powerai
user=powerai
autostart=true
autorestart=true
stderr_logfile=/var/log/powerai/error.log
stdout_logfile=/var/log/powerai/access.log
```

Start:
```bash
supervisorctl reread
supervisorctl update
supervisorctl start powerai
```

#### Option 3: PM2 (Node.js process manager)

Install PM2:
```bash
npm install -g pm2
```

Create `ecosystem.config.js`:
```javascript
module.exports = {
  apps: [{
    name: 'powerai',
    script: 'streamlit',
    args: 'run streamlit_app.py',
    cwd: '/opt/powerai',
    interpreter: '/opt/powerai/.venv/bin/python',
    env: {
      STREAMLIT_SERVER_HEADLESS: 'true'
    }
  }]
}
```

Start:
```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

### Reverse Proxy (Nginx)

Install Nginx:
```bash
sudo apt-get install nginx  # Ubuntu/Debian
sudo yum install nginx      # CentOS/RHEL
```

Configure `/etc/nginx/sites-available/powerai`:
```nginx
server {
    listen 80;
    server_name powerai.example.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/powerai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL/TLS (Let's Encrypt)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d powerai.example.com
```

---

## ☁️ Cloud Platforms

### Streamlit Cloud (Recommended)

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/powerai.git
git push -u origin main
```

2. **Deploy**
- Visit [streamlit.io/cloud](https://streamlit.io/cloud)
- Sign in with GitHub
- Click "New app"
- Select repository and branch
- Set main file: `streamlit_app.py`
- Click "Deploy"

3. **Configure**
- Add secrets in Streamlit Cloud dashboard
- Set Python version (3.9 recommended)
- Monitor app health

**Pros**: Free tier, automatic HTTPS, GitHub integration  
**Cons**: Limited resources, public by default

### AWS EC2

1. **Launch Instance**
- AMI: Ubuntu 22.04 LTS
- Instance type: t3.medium (4GB RAM)
- Security group: Allow ports 22, 80, 443, 8501

2. **Connect and Setup**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python
sudo apt-get install python3-pip python3-venv -y

# Clone repo
git clone https://github.com/yourusername/powerai.git
cd powerai

# Setup app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-streamlit.txt

# Run
streamlit run streamlit_app.py
```

3. **Setup Auto-start** (use Systemd service above)

**Cost**: ~$30-50/month  
**Pros**: Full control, scalable  
**Cons**: Manual management

### Heroku

1. **Prepare Files**

Create `Procfile`:
```
web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `runtime.txt`:
```
python-3.9.18
```

2. **Deploy**
```bash
# Login
heroku login

# Create app
heroku create powerai-app

# Deploy
git push heroku main

# Open
heroku open
```

**Cost**: $7/month (Eco dyno)  
**Pros**: Easy deployment, automatic SSL  
**Cons**: Sleep mode on free tier

### Google Cloud Run

1. **Prepare Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements-streamlit.txt .
RUN pip install --no-cache-dir -r requirements-streamlit.txt

COPY . .

EXPOSE 8080

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
```

2. **Deploy**
```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/powerai

# Deploy
gcloud run deploy powerai \
  --image gcr.io/PROJECT_ID/powerai \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Cost**: Pay per use (~$10-20/month)  
**Pros**: Serverless, auto-scaling  
**Cons**: Cold starts

---

## 🐳 Docker Deployment

### Basic Docker

1. **Create Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements-streamlit.txt .
RUN pip install --no-cache-dir -r requirements-streamlit.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run
CMD ["streamlit", "run", "streamlit_app.py", "--server.headless", "true"]
```

2. **Build and Run**
```bash
# Build
docker build -t powerai:latest .

# Run
docker run -p 8501:8501 powerai:latest

# Run with volume
docker run -p 8501:8501 -v $(pwd)/models:/app/models powerai:latest
```

### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  powerai:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./models:/app/models
      - ./logs:/app/logs
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Deploy:
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### Kubernetes

Create `deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: powerai
spec:
  replicas: 2
  selector:
    matchLabels:
      app: powerai
  template:
    metadata:
      labels:
        app: powerai
    spec:
      containers:
      - name: powerai
        image: powerai:latest
        ports:
        - containerPort: 8501
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
---
apiVersion: v1
kind: Service
metadata:
  name: powerai-service
spec:
  selector:
    app: powerai
  ports:
  - port: 80
    targetPort: 8501
  type: LoadBalancer
```

Deploy:
```bash
kubectl apply -f deployment.yaml
kubectl get pods
kubectl get services
```

---

## 📊 Monitoring & Maintenance

### Application Monitoring

1. **Streamlit Metrics**
```python
# Add to streamlit_app.py
import streamlit as st

st.set_page_config(
    page_title="PowerAI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.powerai.com',
        'Report a bug': "https://github.com/yourusername/powerai/issues",
        'About': "PowerAI v1.0 - © 2025 OnePower"
    }
)
```

2. **Logging**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/powerai.log'),
        logging.StreamHandler()
    ]
)
```

3. **Health Checks**
```bash
# Check app status
curl http://localhost:8501/_stcore/health

# Expected response: {"status": "ok"}
```

### Performance Monitoring

Use monitoring tools:

**Prometheus + Grafana**:
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'powerai'
    static_configs:
      - targets: ['localhost:8501']
```

**Datadog**:
```bash
pip install ddtrace
DD_SERVICE=powerai streamlit run streamlit_app.py
```

### Backup Strategy

1. **Models**
```bash
# Backup models
tar -czf models-backup-$(date +%Y%m%d).tar.gz models/

# Restore
tar -xzf models-backup-20251116.tar.gz
```

2. **Configuration**
```bash
# Backup configs
cp config_multi_tenant.py config_multi_tenant.py.bak
cp .streamlit/config.toml .streamlit/config.toml.bak
```

3. **Data** (if using database)
```bash
# MySQL
mysqldump -u user -p powerai > powerai-backup-$(date +%Y%m%d).sql

# Restore
mysql -u user -p powerai < powerai-backup-20251116.sql
```

### Update Procedure

1. **Backup Current Version**
```bash
tar -czf powerai-backup-$(date +%Y%m%d).tar.gz /opt/powerai
```

2. **Pull Updates**
```bash
cd /opt/powerai
git pull origin main
```

3. **Update Dependencies**
```bash
source .venv/bin/activate
pip install -r requirements-streamlit.txt --upgrade
```

4. **Restart Application**
```bash
sudo systemctl restart powerai
```

5. **Verify**
```bash
sudo systemctl status powerai
curl http://localhost:8501/_stcore/health
```

---

## 🔧 Troubleshooting

### Common Issues

#### Issue: Port Already in Use
```bash
# Find process
netstat -ano | findstr :8501  # Windows
lsof -i :8501                 # Linux/Mac

# Kill process
taskkill /PID <pid> /F        # Windows
kill -9 <pid>                 # Linux/Mac
```

#### Issue: Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements-streamlit.txt --force-reinstall

# Verify installation
pip list | grep streamlit
```

#### Issue: Models Not Loading
```bash
# Check models directory
ls -la models/

# Verify permissions
chmod 644 models/*.pkl
chmod 644 models/*.h5

# Test loading
python -c "from pretrained_models import PreTrainedModelLoader; loader = PreTrainedModelLoader(); print(loader.models_available())"
```

#### Issue: High Memory Usage
```bash
# Monitor memory
top           # Linux
htop          # Linux (better)
taskmgr       # Windows

# Solutions:
# 1. Increase system RAM
# 2. Reduce model size
# 3. Enable memory profiling
```

#### Issue: Slow Performance
```python
# Enable caching
@st.cache_data
def generate_data():
    return expensive_computation()

# Use session state
if 'data' not in st.session_state:
    st.session_state.data = load_data()
```

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Run with verbose output:
```bash
streamlit run streamlit_app.py --logger.level=debug
```

### Getting Help

1. **Check Logs**
```bash
tail -f /var/log/powerai/app.log
```

2. **Streamlit Docs**: https://docs.streamlit.io
3. **GitHub Issues**: https://github.com/yourusername/powerai/issues
4. **Community**: Streamlit Community Forum

---

## 📞 Support

For deployment assistance:
- **Email**: support@powerai.co.ls
- **Documentation**: https://docs.powerai.com
- **GitHub**: https://github.com/yourusername/powerai

---

**© 2025 PowerAI Lesotho | PowerAI Deployment Guide v1.0**
