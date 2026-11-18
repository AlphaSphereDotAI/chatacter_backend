# Development Guide

This guide covers setting up a development environment, making changes, and contributing to the Chatacter Backend project.

## Table of Contents

- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Debugging](#debugging)
- [Performance Optimization](#performance-optimization)

## Development Environment Setup

### Prerequisites

- **Python 3.10+** for backend development
- **Docker & Docker Compose** for containerized development
- **Git** with submodule support
- **NVIDIA GPU** with CUDA support (recommended)
- **Code Editor** (VS Code, PyCharm, etc.)

### Local Development Setup

#### 1. Clone Repository

```bash
# Clone with all submodules
git clone --recurse-submodules https://github.com/AlphaSphereDotAI/chatacter_backend.git
cd chatacter_backend

# If already cloned without submodules
git submodule update --init --recursive
```

#### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"  # If setup.py exists
# Or install requirements directly
pip install -r requirements-dev.txt
```

#### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env.dev

# Edit with your development settings
nano .env.dev
```

**Development Environment Variables:**
```bash
# .env.dev
MODEL__API_KEY=your-dev-api-key
MODEL__NAME=llama3-8b-8192  # Smaller model for dev
MODEL__TEMPERATURE=0.1
LOG_LEVEL=DEBUG
ENVIRONMENT=development
WORKERS=1
PRELOAD_MODELS=false
ENABLE_DEBUG_TOOLBAR=true
```

#### 4. Start Development Services

```bash
# Start core services only
docker compose up -d vector_database

# Or start all services in development mode
docker compose -f compose.yaml -f compose.dev.yaml up -d
```

### Individual Service Development

#### Chattr App Development

```bash
cd App

# Install dependencies
pip install -r requirements.txt

# Run in development mode with auto-reload
python -m gradio src/app.py --reload --debug

# Or with custom settings
GRADIO_SERVER_PORT=8000 python src/app.py
```

#### Video Generator Development

```bash
cd VideoGenerator

# Install dependencies
pip install -r requirements.txt

# Run development server
python src/app.py --dev

# With specific GPU
CUDA_VISIBLE_DEVICES=0 python src/app.py
```

#### Voice Generator Development

```bash
cd VoiceGenerator

# Install dependencies
pip install -r requirements.txt

# Run with development settings
python src/app.py --debug
```

## Project Structure

### Repository Layout

```
chatacter_backend/
├── App/                    # Main application (submodule: chattr)
│   ├── src/               # Source code
│   ├── tests/             # Unit tests
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile        # Container configuration
├── VideoGenerator/        # Video service (submodule: visualizr)
│   ├── src/              # Source code
│   ├── models/           # AI model configurations
│   └── tests/            # Unit tests
├── VoiceGenerator/        # Voice service (submodule: vocalizr)
│   ├── src/              # Source code
│   ├── models/           # Voice model configurations
│   └── tests/            # Unit tests
├── docs/                 # Documentation
├── compose.yaml          # Docker Compose configuration
├── compose.dev.yaml      # Development overrides
└── README.md            # Project overview
```

### App Structure (Chattr)

```
App/
├── src/
│   ├── app.py           # Main Gradio application
│   ├── chat/            # Chat logic and handlers
│   ├── characters/      # Character definitions and management
│   ├── memory/          # Conversation memory and retrieval
│   ├── models/          # LLM integration
│   ├── media/           # Media generation coordination
│   ├── api/             # REST API endpoints
│   └── utils/           # Utility functions
├── tests/
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── fixtures/        # Test data and fixtures
├── config/              # Configuration files
└── assets/              # Static assets
```

## Development Workflow

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/new-character-type

# Make changes to submodules
cd App
git checkout -b feature/new-character-type
# ... make changes ...
git commit -m "Add new character type support"
git push origin feature/new-character-type

# Update main repository
cd ..
git add App
git commit -m "Update App submodule for new character type"
git push origin feature/new-character-type
```

### 2. Testing Changes

```bash
# Run unit tests
python -m pytest tests/unit/

# Run integration tests
python -m pytest tests/integration/

# Run with coverage
python -m pytest --cov=src tests/

# Test specific service
cd App && python -m pytest tests/
```

### 3. Code Quality Checks

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
flake8 src/ tests/
pylint src/

# Type checking
mypy src/

# Security scan
bandit -r src/
```

### 4. Docker Development

```bash
# Build development images
docker compose -f compose.dev.yaml build

# Run with development overrides
docker compose -f compose.yaml -f compose.dev.yaml up -d

# View logs
docker compose logs -f app

# Execute commands in container
docker compose exec app bash
```

## Code Standards

### Python Style Guide

We follow PEP 8 with some modifications:

```python
# File: src/example.py
"""Module docstring describing the purpose."""

import os
import sys
from typing import Dict, List, Optional

import requests
from fastapi import FastAPI

from .models import Character
from .utils import logger


class CharacterManager:
    """Manage character instances and configurations.
    
    Attributes:
        characters: Dictionary of available characters.
        default_character: Default character ID.
    """
    
    def __init__(self, config: Dict[str, str]) -> None:
        """Initialize character manager.
        
        Args:
            config: Configuration dictionary.
        """
        self.characters: Dict[str, Character] = {}
        self.default_character = config.get("default_character", "assistant")
        self._load_characters(config)
    
    def get_character(self, character_id: str) -> Optional[Character]:
        """Get character by ID.
        
        Args:
            character_id: Unique character identifier.
            
        Returns:
            Character instance or None if not found.
        """
        return self.characters.get(character_id)
    
    def _load_characters(self, config: Dict[str, str]) -> None:
        """Load characters from configuration."""
        # Implementation details...
        logger.info(f"Loaded {len(self.characters)} characters")
```

### Configuration Management

```python
# config/settings.py
from pydantic import BaseSettings, Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Model configuration
    model_api_key: str = Field(..., env="MODEL__API_KEY")
    model_url: str = Field(
        "https://api.groq.com/openai/v1", 
        env="MODEL__URL"
    )
    model_name: str = Field("llama3-70b-8192", env="MODEL__NAME")
    
    # Database configuration
    vector_db_url: str = Field(
        "http://vector_database:6333",
        env="VECTOR_DATABASE__URL"
    )
    
    # Optional settings
    debug: bool = Field(False, env="DEBUG")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
```

### Error Handling

```python
# utils/exceptions.py
class ChatacterError(Exception):
    """Base exception for Chatacter application."""
    pass


class ModelError(ChatacterError):
    """Exception for model-related errors."""
    
    def __init__(self, message: str, model_name: str = None):
        super().__init__(message)
        self.model_name = model_name


class GenerationError(ChatacterError):
    """Exception for media generation errors."""
    
    def __init__(self, message: str, generation_type: str = None):
        super().__init__(message)
        self.generation_type = generation_type


# Usage in application
try:
    response = model.generate(prompt)
except ModelError as e:
    logger.error(f"Model error: {e}")
    raise GenerationError(f"Failed to generate response: {e}")
```

### Logging Configuration

```python
# utils/logging.py
import logging
import sys
from typing import Optional

def setup_logging(
    level: str = "INFO",
    format_string: Optional[str] = None,
    include_timestamp: bool = True
) -> None:
    """Configure application logging.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR).
        format_string: Custom format string.
        include_timestamp: Whether to include timestamps.
    """
    if format_string is None:
        if include_timestamp:
            format_string = (
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        else:
            format_string = "%(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/app.log", mode="a")
        ]
    )

# Usage
logger = logging.getLogger(__name__)
```

## Testing

### Test Structure

```python
# tests/unit/test_character_manager.py
import pytest
from unittest.mock import Mock, patch

from src.characters.manager import CharacterManager
from src.models import Character


class TestCharacterManager:
    """Test suite for CharacterManager."""
    
    @pytest.fixture
    def manager(self):
        """Create character manager for testing."""
        config = {
            "default_character": "assistant",
            "characters": {
                "assistant": {
                    "name": "Assistant",
                    "personality": "helpful"
                }
            }
        }
        return CharacterManager(config)
    
    def test_get_character_exists(self, manager):
        """Test getting an existing character."""
        character = manager.get_character("assistant")
        assert character is not None
        assert character.name == "Assistant"
    
    def test_get_character_not_exists(self, manager):
        """Test getting a non-existent character."""
        character = manager.get_character("nonexistent")
        assert character is None
    
    @patch('src.characters.manager.logger')
    def test_load_characters_logging(self, mock_logger, manager):
        """Test that character loading is logged."""
        mock_logger.info.assert_called_once()
```

### Integration Tests

```python
# tests/integration/test_api.py
import pytest
import requests
from fastapi.testclient import TestClient

from src.app import app


class TestChatAPI:
    """Integration tests for chat API."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    def test_send_message(self, client):
        """Test sending a chat message."""
        response = client.post(
            "/api/v1/chat/message",
            json={
                "message": "Hello!",
                "character_id": "assistant",
                "session_id": "test_session"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["character_id"] == "assistant"
    
    def test_get_characters(self, client):
        """Test getting character list."""
        response = client.get("/api/v1/characters")
        assert response.status_code == 200
        data = response.json()
        assert "characters" in data
        assert len(data["characters"]) > 0
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/unit/test_character_manager.py

# Run with coverage
python -m pytest --cov=src --cov-report=html tests/

# Run tests with specific markers
python -m pytest -m "not slow" tests/

# Run tests in parallel
python -m pytest -n auto tests/
```

## Debugging

### Debug Configuration

```python
# debug/config.py
import os

DEBUG_CONFIG = {
    "enable_debug_toolbar": os.getenv("ENABLE_DEBUG_TOOLBAR", "false").lower() == "true",
    "log_sql_queries": os.getenv("LOG_SQL_QUERIES", "false").lower() == "true",
    "enable_profiling": os.getenv("ENABLE_PROFILING", "false").lower() == "true",
    "debug_media_generation": os.getenv("DEBUG_MEDIA_GENERATION", "false").lower() == "true"
}
```

### VS Code Debug Configuration

```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug Chattr App",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/App/src/app.py",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/App",
                "DEBUG": "true",
                "LOG_LEVEL": "DEBUG"
            },
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/App"
        },
        {
            "name": "Debug Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["tests/", "-v"],
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            },
            "console": "integratedTerminal"
        }
    ]
}
```

### Docker Debugging

```bash
# Debug container startup
docker compose up --no-detach app

# Access container shell
docker compose exec app bash

# View container logs
docker compose logs -f app

# Debug with specific environment
docker compose run --rm -e DEBUG=true app python src/app.py
```

## Performance Optimization

### Profiling

```python
# utils/profiling.py
import cProfile
import pstats
from functools import wraps
from typing import Callable

def profile_function(func: Callable) -> Callable:
    """Decorator to profile function execution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # Top 10 functions
        
        return result
    return wrapper

# Usage
@profile_function
def generate_response(prompt: str) -> str:
    # Function implementation
    pass
```

### Memory Monitoring

```python
# utils/monitoring.py
import psutil
import GPUtil
from typing import Dict

def get_system_metrics() -> Dict[str, float]:
    """Get current system resource usage."""
    # CPU and memory
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    # GPU metrics
    gpu_metrics = {}
    try:
        gpus = GPUtil.getGPUs()
        for i, gpu in enumerate(gpus):
            gpu_metrics[f"gpu_{i}_load"] = gpu.load * 100
            gpu_metrics[f"gpu_{i}_memory"] = gpu.memoryUtil * 100
    except Exception:
        pass
    
    return {
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "memory_available_gb": memory.available / (1024**3),
        **gpu_metrics
    }
```

### Optimization Guidelines

1. **Database Queries**
   - Use connection pooling
   - Implement query caching
   - Optimize vector search parameters

2. **Memory Management**
   - Implement model caching strategies
   - Use lazy loading for large assets
   - Monitor GPU memory usage

3. **API Performance**
   - Implement response caching
   - Use async/await for I/O operations
   - Add request rate limiting

4. **Media Generation**
   - Queue heavy operations
   - Implement progress tracking
   - Cache generated content

---

This development guide provides the foundation for contributing to the Chatacter Backend project. For specific contribution guidelines, see [Contributing](./contributing.md).