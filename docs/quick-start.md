# Quick Start Guide

Get the Chatacter Backend up and running in less than 5 minutes.

## Prerequisites Check

Before starting, ensure you have:

- ✅ **Docker** (20.10+): `docker --version`
- ✅ **Docker Compose** (2.0+): `docker compose version`
- ✅ **NVIDIA GPU** (for video/voice): `nvidia-smi`
- ✅ **API Key** from Groq or OpenAI

## Step 1: Clone Repository

```bash
git clone --recurse-submodules https://github.com/AlphaSphereDotAI/chatacter_backend.git
cd chatacter_backend
```

💡 **Note**: The `--recurse-submodules` flag is essential as this project uses git submodules.

## Step 2: Set Environment Variables

Create a `.env` file or set environment variables:

```bash
# Method 1: Create .env file
cat > .env << EOF
MODEL__API_KEY=your-api-key-here
MODEL__NAME=llama3-70b-8192
MODEL__URL=https://api.groq.com/openai/v1
EOF

# Method 2: Export directly
export MODEL__API_KEY="your-api-key-here"
```

### Getting API Keys

**For Groq (Recommended - Free Tier Available):**
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up and navigate to API Keys
3. Create a new API key
4. Copy the key to your `.env` file

**For OpenAI:**
1. Visit [platform.openai.com](https://platform.openai.com)
2. Go to API Keys section
3. Create a new secret key
4. Update environment variables:
   ```bash
   MODEL__URL=https://api.openai.com/v1
   MODEL__NAME=gpt-4o-mini
   ```

## Step 3: Launch Services

```bash
# Start all services in background
docker compose up -d

# View startup logs
docker compose logs -f
```

## Step 4: Verify Installation

Check that all services are running:

```bash
# Check service status
docker compose ps

# Expected output:
# NAME        IMAGE                    STATUS         PORTS
# chattr      ghcr.io/...             Up (healthy)   0.0.0.0:8000->7860/tcp
# qdrant      qdrant/qdrant:latest     Up             0.0.0.0:6333->6333/tcp
# visualizr   ghcr.io/...             Up (healthy)   0.0.0.0:8002->7860/tcp
# vocalizr    ghcr.io/...             Up             0.0.0.0:8001->7860/tcp
```

## Step 5: Access the Application

Once all services are healthy (may take 2-3 minutes):

- **🤖 Main Chat Interface**: http://localhost:8000
- **🎬 Video Generator**: http://localhost:8002
- **🔊 Voice Generator**: http://localhost:8001
- **🗃️ Vector Database Dashboard**: http://localhost:6333/dashboard

## Quick Test

1. Open http://localhost:8000 in your browser
2. Start a conversation with a character
3. Try generating voice with the 🔊 button
4. Try generating video with the 🎬 button

## Common Issues

### Services Not Starting
```bash
# Check logs for errors
docker compose logs app
docker compose logs video_generator
docker compose logs voice_generator

# Restart specific service
docker compose restart app
```

### GPU Access Issues
```bash
# Verify NVIDIA Docker runtime
docker run --rm --gpus all nvidia/cuda:11.0.3-base-ubuntu20.04 nvidia-smi

# If fails, install nvidia-docker2:
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
```

### API Key Issues
```bash
# Verify environment variables are set
docker compose exec app printenv | grep MODEL__

# Update API key without restart
docker compose restart app
```

## Next Steps

- **[📖 Full Documentation](./README.md)** - Complete documentation index
- **[🏗️ Architecture Guide](./architecture.md)** - Understand the system design
- **[🔌 API Documentation](./api/)** - Integrate with the APIs
- **[⚙️ Configuration](./configuration.md)** - Customize your setup
- **[🚀 Production Deployment](./deployment.md)** - Deploy to production

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](./troubleshooting.md)
2. Review service logs: `docker compose logs <service-name>`
3. Open an [issue on GitHub](https://github.com/AlphaSphereDotAI/chatacter_backend/issues)

---

**🎉 Congratulations!** You now have a fully functional Chatacter Backend system running locally.