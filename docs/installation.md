# Installation Guide

This comprehensive guide covers all installation methods for the Chatacter Backend system.

## Table of Contents

- [System Requirements](#system-requirements)
- [Docker Installation (Recommended)](#docker-installation-recommended)
- [Development Installation](#development-installation)
- [Production Installation](#production-installation)
- [Kubernetes Installation](#kubernetes-installation)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **OS**: Linux (Ubuntu 20.04+), macOS (10.15+), Windows 10+ with WSL2
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 50GB free space for containers and models
- **CPU**: 4 cores minimum, 8 cores recommended
- **GPU**: NVIDIA GPU with 6GB+ VRAM (for video/voice generation)

### Recommended Requirements
- **OS**: Ubuntu 22.04 LTS or similar Linux distribution
- **RAM**: 32GB+ for production workloads
- **Storage**: 100GB+ SSD storage
- **CPU**: 16+ cores for better performance
- **GPU**: NVIDIA RTX 3080+ or A100 for optimal performance

### Software Prerequisites
- **Docker**: 20.10 or later
- **Docker Compose**: 2.0 or later
- **NVIDIA Docker**: For GPU support
- **Git**: For repository cloning

## Docker Installation (Recommended)

### Step 1: Install Docker

#### Ubuntu/Debian
```bash
# Update package index
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
```

#### macOS
```bash
# Using Homebrew
brew install --cask docker

# Or download Docker Desktop from docker.com
```

#### Windows
1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
2. Enable WSL2 integration
3. Install and restart

### Step 2: Install Docker Compose

```bash
# Install Docker Compose (if not included with Docker Desktop)
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker compose version
```

### Step 3: Install NVIDIA Docker (For GPU Support)

```bash
# Ubuntu/Debian
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
   && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# Test GPU access
docker run --rm --gpus all nvidia/cuda:11.0.3-base-ubuntu20.04 nvidia-smi
```

### Step 4: Clone and Configure

```bash
# Clone repository with submodules
git clone --recurse-submodules https://github.com/AlphaSphereDotAI/chatacter_backend.git
cd chatacter_backend

# Create environment configuration
cp .env.example .env  # If example exists, otherwise create new
nano .env  # Edit with your configuration
```

### Step 5: Launch Services

```bash
# Start all services
docker compose up -d

# Monitor startup
docker compose logs -f

# Check service status
docker compose ps
```

## Development Installation

For local development with hot reloading and debugging capabilities.

### Prerequisites
- Python 3.10+
- Node.js 16+ (for frontend development)
- All Docker requirements above

### Setup Development Environment

```bash
# Clone repository
git clone --recurse-submodules https://github.com/AlphaSphereDotAI/chatacter_backend.git
cd chatacter_backend

# Create development environment file
cat > .env.dev << EOF
# Development configuration
MODEL__API_KEY=your-api-key
MODEL__URL=https://api.groq.com/openai/v1
MODEL__NAME=llama3-70b-8192
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=debug
EOF

# Create development compose override
cat > compose.dev.yaml << EOF
services:
  app:
    build:
      context: ./App
      dockerfile: Dockerfile.dev
    volumes:
      - ./App/src:/app/src:ro
      - ./logs:/app/logs
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
    command: ["python", "-m", "gradio", "src/app.py", "--reload"]
    
  video_generator:
    volumes:
      - ./VideoGenerator/src:/app/src:ro
    environment:
      - ENVIRONMENT=development
      
  voice_generator:
    volumes:
      - ./VoiceGenerator/src:/app/src:ro
    environment:
      - ENVIRONMENT=development
EOF

# Start in development mode
docker compose -f compose.yaml -f compose.dev.yaml up -d
```

### Individual Service Development

#### Chattr App Development
```bash
cd App
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m gradio src/app.py --reload
```

#### Video Generator Development
```bash
cd VideoGenerator
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/app.py
```

#### Voice Generator Development
```bash
cd VoiceGenerator
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/app.py
```

## Production Installation

### Step 1: Prepare Production Environment

```bash
# Create production directory
sudo mkdir -p /opt/chatacter
cd /opt/chatacter

# Clone repository
sudo git clone --recurse-submodules https://github.com/AlphaSphereDotAI/chatacter_backend.git .
sudo chown -R $USER:$USER /opt/chatacter
```

### Step 2: Production Configuration

```bash
# Create production environment file
cat > .env.prod << EOF
# Production configuration
MODEL__API_KEY=your-production-api-key
MODEL__URL=https://api.groq.com/openai/v1
MODEL__NAME=llama3-70b-8192

# Performance settings
MODEL__TEMPERATURE=0.0
WORKERS=4
MAX_CONCURRENT_REQUESTS=100

# Security settings
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
SECRET_KEY=your-super-secret-production-key

# Database settings
VECTOR_DATABASE__NAME=chatacter_prod
REDIS_URL=redis://redis:6379/0

# Storage settings
ASSETS_PATH=/data/assets
LOGS_PATH=/data/logs

# Resource limits
MEMORY_LIMIT=8g
CPU_LIMIT=4.0
GPU_MEMORY_LIMIT=8g
EOF

# Set appropriate permissions
chmod 600 .env.prod
```

### Step 3: Production Compose Configuration

```bash
# Create production compose file
cat > compose.prod.yaml << EOF
services:
  app:
    restart: unless-stopped
    environment:
      - ENVIRONMENT=production
    deploy:
      resources:
        limits:
          memory: 8g
          cpus: '4.0'
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7860/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "5"

  video_generator:
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 16g
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  voice_generator:
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 8g
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  vector_database:
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 4g
          cpus: '2.0'

  # Add reverse proxy for production
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - app
    restart: unless-stopped

  # Add Redis for session management
  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped
    command: redis-server --appendonly yes

volumes:
  redis_data:
EOF
```

### Step 4: SSL Configuration (Production)

```bash
# Create nginx configuration
cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream app {
        server app:7860;
    }

    server {
        listen 80;
        server_name your-domain.com www.your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com www.your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF

# Generate SSL certificates (use Let's Encrypt for production)
mkdir -p ssl
# ... SSL certificate setup ...
```

### Step 5: Launch Production

```bash
# Start production services
docker compose -f compose.yaml -f compose.prod.yaml up -d

# Monitor services
docker compose logs -f
```

## Kubernetes Installation

For large-scale deployments using Kubernetes.

### Step 1: Prepare Kubernetes Manifests

```bash
# Create kubernetes directory
mkdir -p k8s

# Generate manifests
cat > k8s/namespace.yaml << 'EOF'
apiVersion: v1
kind: Namespace
metadata:
  name: chatacter
EOF

cat > k8s/configmap.yaml << 'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: chatacter-config
  namespace: chatacter
data:
  MODEL__URL: "https://api.groq.com/openai/v1"
  MODEL__NAME: "llama3-70b-8192"
  VECTOR_DATABASE__NAME: "chatacter"
  VECTOR_DATABASE__URL: "http://qdrant:6333"
EOF

# Add secret for API key
cat > k8s/secret.yaml << 'EOF'
apiVersion: v1
kind: Secret
metadata:
  name: chatacter-secrets
  namespace: chatacter
type: Opaque
data:
  MODEL__API_KEY: <base64-encoded-api-key>
EOF
```

### Step 2: Deploy to Kubernetes

```bash
# Apply manifests
kubectl apply -f k8s/

# Monitor deployment
kubectl get pods -n chatacter -w
```

## Troubleshooting

### Common Issues

#### Docker Permission Issues
```bash
# Fix Docker permissions
sudo usermod -aG docker $USER
newgrp docker
```

#### GPU Not Detected
```bash
# Check NVIDIA drivers
nvidia-smi

# Check Docker GPU support
docker run --rm --gpus all nvidia/cuda:11.0.3-base-ubuntu20.04 nvidia-smi

# Reinstall NVIDIA Docker if needed
sudo apt-get purge nvidia-docker2
sudo apt-get install nvidia-docker2
sudo systemctl restart docker
```

#### Service Health Check Failures
```bash
# Check service logs
docker compose logs app

# Check service health
curl -f http://localhost:8000/health

# Restart unhealthy services
docker compose restart app
```

#### Memory Issues
```bash
# Check memory usage
docker stats

# Increase Docker memory limits
# Edit Docker Desktop settings or system resources
```

### Performance Optimization

#### GPU Memory Optimization
```bash
# Set GPU memory growth
export CUDA_VISIBLE_DEVICES=0
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:1024
```

#### CPU Optimization
```bash
# Set CPU affinity
docker compose up -d --cpuset-cpus="0-7"
```

### Monitoring Installation

```bash
# Add monitoring to compose
cat >> compose.yaml << 'EOF'
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
EOF
```

---

For additional help, see the [Troubleshooting Guide](./troubleshooting.md) or open an issue on GitHub.