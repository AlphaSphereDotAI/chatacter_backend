# Configuration Reference

Complete reference for all configuration options and environment variables used in the Chatacter Backend system.

## Table of Contents

- [Environment Variables](#environment-variables)
- [Service Configuration](#service-configuration)
- [Docker Compose Configuration](#docker-compose-configuration)
- [Production Settings](#production-settings)
- [Security Configuration](#security-configuration)

## Environment Variables

### Core Application Settings

#### Model Configuration
| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `MODEL__API_KEY` | API key for LLM service (Groq/OpenAI) | ✅ | `None` | `gsk_abc123...` |
| `MODEL__URL` | OpenAI-compatible API endpoint | ❌ | `https://api.groq.com/openai/v1` | `https://api.openai.com/v1` |
| `MODEL__NAME` | Model name to use for conversations | ❌ | `llama3-70b-8192` | `gpt-4o-mini` |
| `MODEL__TEMPERATURE` | Model creativity (0.0-1.0) | ❌ | `0.0` | `0.7` |
| `MODEL__MAX_TOKENS` | Maximum tokens per response | ❌ | `4096` | `2048` |
| `MODEL__TOP_P` | Nucleus sampling parameter | ❌ | `1.0` | `0.9` |

#### Vector Database Configuration
| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `VECTOR_DATABASE__URL` | Qdrant database connection URL | ❌ | `http://vector_database:6333` | `https://your-qdrant.com` |
| `VECTOR_DATABASE__NAME` | Collection name for vectors | ❌ | `chattr` | `production_chats` |
| `VECTOR_DATABASE__API_KEY` | API key for Qdrant Cloud | ❌ | `None` | `your-qdrant-key` |
| `VECTOR_DATABASE__TIMEOUT` | Connection timeout (seconds) | ❌ | `30` | `60` |

#### Memory Configuration
| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `SHORT_TERM_MEMORY__URL` | Redis URL for session storage | ❌ | `redis://localhost:6379` | `redis://redis:6379/0` |
| `SHORT_TERM_MEMORY__TTL` | Session expiry time (seconds) | ❌ | `3600` | `7200` |
| `SHORT_TERM_MEMORY__MAX_SIZE` | Max memory entries per session | ❌ | `100` | `200` |

#### Service URLs
| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `VOICE_GENERATOR_MCP__URL` | Voice generation service URL | ❌ | `http://localhost:8001/gradio_api/mcp/sse` | `http://vocalizr:7860/gradio_api/mcp/sse` |
| `VIDEO_GENERATOR_MCP__URL` | Video generation service URL | ❌ | `http://localhost:8002/gradio_api/mcp/sse` | `http://visualizr:7860/gradio_api/mcp/sse` |

#### Directory Configuration
| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `DIRECTORY__ASSETS` | Base directory for all assets | ❌ | `./assets` | `/data/assets` |
| `DIRECTORY__LOG` | Log files directory | ❌ | `./logs` | `/var/log/chatacter` |
| `DIRECTORY__IMAGE` | Image assets subdirectory | ❌ | `./assets/image` | `/data/assets/images` |
| `DIRECTORY__AUDIO` | Audio assets subdirectory | ❌ | `./assets/audio` | `/data/assets/audio` |
| `DIRECTORY__VIDEO` | Video assets subdirectory | ❌ | `./assets/video` | `/data/assets/videos` |

### Application Behavior

#### Server Configuration
| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `GRADIO_SERVER_PORT` | Port for Gradio interface | ❌ | `7860` | `8080` |
| `GRADIO_SERVER_NAME` | Interface binding address | ❌ | `0.0.0.0` | `127.0.0.1` |
| `MAX_FILE_SIZE` | Maximum upload file size (MB) | ❌ | `100` | `500` |
| `MAX_CONCURRENT_REQUESTS` | Concurrent request limit | ❌ | `10` | `50` |

#### Character Configuration
| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `DEFAULT_CHARACTER` | Default character personality | ❌ | `assistant` | `friendly_bot` |
| `CHARACTER_MEMORY_SIZE` | Character memory limit | ❌ | `1000` | `2000` |
| `CONTEXT_WINDOW_SIZE` | Conversation context size | ❌ | `4000` | `8000` |

#### Content Generation
| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `ENABLE_VIDEO_GENERATION` | Enable video generation | ❌ | `true` | `false` |
| `ENABLE_VOICE_GENERATION` | Enable voice generation | ❌ | `true` | `false` |
| `VIDEO_QUALITY` | Video generation quality | ❌ | `medium` | `high` |
| `AUDIO_QUALITY` | Audio generation quality | ❌ | `medium` | `high` |

### Security & Authentication

| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `SECRET_KEY` | Application secret key | ❌ | Auto-generated | `your-secret-key-here` |
| `ALLOWED_HOSTS` | Allowed host headers | ❌ | `*` | `yourdomain.com,www.yourdomain.com` |
| `CORS_ORIGINS` | CORS allowed origins | ❌ | `*` | `https://yourdomain.com` |
| `API_RATE_LIMIT` | API requests per minute | ❌ | `60` | `100` |

### Logging & Monitoring

| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `LOG_LEVEL` | Logging verbosity level | ❌ | `INFO` | `DEBUG` |
| `LOG_FORMAT` | Log message format | ❌ | `json` | `text` |
| `ENABLE_METRICS` | Enable Prometheus metrics | ❌ | `false` | `true` |
| `METRICS_PORT` | Metrics endpoint port | ❌ | `9090` | `8090` |

### Performance Tuning

| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `WORKERS` | Number of worker processes | ❌ | `1` | `4` |
| `WORKER_TIMEOUT` | Worker timeout (seconds) | ❌ | `300` | `600` |
| `CACHE_TTL` | Response cache TTL (seconds) | ❌ | `300` | `1800` |
| `PRELOAD_MODELS` | Preload AI models on startup | ❌ | `true` | `false` |

## Service Configuration

### Chattr App Configuration

The main application can be configured through both environment variables and a configuration file:

```yaml
# config.yaml (optional)
app:
  name: "Chatacter"
  version: "1.0.0"
  environment: "production"

model:
  provider: "groq"
  name: "llama3-70b-8192"
  temperature: 0.0
  max_tokens: 4096

characters:
  default: "assistant"
  available:
    - name: "assistant"
      personality: "helpful and friendly"
    - name: "creative"
      personality: "imaginative and artistic"

features:
  video_generation: true
  voice_generation: true
  memory_persistence: true
```

### Visualizr (Video Generator) Configuration

```bash
# Video generation specific settings
VISUALIZR_MODEL=stable-diffusion-xl
VISUALIZR_STEPS=20
VISUALIZR_GUIDANCE_SCALE=7.5
VISUALIZR_WIDTH=1024
VISUALIZR_HEIGHT=1024
VISUALIZR_BATCH_SIZE=1
```

### Vocalizr (Voice Generator) Configuration

```bash
# Voice generation specific settings
VOCALIZR_MODEL=coqui-tts
VOCALIZR_SAMPLE_RATE=22050
VOCALIZR_VOICE_SPEED=1.0
VOCALIZR_VOICE_PITCH=1.0
```

## Docker Compose Configuration

### Basic Configuration

```yaml
# compose.yaml
name: Chatacter
services:
  app:
    image: ghcr.io/alphaspheredotai/chattr:latest
    container_name: chattr
    environment:
      - MODEL__API_KEY=${MODEL__API_KEY}
      - MODEL__NAME=${MODEL__NAME:-llama3-70b-8192}
      - MODEL__URL=${MODEL__URL:-https://api.groq.com/openai/v1}
    ports:
      - "${APP_PORT:-8000}:7860"
    volumes:
      - assets:/home/nonroot/assets
      - logs:/home/nonroot/logs
    restart: unless-stopped
```

### Environment File (.env)

```bash
# .env file for Docker Compose
MODEL__API_KEY=your-api-key-here
MODEL__NAME=llama3-70b-8192
MODEL__URL=https://api.groq.com/openai/v1

# Port mappings
APP_PORT=8000
VIDEO_PORT=8002
VOICE_PORT=8001
QDRANT_PORT=6333

# Volume paths
ASSETS_PATH=./data/assets
LOGS_PATH=./data/logs
QDRANT_PATH=./data/qdrant
```

## Production Settings

### High Performance Configuration

```bash
# Production environment variables
ENVIRONMENT=production
WORKERS=4
MAX_CONCURRENT_REQUESTS=100
PRELOAD_MODELS=true
CACHE_TTL=1800

# Resource limits
MEMORY_LIMIT=16g
CPU_LIMIT=8.0
GPU_MEMORY_LIMIT=12g

# Security
SECRET_KEY=your-super-secret-production-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ORIGINS=https://yourdomain.com

# Monitoring
LOG_LEVEL=WARNING
ENABLE_METRICS=true
METRICS_PORT=9090
```

### Scalability Configuration

```bash
# Load balancing
LOAD_BALANCER_ALGORITHM=round_robin
STICKY_SESSIONS=false

# Database optimization
VECTOR_DATABASE__TIMEOUT=60
VECTOR_DATABASE__POOL_SIZE=10
SHORT_TERM_MEMORY__POOL_SIZE=20

# Caching
REDIS_MAX_CONNECTIONS=100
CACHE_BACKEND=redis
CACHE_TTL=3600
```

## Security Configuration

### API Security

```bash
# Authentication
REQUIRE_API_KEY=true
API_KEY_HEADER=X-API-Key
JWT_SECRET=your-jwt-secret

# Rate limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
RATE_LIMIT_PER_DAY=10000

# Content filtering
ENABLE_CONTENT_FILTER=true
BLOCKED_WORDS_FILE=/config/blocked_words.txt
```

### Network Security

```bash
# TLS/SSL
FORCE_HTTPS=true
SSL_CERT_PATH=/etc/ssl/certs/cert.pem
SSL_KEY_PATH=/etc/ssl/private/key.pem

# Firewall
ALLOWED_IPS=0.0.0.0/0
BLOCKED_IPS_FILE=/config/blocked_ips.txt
```

## Configuration Validation

### Environment Validation Script

```bash
#!/bin/bash
# validate-config.sh

echo "Validating Chatacter Backend configuration..."

# Check required variables
required_vars=("MODEL__API_KEY")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "ERROR: Required variable $var is not set"
        exit 1
    fi
done

# Check service connectivity
echo "Checking service connectivity..."
curl -f http://localhost:8000/health || echo "WARNING: Main app not responding"
curl -f http://localhost:6333/dashboard || echo "WARNING: Qdrant not responding"

echo "Configuration validation complete!"
```

### Docker Health Checks

```yaml
# Health check configuration
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:7860/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## Configuration Templates

### Development Template (.env.dev)

```bash
# Development configuration
MODEL__API_KEY=your-dev-api-key
MODEL__NAME=llama3-8b-8192
MODEL__TEMPERATURE=0.1
LOG_LEVEL=DEBUG
ENVIRONMENT=development
WORKERS=1
PRELOAD_MODELS=false
```

### Production Template (.env.prod)

```bash
# Production configuration
MODEL__API_KEY=your-prod-api-key
MODEL__NAME=llama3-70b-8192
MODEL__TEMPERATURE=0.0
LOG_LEVEL=INFO
ENVIRONMENT=production
WORKERS=4
PRELOAD_MODELS=true
ALLOWED_HOSTS=yourdomain.com
FORCE_HTTPS=true
```

---

This configuration reference provides comprehensive coverage of all available settings. For specific use cases, refer to the [Installation Guide](./installation.md) and [Deployment Guide](./deployment.md).