# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the Chatacter Backend system.

## Table of Contents

- [Common Issues](#common-issues)
- [Service-Specific Issues](#service-specific-issues)
- [Performance Issues](#performance-issues)
- [Configuration Issues](#configuration-issues)
- [Debugging Tools](#debugging-tools)
- [Getting Help](#getting-help)

## Common Issues

### Services Not Starting

#### Symptoms
- Containers fail to start
- Health checks failing
- Service unavailable errors

#### Diagnosis Steps

```bash
# Check service status
docker compose ps

# View service logs
docker compose logs app
docker compose logs video_generator
docker compose logs voice_generator
docker compose logs vector_database

# Check resource usage
docker stats

# Verify port availability
netstat -tlnp | grep :8000
netstat -tlnp | grep :6333
```

#### Solutions

**Port Conflicts:**
```bash
# Check what's using the port
sudo lsof -i :8000

# Kill conflicting process
sudo kill -9 <PID>

# Or change port in .env
echo "APP_PORT=8080" >> .env
```

**Memory Issues:**
```bash
# Check available memory
free -h

# Increase Docker memory limits
# Edit Docker Desktop settings or:
docker compose down
docker system prune -f
docker compose up -d
```

**GPU Access Issues:**
```bash
# Verify NVIDIA drivers
nvidia-smi

# Check Docker GPU support
docker run --rm --gpus all nvidia/cuda:11.0.3-base-ubuntu20.04 nvidia-smi

# Reinstall NVIDIA Docker runtime
sudo apt-get purge nvidia-docker2
sudo apt-get install nvidia-docker2
sudo systemctl restart docker
```

### API Key Issues

#### Symptoms
- Authentication errors (401)
- Model access denied
- Empty responses from LLM

#### Diagnosis
```bash
# Check if API key is set
echo $MODEL__API_KEY

# Verify API key format
# Groq: starts with "gsk_"
# OpenAI: starts with "sk-"

# Test API key manually
curl -H "Authorization: Bearer $MODEL__API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"llama3-8b-8192","messages":[{"role":"user","content":"test"}]}' \
     https://api.groq.com/openai/v1/chat/completions
```

#### Solutions

**Invalid API Key:**
```bash
# Get new API key from provider
# For Groq: https://console.groq.com/keys
# For OpenAI: https://platform.openai.com/api-keys

# Update environment variable
export MODEL__API_KEY="your-new-api-key"

# Or update .env file
echo "MODEL__API_KEY=your-new-api-key" > .env

# Restart services
docker compose restart app
```

**Wrong Model Name:**
```bash
# List available models
curl -H "Authorization: Bearer $MODEL__API_KEY" \
     https://api.groq.com/openai/v1/models

# Update model name in .env
echo "MODEL__NAME=llama3-8b-8192" >> .env
```

### Connection Issues

#### Symptoms
- Services can't communicate
- Database connection errors
- Media generation timeouts

#### Diagnosis
```bash
# Check Docker network
docker network ls
docker network inspect chatacter_default

# Test service connectivity
docker compose exec app curl -f http://vector_database:6333/health
docker compose exec app curl -f http://video_generator:7860/health

# Check DNS resolution
docker compose exec app nslookup vector_database
```

#### Solutions

**Network Issues:**
```bash
# Recreate Docker network
docker compose down
docker network prune
docker compose up -d

# Check firewall rules
sudo ufw status
```

**Service Discovery Issues:**
```bash
# Use IP addresses instead of hostnames
docker compose exec app ip route

# Update service URLs in .env
VECTOR_DATABASE__URL=http://172.18.0.3:6333
```

## Service-Specific Issues

### Chattr App Issues

#### Memory Leaks
```bash
# Monitor memory usage
docker stats app

# Check for memory leaks in logs
docker compose logs app | grep -i "memory\|oom"

# Restart service
docker compose restart app
```

#### Model Loading Failures
```bash
# Check model configuration
docker compose exec app env | grep MODEL__

# Verify model availability
curl -H "Authorization: Bearer $MODEL__API_KEY" \
     "$MODEL__URL/models"

# Test with smaller model
export MODEL__NAME="llama3-8b-8192"
docker compose restart app
```

### Video Generator Issues

#### GPU Out of Memory
```bash
# Check GPU memory usage
nvidia-smi

# Reduce batch size or resolution
docker compose exec video_generator nvidia-smi
docker compose restart video_generator

# Clear GPU cache
docker compose exec video_generator python -c "
import torch
torch.cuda.empty_cache()
print('GPU cache cleared')
"
```

#### Slow Generation
```bash
# Check GPU utilization
watch -n 1 nvidia-smi

# Optimize generation parameters
curl -X POST http://localhost:8002/api/v1/generate/video \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "test",
    "num_inference_steps": 10,
    "width": 512,
    "height": 512
  }'
```

### Voice Generator Issues

#### Audio Quality Problems
```bash
# Check sample rate configuration
docker compose logs voice_generator | grep sample_rate

# Test with different voice models
curl -X POST http://localhost:8001/api/v1/generate/speech \
  -H "Content-Type: application/json" \
  -d '{
    "text": "test audio quality",
    "voice_model": "coqui-tts",
    "sample_rate": 22050
  }'
```

#### Model Loading Errors
```bash
# Check available disk space
df -h

# Clear model cache
docker compose exec voice_generator rm -rf /home/nonroot/.cache/

# Restart with fresh models
docker compose down
docker volume rm chatacter_huggingface
docker compose up -d
```

### Vector Database Issues

#### Index Corruption
```bash
# Check Qdrant status
curl http://localhost:6333/

# View collection info
curl http://localhost:6333/collections/

# Recreate collection if corrupted
curl -X DELETE http://localhost:6333/collections/chattr
docker compose restart vector_database
```

#### Search Performance
```bash
# Check index size
curl http://localhost:6333/collections/chattr

# Optimize collection
curl -X POST http://localhost:6333/collections/chattr/index \
  -H "Content-Type: application/json" \
  -d '{"operation": "optimize"}'
```

## Performance Issues

### High CPU Usage

#### Diagnosis
```bash
# Monitor CPU usage
top -p $(docker compose ps -q)

# Check container limits
docker inspect $(docker compose ps -q app) | grep -i cpu

# Profile application
docker compose exec app python -m cProfile -o profile.out src/app.py
```

#### Solutions
```bash
# Limit CPU usage
docker compose down
echo "
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2.0'
" > compose.override.yaml
docker compose up -d

# Optimize worker count
export WORKERS=2
docker compose restart app
```

### High Memory Usage

#### Diagnosis
```bash
# Check memory usage
docker stats --no-stream

# Monitor memory over time
while true; do 
  docker stats --no-stream | head -n 5
  sleep 10
done
```

#### Solutions
```bash
# Increase memory limits
docker compose down
echo "
services:
  app:
    deploy:
      resources:
        limits:
          memory: 8g
" > compose.override.yaml
docker compose up -d

# Clear caches
docker compose exec app python -c "
import gc
gc.collect()
"
```

### Slow Response Times

#### Diagnosis
```bash
# Test API response times
time curl -X POST http://localhost:8000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "hello", "character_id": "assistant"}'

# Check database query times
curl http://localhost:6333/metrics
```

#### Solutions
```bash
# Enable caching
export CACHE_TTL=3600
docker compose restart app

# Optimize database
curl -X POST http://localhost:6333/collections/chattr/index

# Scale services
docker compose up -d --scale app=2
```

## Configuration Issues

### Environment Variables

#### Common Mistakes
```bash
# Check all environment variables
docker compose exec app env | sort

# Verify Boolean values (use true/false, not True/False)
export DEBUG=true  # ✅ Correct
export DEBUG=True  # ❌ Wrong

# Check for typos in variable names
export MODEL__API_KEY=...    # ✅ Correct
export MODEL_API_KEY=...     # ❌ Wrong (single underscore)
```

#### Validation Script
```bash
#!/bin/bash
# validate-config.sh

echo "Validating Chatacter Backend configuration..."

# Required variables
required_vars=("MODEL__API_KEY")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Required variable $var is not set"
        exit 1
    else
        echo "✅ $var is set"
    fi
done

# Service connectivity
services=("8000" "6333" "8001" "8002")
for port in "${services[@]}"; do
    if curl -f "http://localhost:$port/health" >/dev/null 2>&1; then
        echo "✅ Service on port $port is healthy"
    else
        echo "❌ Service on port $port is not responding"
    fi
done

echo "Configuration validation complete!"
```

### Volume Permissions

#### Symptoms
- Permission denied errors
- Files not persisting
- Container startup failures

#### Solutions
```bash
# Fix volume permissions
sudo chown -R $USER:$USER ./data/
sudo chmod -R 755 ./data/

# Use proper user in containers
docker compose exec --user root app chown -R nonroot:nonroot /home/nonroot/assets

# Create volumes with correct permissions
mkdir -p ./data/{assets,logs,qdrant}
chmod 755 ./data/*
```

## Debugging Tools

### Health Check Scripts

```bash
#!/bin/bash
# health-check.sh

echo "=== Chatacter Backend Health Check ==="

# Service status
echo "1. Service Status:"
docker compose ps

# Health endpoints
echo -e "\n2. Health Endpoints:"
services=("app:8000" "video_generator:8002" "voice_generator:8001" "vector_database:6333")
for service in "${services[@]}"; do
    name="${service%:*}"
    port="${service#*:}"
    if curl -sf "http://localhost:$port/health" > /dev/null; then
        echo "✅ $name (port $port)"
    else
        echo "❌ $name (port $port)"
    fi
done

# Resource usage
echo -e "\n3. Resource Usage:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# GPU status
echo -e "\n4. GPU Status:"
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv,noheader
else
    echo "NVIDIA drivers not available"
fi
```

### Log Analysis

```bash
#!/bin/bash
# analyze-logs.sh

echo "=== Log Analysis ==="

# Error patterns
echo "1. Recent Errors:"
docker compose logs --since=1h | grep -i error | tail -10

# Memory warnings
echo -e "\n2. Memory Warnings:"
docker compose logs --since=1h | grep -i "memory\|oom" | tail -5

# Performance issues
echo -e "\n3. Performance Issues:"
docker compose logs --since=1h | grep -i "slow\|timeout\|timeout" | tail -5

# API errors
echo -e "\n4. API Errors:"
docker compose logs app --since=1h | grep -E "(401|403|429|500|502|503)" | tail -5
```

### Network Diagnostics

```bash
#!/bin/bash
# network-diagnostics.sh

echo "=== Network Diagnostics ==="

# Container network info
echo "1. Container Network:"
docker network inspect $(docker compose ps -q | head -1) | grep -A 10 "Networks"

# Service connectivity
echo -e "\n2. Inter-Service Connectivity:"
docker compose exec app ping -c 1 vector_database
docker compose exec app ping -c 1 video_generator
docker compose exec app ping -c 1 voice_generator

# Port accessibility
echo -e "\n3. Port Accessibility:"
for port in 8000 8001 8002 6333; do
    if nc -z localhost $port; then
        echo "✅ Port $port is accessible"
    else
        echo "❌ Port $port is not accessible"
    fi
done
```

## Getting Help

### Information to Gather

When reporting issues, please include:

1. **System Information:**
   ```bash
   # OS and Docker versions
   uname -a
   docker --version
   docker compose version
   
   # Hardware info
   lscpu | grep "Model name"
   free -h
   nvidia-smi | head -10
   ```

2. **Configuration:**
   ```bash
   # Environment variables (redact sensitive info)
   docker compose exec app env | grep -v API_KEY | sort
   
   # Service status
   docker compose ps
   ```

3. **Logs:**
   ```bash
   # Recent logs with timestamps
   docker compose logs --timestamps --since=1h > chatacter-logs.txt
   ```

4. **Error Details:**
   - Exact error messages
   - Steps to reproduce
   - Expected vs actual behavior

### Community Support

- **GitHub Issues**: [Open an issue](https://github.com/AlphaSphereDotAI/chatacter_backend/issues)
- **Documentation**: Check [docs](./README.md) for additional guides
- **Component Issues**: Check individual component repositories:
  - [Chattr Issues](https://github.com/AlphaSphereDotAI/chattr/issues)
  - [Visualizr Issues](https://github.com/AlphaSphereDotAI/visualizr/issues)
  - [Vocalizr Issues](https://github.com/AlphaSphereDotAI/vocalizr/issues)

### Quick Fixes

**Reset Everything:**
```bash
# Nuclear option - resets all data
docker compose down -v
docker system prune -af
git pull
git submodule update --recursive
docker compose up -d
```

**Restart Services:**
```bash
# Restart specific service
docker compose restart app

# Restart all services
docker compose restart

# Restart with fresh containers
docker compose down
docker compose up -d
```

**Clear Caches:**
```bash
# Clear Docker caches
docker system prune -f

# Clear model caches
docker compose exec video_generator rm -rf /home/nonroot/.cache/
docker compose exec voice_generator rm -rf /home/nonroot/.cache/

# Clear application caches
docker compose exec app python -c "
import shutil
import os
cache_dirs = ['/tmp/cache', '/home/nonroot/.cache']
for cache_dir in cache_dirs:
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
        print(f'Cleared {cache_dir}')
"
```

---

If you're still experiencing issues after following this guide, please open an issue on GitHub with the diagnostic information requested above.