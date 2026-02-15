# Environment Variables Reference

Complete reference for all environment variables used in the Chatacter Backend system.

## Quick Reference

| Variable | Service | Required | Default | Description |
|----------|---------|----------|---------|-------------|
| `MODEL__API_KEY` | App | ✅ | - | API key for LLM service |
| `MODEL__URL` | App | ❌ | `https://api.groq.com/openai/v1` | LLM API endpoint |
| `MODEL__NAME` | App | ❌ | `llama3-70b-8192` | Model name |
| `VECTOR_DATABASE__URL` | App | ❌ | `http://vector_database:6333` | Qdrant URL |
| `VOICE_GENERATOR_MCP__URL` | App | ❌ | `http://localhost:8001/gradio_api/mcp/sse` | Voice service URL |
| `VIDEO_GENERATOR_MCP__URL` | App | ❌ | `http://localhost:8002/gradio_api/mcp/sse` | Video service URL |
| `GRADIO_SERVER_PORT` | All | ❌ | `7860` | Service port |

## Core Application (Chattr)

### Model Configuration

```bash
# Required: API key for LLM service
MODEL__API_KEY=your-api-key-here

# OpenAI-compatible API endpoint
MODEL__URL=https://api.groq.com/openai/v1
# Alternatives:
# MODEL__URL=https://api.openai.com/v1
# MODEL__URL=https://api.anthropic.com/v1

# Model name to use
MODEL__NAME=llama3-70b-8192
# Popular options:
# Groq: llama3-8b-8192, llama3-70b-8192, mixtral-8x7b-32768
# OpenAI: gpt-4o-mini, gpt-4o, gpt-3.5-turbo

# Model parameters
MODEL__TEMPERATURE=0.0          # Creativity (0.0-1.0)
MODEL__MAX_TOKENS=4096          # Maximum response tokens
MODEL__TOP_P=1.0               # Nucleus sampling
MODEL__FREQUENCY_PENALTY=0.0    # Repetition penalty
MODEL__PRESENCE_PENALTY=0.0     # Topic diversity
```

### Vector Database Configuration

```bash
# Qdrant connection URL
VECTOR_DATABASE__URL=http://vector_database:6333
# Cloud: https://your-cluster.qdrant.cloud:6333

# Collection name for vectors
VECTOR_DATABASE__NAME=chattr
# Production: chatacter_prod

# API key for Qdrant Cloud (optional)
VECTOR_DATABASE__API_KEY=your-qdrant-api-key

# Connection settings
VECTOR_DATABASE__TIMEOUT=30     # Connection timeout (seconds)
VECTOR_DATABASE__POOL_SIZE=10   # Connection pool size
VECTOR_DATABASE__RETRY_COUNT=3  # Retry attempts
```

### Memory and Caching

```bash
# Redis URL for short-term memory
SHORT_TERM_MEMORY__URL=redis://localhost:6379
# With auth: redis://:password@localhost:6379
# Cluster: redis://redis-cluster:6379

# Memory settings
SHORT_TERM_MEMORY__TTL=3600     # Session expiry (seconds)
SHORT_TERM_MEMORY__MAX_SIZE=100 # Max entries per session
SHORT_TERM_MEMORY__PREFIX=chat  # Key prefix

# Application cache
CACHE_TTL=300                   # Response cache TTL
CACHE_BACKEND=redis             # Cache backend (redis, memory)
CACHE_MAX_SIZE=1000            # Max cache entries
```

### Service Integration

```bash
# Voice generation service
VOICE_GENERATOR_MCP__URL=http://localhost:8001/gradio_api/mcp/sse
# Production: http://vocalizr:7860/gradio_api/mcp/sse

# Video generation service  
VIDEO_GENERATOR_MCP__URL=http://localhost:8002/gradio_api/mcp/sse
# Production: http://visualizr:7860/gradio_api/mcp/sse

# Service timeouts
VOICE_GENERATOR_TIMEOUT=60      # Voice generation timeout
VIDEO_GENERATOR_TIMEOUT=120     # Video generation timeout
SERVICE_RETRY_COUNT=3           # Service retry attempts
```

### Directory Configuration

```bash
# Base directory for all assets
DIRECTORY__ASSETS=./assets
# Production: /data/assets

# Subdirectories
DIRECTORY__LOG=./logs           # Log files
DIRECTORY__IMAGE=./assets/image # Image assets
DIRECTORY__AUDIO=./assets/audio # Audio files
DIRECTORY__VIDEO=./assets/video # Video files
DIRECTORY__TEMP=/tmp           # Temporary files

# Storage backend
STORAGE_BACKEND=local          # local, s3, gcs, azure
S3_BUCKET=chatacter-assets     # S3 bucket name
S3_REGION=us-west-2           # S3 region
```

## Server Configuration

### Gradio Settings

```bash
# Server port
GRADIO_SERVER_PORT=7860
# Alternative ports: 8000, 8001, 8002

# Server binding
GRADIO_SERVER_NAME=0.0.0.0     # Bind to all interfaces
# Local only: 127.0.0.1

# Server options
GRADIO_ROOT_PATH=/             # Root path for reverse proxy
GRADIO_ANALYTICS_ENABLED=false # Disable analytics
GRADIO_SHARE=false            # Disable public sharing
```

### Performance Settings

```bash
# Worker processes
WORKERS=1                      # Number of worker processes
# Production: 4-8 workers

# Concurrency limits
MAX_CONCURRENT_REQUESTS=10     # Max concurrent requests
MAX_FILE_SIZE=100             # Max upload size (MB)
REQUEST_TIMEOUT=300           # Request timeout (seconds)

# Resource limits
MEMORY_LIMIT=8g               # Memory limit
CPU_LIMIT=4.0                 # CPU limit
GPU_MEMORY_LIMIT=12g          # GPU memory limit
```

### Character Configuration

```bash
# Default character
DEFAULT_CHARACTER=assistant

# Character settings
CHARACTER_MEMORY_SIZE=1000     # Character memory limit
CONTEXT_WINDOW_SIZE=4000      # Conversation context size
MAX_HISTORY_LENGTH=50         # Max conversation history

# Character customization
ENABLE_CHARACTER_CREATION=true # Allow custom characters
CHARACTER_CONFIG_PATH=./config/characters.yaml
```

## Content Generation

### Video Generation (Visualizr)

```bash
# Model configuration
VISUALIZR_MODEL=stable-diffusion-xl
VISUALIZR_DEVICE=cuda          # cuda, cpu, auto

# Generation parameters
VISUALIZR_STEPS=20             # Inference steps
VISUALIZR_GUIDANCE_SCALE=7.5   # Guidance scale
VISUALIZR_WIDTH=1024           # Default width
VISUALIZR_HEIGHT=1024          # Default height
VISUALIZR_BATCH_SIZE=1         # Batch size

# Performance
VISUALIZR_MEMORY_EFFICIENT=true # Memory optimization
VISUALIZR_COMPILE_MODEL=false   # Model compilation
VISUALIZR_QUEUE_SIZE=10        # Request queue size
```

### Voice Generation (Vocalizr)

```bash
# TTS model configuration
VOCALIZR_MODEL=coqui-tts       # Voice model
VOCALIZR_DEVICE=cuda           # Device selection

# Audio parameters
VOCALIZR_SAMPLE_RATE=22050     # Audio sample rate
VOCALIZR_VOICE_SPEED=1.0       # Speaking speed
VOCALIZR_VOICE_PITCH=1.0       # Voice pitch
VOCALIZR_VOICE_VOLUME=1.0      # Voice volume

# Quality settings
VOCALIZR_AUDIO_FORMAT=wav      # Output format
VOCALIZR_BITRATE=192           # Audio bitrate (kbps)
VOCALIZR_CHANNELS=1            # Audio channels (1=mono, 2=stereo)
```

## Security Configuration

### Authentication

```bash
# Application secret
SECRET_KEY=your-super-secret-key-here
# Generate: python -c "import secrets; print(secrets.token_urlsafe(32))"

# API authentication
REQUIRE_API_KEY=false          # Require API key for access
API_KEY_HEADER=X-API-Key       # API key header name
JWT_SECRET=your-jwt-secret     # JWT signing secret

# Session management
SESSION_TIMEOUT=3600           # Session timeout (seconds)
SESSION_COOKIE_SECURE=true     # Secure cookies (HTTPS only)
SESSION_COOKIE_HTTPONLY=true   # HTTP-only cookies
```

### CORS and Security

```bash
# Allowed hosts
ALLOWED_HOSTS=localhost,127.0.0.1
# Production: yourdomain.com,www.yourdomain.com

# CORS configuration
CORS_ORIGINS=*                 # Allowed origins
# Production: https://yourdomain.com,https://www.yourdomain.com
CORS_METHODS=GET,POST,PUT,DELETE # Allowed methods
CORS_HEADERS=*                 # Allowed headers

# Security headers
FORCE_HTTPS=false              # Force HTTPS redirect
X_FRAME_OPTIONS=DENY           # Frame options
X_CONTENT_TYPE_OPTIONS=nosniff # Content type options
```

### Rate Limiting

```bash
# API rate limits
API_RATE_LIMIT=60              # Requests per minute
API_BURST_LIMIT=100            # Burst limit
RATE_LIMIT_STRATEGY=sliding_window # fixed_window, sliding_window

# Media generation limits
VIDEO_RATE_LIMIT=5             # Video requests per hour
VOICE_RATE_LIMIT=30            # Voice requests per hour
CONCURRENT_GENERATIONS=3       # Max concurrent generations
```

## Logging and Monitoring

### Logging Configuration

```bash
# Log level
LOG_LEVEL=INFO                 # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Log format
LOG_FORMAT=json                # json, text
LOG_INCLUDE_TIMESTAMP=true     # Include timestamps
LOG_INCLUDE_REQUEST_ID=true    # Include request IDs

# Log destinations
LOG_TO_CONSOLE=true           # Console logging
LOG_TO_FILE=true              # File logging
LOG_FILE_PATH=./logs/app.log  # Log file path
LOG_FILE_MAX_SIZE=100MB       # Max log file size
LOG_FILE_BACKUP_COUNT=5       # Number of backup files
```

### Metrics and Monitoring

```bash
# Prometheus metrics
ENABLE_METRICS=false          # Enable metrics endpoint
METRICS_PORT=9090             # Metrics endpoint port
METRICS_PATH=/metrics         # Metrics endpoint path

# Health checks
HEALTH_CHECK_INTERVAL=30      # Health check interval (seconds)
HEALTH_CHECK_TIMEOUT=10       # Health check timeout (seconds)

# External monitoring
SENTRY_DSN=                   # Sentry error tracking DSN
DATADOG_API_KEY=             # Datadog API key
NEW_RELIC_LICENSE_KEY=       # New Relic license key
```

## Development Settings

### Development Mode

```bash
# Environment
ENVIRONMENT=development        # development, staging, production
DEBUG=true                    # Enable debug mode
RELOAD=true                   # Auto-reload on code changes

# Development features
ENABLE_DEBUG_TOOLBAR=true     # Debug toolbar
ENABLE_PROFILING=false        # Performance profiling
ENABLE_CORS_ALL=true          # Allow all CORS origins
SKIP_AUTH=false               # Skip authentication (dangerous!)

# Model settings for development
PRELOAD_MODELS=false          # Don't preload models
USE_DUMMY_RESPONSES=false     # Use dummy responses for testing
FAST_GENERATION=true          # Use faster, lower-quality generation
```

### Testing Configuration

```bash
# Test database
TEST_VECTOR_DATABASE__URL=http://localhost:6333
TEST_REDIS_URL=redis://localhost:6379/1

# Test settings
TEST_API_KEY=test-api-key
TEST_MODEL_NAME=llama3-8b-8192 # Smaller model for tests
TEST_TIMEOUT=30               # Test timeout (seconds)

# Mock services
MOCK_VIDEO_GENERATION=true    # Mock video generation
MOCK_VOICE_GENERATION=true    # Mock voice generation
MOCK_LLM_RESPONSES=false      # Mock LLM responses
```

## Production Settings

### Production Environment

```bash
# Environment
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING

# Performance
WORKERS=4                     # Multiple workers
PRELOAD_MODELS=true          # Preload for faster response
MAX_CONCURRENT_REQUESTS=100  # Higher concurrency

# Security
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
FORCE_HTTPS=true
```

### High Availability

```bash
# Load balancing
LOAD_BALANCER_ALGORITHM=round_robin # round_robin, least_conn, ip_hash
STICKY_SESSIONS=false         # Session affinity
HEALTH_CHECK_PATH=/health     # Health check endpoint

# Database clustering
VECTOR_DATABASE__CLUSTER_URLS=http://qdrant1:6333,http://qdrant2:6333
REDIS_CLUSTER_URLS=redis://redis1:6379,redis://redis2:6379

# Failover settings
RETRY_ATTEMPTS=3              # Service retry attempts
CIRCUIT_BREAKER_THRESHOLD=5   # Circuit breaker threshold
FALLBACK_RESPONSES=true       # Use fallback responses on failure
```

## Docker Environment

### Container Configuration

```bash
# User settings
RUN_AS_USER=nonroot           # Container user
USER_ID=1000                  # User ID
GROUP_ID=1000                 # Group ID

# Resource limits
MEMORY_LIMIT=8g               # Memory limit
CPU_LIMIT=4.0                 # CPU limit
SHM_SIZE=2g                   # Shared memory size

# Health checks
HEALTHCHECK_INTERVAL=30s      # Health check interval
HEALTHCHECK_TIMEOUT=10s       # Health check timeout
HEALTHCHECK_RETRIES=3         # Health check retries
```

### Volume Configuration

```bash
# Volume mounts
ASSETS_VOLUME=/data/assets    # Assets volume
LOGS_VOLUME=/data/logs        # Logs volume
CONFIG_VOLUME=/data/config    # Config volume

# Permissions
VOLUME_PERMISSIONS=755        # Volume permissions
ASSET_CLEANUP_DAYS=7         # Auto-cleanup after days
```

## Example Configuration Files

### Development (.env.dev)

```bash
# Development environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG

# Model (using cheaper/faster options)
MODEL__API_KEY=your-dev-api-key
MODEL__NAME=llama3-8b-8192
MODEL__TEMPERATURE=0.1

# Local services
VECTOR_DATABASE__URL=http://localhost:6333
SHORT_TERM_MEMORY__URL=redis://localhost:6379
VOICE_GENERATOR_MCP__URL=http://localhost:8001/gradio_api/mcp/sse
VIDEO_GENERATOR_MCP__URL=http://localhost:8002/gradio_api/mcp/sse

# Development settings
WORKERS=1
PRELOAD_MODELS=false
ENABLE_DEBUG_TOOLBAR=true
CORS_ORIGINS=*
```

### Production (.env.prod)

```bash
# Production environment
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Model (production settings)
MODEL__API_KEY=your-production-api-key
MODEL__NAME=llama3-70b-8192
MODEL__TEMPERATURE=0.0

# Production services
VECTOR_DATABASE__URL=http://qdrant-cluster:6333
SHORT_TERM_MEMORY__URL=redis://redis-cluster:6379
VOICE_GENERATOR_MCP__URL=http://vocalizr:7860/gradio_api/mcp/sse
VIDEO_GENERATOR_MCP__URL=http://visualizr:7860/gradio_api/mcp/sse

# Security
SECRET_KEY=your-super-secure-production-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
FORCE_HTTPS=true

# Performance
WORKERS=4
MAX_CONCURRENT_REQUESTS=100
PRELOAD_MODELS=true
CACHE_TTL=3600

# Monitoring
ENABLE_METRICS=true
SENTRY_DSN=your-sentry-dsn
```

### Docker Compose (.env)

```bash
# Port mappings
APP_PORT=8000
VIDEO_PORT=8002
VOICE_PORT=8001
QDRANT_PORT=6333
REDIS_PORT=6379

# Volume paths
ASSETS_PATH=./data/assets
LOGS_PATH=./data/logs
QDRANT_PATH=./data/qdrant
REDIS_PATH=./data/redis

# Image tags
APP_IMAGE_TAG=latest
VIDEO_IMAGE_TAG=latest
VOICE_IMAGE_TAG=latest
QDRANT_IMAGE_TAG=latest
```

---

For additional configuration options, see the [Configuration Guide](./configuration.md).