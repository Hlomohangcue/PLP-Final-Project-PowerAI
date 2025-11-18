# PowerAI - Intelligent Renewable Energy Management System
# Streamlit Docker container for production deployment

FROM python:3.9-slim

# Set maintainer
LABEL maintainer="Hlomohang Sethuntsa <hlomohangsethuntsa3@gmail.com>"
LABEL description="PowerAI - Intelligent Renewable Energy Management System"
LABEL version="1.0"
LABEL url="https://powerai-lesotho.streamlit.app/"

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements-streamlit.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-streamlit.txt

# Copy application files
COPY streamlit_app.py .
COPY config_multi_tenant.py .
COPY pretrained_models.py .
COPY enhanced_demand_forecasting.py .

# Copy models directory
COPY models/ models/

# Copy documentation
COPY DOCUMENTATION.md .
COPY README.md .

# Create .streamlit directory for config
RUN mkdir -p .streamlit

# Create logs directory
RUN mkdir -p logs

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]