# FAQ - Frequently Asked Questions

Common questions and answers about the Chatacter Backend system.

## General Questions

### What is Chatacter Backend?

Chatacter Backend is a sophisticated AI-powered system that enables character-based conversations with integrated video and voice generation capabilities. It consists of three main services:

- **Chattr**: Main chat application with AI character interactions
- **Visualizr**: Video generation service for visual content
- **Vocalizr**: Voice synthesis service for audio generation

### What makes it different from other chatbots?

- **Multimodal**: Combines text, voice, and video generation
- **Character-focused**: Designed for persistent character personalities
- **Modular**: Microservices architecture for scalability
- **Open source**: Customizable and extensible
- **Production-ready**: Docker-based deployment with monitoring

### What are the system requirements?

**Minimum:**
- 8GB RAM, 4 CPU cores
- 50GB storage
- NVIDIA GPU with 6GB+ VRAM (recommended)

**Recommended:**
- 32GB+ RAM, 16+ CPU cores
- 100GB+ SSD storage
- NVIDIA RTX 3080+ or A100 GPU

## Installation & Setup

### How do I get started quickly?

1. Clone the repository:
   ```bash
   git clone --recurse-submodules https://github.com/AlphaSphereDotAI/chatacter_backend.git
   cd chatacter_backend
   ```

2. Set your API key:
   ```bash
   export MODEL__API_KEY="your-api-key-here"
   ```

3. Start the services:
   ```bash
   docker compose up -d
   ```

4. Access at http://localhost:8000

See the [Quick Start Guide](./quick-start.md) for detailed instructions.

### Do I need an NVIDIA GPU?

- **Required for**: Video and voice generation services
- **Not required for**: Text-only chat functionality
- **Alternatives**: Use cloud GPU services or CPU-only mode (slower)

### What API keys do I need?

You need an API key from one of these LLM providers:
- **Groq** (recommended): Free tier available, fast inference
- **OpenAI**: GPT-4, GPT-3.5-turbo models
- **Other**: Any OpenAI-compatible API

Get a Groq API key at [console.groq.com](https://console.groq.com).

### Can I run this without Docker?

Yes, but Docker is recommended. For manual installation:

1. Install Python 3.10+
2. Set up each service individually (App, VideoGenerator, VoiceGenerator)
3. Install and configure Qdrant vector database
4. Install and configure Redis (optional)

See the [Development Guide](./development.md) for details.

## Configuration

### How do I change the AI model?

Set these environment variables:

```bash
# For Groq
MODEL__URL=https://api.groq.com/openai/v1
MODEL__NAME=llama3-70b-8192

# For OpenAI
MODEL__URL=https://api.openai.com/v1
MODEL__NAME=gpt-4o-mini
```

### How do I customize character personalities?

Characters are defined in the application configuration. You can:

1. **Modify existing characters** by updating their personality descriptions
2. **Add new characters** through the API or configuration files
3. **Customize behavior** with system prompts and temperature settings

### Can I use my own AI models?

Yes, if they're compatible with the OpenAI API format:

```bash
MODEL__URL=http://your-local-model:8000/v1
MODEL__NAME=your-custom-model
```

Popular options include:
- **Ollama**: Local model serving
- **vLLM**: High-performance inference
- **LocalAI**: OpenAI-compatible local API

### How do I scale for production?

1. **Horizontal scaling**: Run multiple instances
   ```bash
   docker compose up -d --scale app=3
   ```

2. **Load balancing**: Use NGINX or cloud load balancer

3. **Resource allocation**: Adjust memory and CPU limits
   ```yaml
   deploy:
     resources:
       limits:
         memory: 8g
         cpus: '4.0'
   ```

4. **Database clustering**: Use Qdrant Cloud or clustered deployment

## Features & Capabilities

### What video generation models are supported?

- **Stable Video Diffusion**: High-quality text-to-video
- **AnimateDiff**: Image-to-video animation
- **Custom models**: Add your own models via the plugin system

### What voice models are available?

- **Coqui TTS**: High-quality neural text-to-speech
- **Bark**: Expressive multilingual synthesis
- **Custom voices**: Voice cloning from samples

### Can characters remember previous conversations?

Yes, through multiple memory systems:

1. **Short-term memory**: Recent conversation context (Redis)
2. **Long-term memory**: Semantic search through conversation history (Qdrant)
3. **Character memory**: Persistent character knowledge and preferences

### How does the vector database work?

The system uses Qdrant to store and search conversation embeddings:

1. **Storage**: Conversations are converted to vector embeddings
2. **Retrieval**: Relevant context is retrieved for each new message
3. **Memory**: Characters can reference past conversations and learned information

## Troubleshooting

### Services won't start - what should I check?

1. **Check ports**: Ensure ports 8000, 8001, 8002, 6333 are available
2. **Check API key**: Verify your `MODEL__API_KEY` is set correctly
3. **Check resources**: Ensure sufficient RAM and GPU memory
4. **Check logs**: `docker compose logs app`

### I get "API key not found" errors

1. **Set the environment variable**:
   ```bash
   export MODEL__API_KEY="your-api-key-here"
   ```

2. **Or create a .env file**:
   ```bash
   echo "MODEL__API_KEY=your-api-key-here" > .env
   ```

3. **Restart services**:
   ```bash
   docker compose restart app
   ```

### Video/voice generation is very slow

1. **Check GPU usage**: `nvidia-smi`
2. **Reduce quality settings**: Lower resolution, fewer inference steps
3. **Check GPU memory**: May need more VRAM
4. **Use faster models**: Switch to lighter-weight models

### Out of memory errors

1. **GPU memory**: Reduce batch sizes or use model optimization
2. **System memory**: Increase Docker memory limits
3. **Clear caches**: Restart services to clear memory
   ```bash
   docker compose restart
   ```

### Cannot connect to vector database

1. **Check Qdrant status**: `curl http://localhost:6333/`
2. **Check network**: Ensure containers can communicate
3. **Reset database**: 
   ```bash
   docker compose down
   docker volume rm chatacter_qdrant_storage
   docker compose up -d
   ```

## Development

### How do I contribute to the project?

1. **Fork the repository** on GitHub
2. **Set up development environment** (see [Development Guide](./development.md))
3. **Make your changes** and add tests
4. **Submit a pull request** with clear description

See the [Contributing Guide](./contributing.md) for detailed instructions.

### How do I add a new character?

1. **Via API**:
   ```python
   import requests
   
   response = requests.post("http://localhost:8000/api/v1/characters", json={
       "id": "my_character",
       "name": "My Character", 
       "personality": "Friendly and helpful",
       "system_prompt": "You are a friendly assistant..."
   })
   ```

2. **Via configuration file**: Update character definitions in the app configuration

### How do I add a new voice model?

1. **Add model to Vocalizr**: Update the voice generation service
2. **Register model**: Add model configuration
3. **Test integration**: Ensure it works with the main app

### Can I add custom API endpoints?

Yes, the system is built with FastAPI and is easily extensible:

```python
from fastapi import APIRouter

router = APIRouter()

@router.post("/api/v1/custom-endpoint")
async def custom_endpoint(data: dict):
    # Your custom logic here
    return {"result": "success"}

# Register router in main app
app.include_router(router)
```

## Performance & Optimization

### How can I improve response times?

1. **Use faster models**: 
   - Groq models (very fast)
   - Smaller models (llama3-8b vs llama3-70b)

2. **Enable caching**:
   ```bash
   CACHE_TTL=3600  # Cache responses for 1 hour
   ```

3. **Preload models**:
   ```bash
   PRELOAD_MODELS=true
   ```

4. **Optimize hardware**: More GPU memory, faster storage

### How much does it cost to run?

**API costs** (main expense):
- **Groq**: ~$0.10-0.50 per 1000 messages (free tier available)
- **OpenAI**: ~$0.50-2.00 per 1000 messages

**Infrastructure costs**:
- **Local**: GPU electricity costs
- **Cloud**: $50-500/month depending on usage and GPU type

### How do I monitor performance?

1. **Built-in metrics**: Enable Prometheus metrics
   ```bash
   ENABLE_METRICS=true
   ```

2. **Grafana dashboards**: Visualize performance data

3. **Log analysis**: Monitor response times and error rates

4. **Resource monitoring**: Track CPU, memory, and GPU usage

## Deployment

### Can I deploy to the cloud?

Yes, multiple options:

1. **Docker Compose**: Simple cloud VM deployment
2. **Kubernetes**: Scalable orchestration (AWS EKS, GKE, AKS)
3. **Cloud Run**: Serverless deployment (limited GPU support)
4. **Cloud VMs**: Custom deployment on cloud instances

See the [Deployment Guide](./deployment.md) for detailed instructions.

### How do I set up SSL/HTTPS?

1. **With reverse proxy** (recommended):
   ```bash
   # Use NGINX with Let's Encrypt
   certbot --nginx -d yourdomain.com
   ```

2. **With cloud load balancer**: Configure SSL termination

3. **Application-level**: Configure Gradio with SSL certificates

### How do I backup the system?

1. **Vector database**: Regular Qdrant snapshots
2. **Generated content**: Backup assets directory
3. **Configuration**: Version control for configurations
4. **Automated backups**: Use cron jobs or cloud backup services

## Security

### Is this secure for production use?

The system includes security features, but you should:

1. **Use HTTPS**: Set up SSL/TLS encryption
2. **Secure API keys**: Use environment variables, not hardcoded values
3. **Network security**: Firewall rules, VPN access for management
4. **Regular updates**: Keep all components updated
5. **Access control**: Implement authentication and authorization

### How do I protect API endpoints?

1. **API key authentication**:
   ```bash
   REQUIRE_API_KEY=true
   ```

2. **Rate limiting**:
   ```bash
   API_RATE_LIMIT=60  # Requests per minute
   ```

3. **CORS configuration**:
   ```bash
   CORS_ORIGINS=https://yourdomain.com
   ```

### Can I run this in a private network?

Yes, ideal for sensitive applications:

1. **Local deployment**: No external API calls needed for core functionality
2. **Air-gapped setup**: Use local AI models with Ollama or similar
3. **Private cloud**: Deploy in private cloud with VPN access

## Licensing & Usage

### What's the license?

Check the LICENSE file in each component repository. Generally open source with permissive licensing.

### Can I use this commercially?

Yes, for most use cases. Check specific component licenses for details.

### Can I modify the code?

Yes, the system is designed to be extensible and customizable.

## Getting Help

### Where can I get support?

1. **Documentation**: Check the [complete documentation](./README.md)
2. **GitHub Issues**: Report bugs and feature requests
3. **Community**: GitHub Discussions for questions
4. **Troubleshooting**: See the [Troubleshooting Guide](./troubleshooting.md)

### How do I report a bug?

1. **Search existing issues** first
2. **Create detailed issue** with:
   - Steps to reproduce
   - Expected vs actual behavior
   - System information
   - Logs and error messages

### How do I request a feature?

1. **Check existing feature requests**
2. **Create GitHub issue** with:
   - Clear description of the feature
   - Use cases and benefits
   - Proposed implementation (if any)

### Is commercial support available?

Contact the project maintainers for commercial support options, including:
- Custom development
- Training and consulting
- Priority support
- Enterprise features

---

Still have questions? Check the [complete documentation](./README.md) or open an issue on GitHub!