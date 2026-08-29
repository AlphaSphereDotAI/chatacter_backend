# Contributing to Chatacter Backend

Thank you for your interest in contributing to the Chatacter Backend project! This guide will help you get started with contributing code, documentation, or other improvements.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Contribution Types](#contribution-types)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Community](#community)

## Code of Conduct

This project adheres to a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- **Be respectful** and inclusive in all interactions
- **Be constructive** in feedback and discussions
- **Focus on the project** and avoid personal attacks
- **Help others** learn and grow

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone --recurse-submodules https://github.com/your-username/chatacter_backend.git
cd chatacter_backend

# Add upstream remote
git remote add upstream https://github.com/AlphaSphereDotAI/chatacter_backend.git
```

### 2. Set Up Development Environment

Follow the [Development Guide](./development.md) to set up your local development environment:

```bash
# Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install

# Start development services
docker compose -f compose.yaml -f compose.dev.yaml up -d
```

### 3. Verify Setup

```bash
# Run tests to ensure everything works
python -m pytest tests/

# Check code quality
black --check src/
flake8 src/
mypy src/
```

## Development Workflow

### 1. Create Feature Branch

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- **Follow coding standards** outlined in the [Development Guide](./development.md)
- **Write tests** for new functionality
- **Update documentation** as needed
- **Commit regularly** with clear messages

### 3. Test Your Changes

```bash
# Run unit tests
python -m pytest tests/unit/

# Run integration tests
python -m pytest tests/integration/

# Check code coverage
python -m pytest --cov=src tests/

# Lint and format
black src/ tests/
isort src/ tests/
flake8 src/ tests/
```

### 4. Submodule Changes

If you're modifying submodules (App, VideoGenerator, VoiceGenerator):

```bash
# Work in the submodule
cd App
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Add new feature"
git push origin feature/your-feature-name

# Update main repository
cd ..
git add App
git commit -m "Update App submodule for new feature"
```

## Contribution Types

### 🐛 Bug Fixes

- **Search existing issues** before creating new ones
- **Provide reproduction steps** with minimal examples
- **Include system information** (OS, Docker version, etc.)
- **Test the fix** thoroughly

### ✨ New Features

- **Discuss in an issue** before starting large features
- **Follow the architecture** patterns established in the codebase
- **Add comprehensive tests** and documentation
- **Consider backward compatibility**

### 📚 Documentation

- **Use clear, concise language**
- **Include practical examples**
- **Test all code examples**
- **Keep formatting consistent**

### 🔧 Infrastructure

- **Docker and deployment** improvements
- **CI/CD pipeline** enhancements
- **Monitoring and logging** additions
- **Performance optimizations**

### 🧪 Testing

- **Unit tests** for individual components
- **Integration tests** for service interactions
- **Performance tests** for critical paths
- **Documentation tests** for code examples

## Pull Request Process

### 1. Pre-PR Checklist

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (if applicable)
- [ ] Commit messages are clear and descriptive

### 2. Create Pull Request

```bash
# Push your changes
git push origin feature/your-feature-name

# Create PR on GitHub with:
# - Clear title and description
# - Reference to related issues
# - Testing instructions
# - Screenshots (for UI changes)
```

### 3. PR Template

When creating a PR, use this template:

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings or errors

## Related Issues
Fixes #(issue number)
```

### 4. Review Process

- **Automated checks** must pass (CI/CD, tests, linting)
- **Code review** by at least one maintainer
- **Address feedback** promptly and thoroughly
- **Rebase and squash** commits if requested

### 5. Merge Requirements

- ✅ All CI checks pass
- ✅ Code review approved
- ✅ Documentation updated
- ✅ No merge conflicts
- ✅ Tests maintain >80% coverage

## Issue Guidelines

### Creating Issues

#### Bug Reports

```markdown
**Bug Description**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g. Ubuntu 22.04]
 - Docker Version: [e.g. 20.10.21]
 - Python Version: [e.g. 3.10.12]
 - GPU: [e.g. RTX 4090]

**Additional Context**
Any other context about the problem.

**Logs**
```
Include relevant logs here
```
```

#### Feature Requests

```markdown
**Feature Description**
A clear description of what you want to happen.

**Problem Statement**
What problem does this solve?

**Proposed Solution**
Describe the solution you'd like.

**Alternatives Considered**
Describe alternatives you've considered.

**Additional Context**
Any other context or screenshots.
```

### Issue Labels

- **`bug`** - Something isn't working
- **`enhancement`** - New feature or request
- **`documentation`** - Improvements to documentation
- **`help wanted`** - Extra attention needed
- **`good first issue`** - Good for newcomers
- **`priority: high`** - High priority
- **`priority: low`** - Low priority
- **`status: in progress`** - Currently being worked on
- **`status: blocked`** - Blocked by other issues

## Code Style Guide

### Python Style

- **Follow PEP 8** with 88-character line limit (Black default)
- **Use type hints** for all function signatures
- **Write docstrings** for all public functions and classes
- **Import order**: standard library, third-party, local imports

```python
from typing import Dict, List, Optional

import requests
from fastapi import FastAPI

from .models import Character
from .utils import logger


def create_character(
    name: str, 
    personality: str, 
    config: Optional[Dict[str, str]] = None
) -> Character:
    """Create a new character instance.
    
    Args:
        name: Character name.
        personality: Character personality description.
        config: Optional configuration dictionary.
        
    Returns:
        Character instance.
        
    Raises:
        ValueError: If name is empty or invalid.
    """
    if not name or not name.strip():
        raise ValueError("Character name cannot be empty")
    
    return Character(
        name=name.strip(),
        personality=personality,
        config=config or {}
    )
```

### Commit Message Format

```
type(scope): subject

body

footer
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(api): add character voice customization endpoint

Add new endpoint to allow users to customize character voices
with pitch, speed, and emotion parameters.

Closes #123
```

```
fix(video): resolve GPU memory leak in generation pipeline

The video generation pipeline was not properly releasing GPU memory
after each generation, causing out-of-memory errors after multiple
requests.

Fixes #456
```

## Development Environment

### Required Tools

- **Python 3.10+**
- **Docker & Docker Compose**
- **Git** with submodule support
- **Pre-commit** for git hooks
- **pytest** for testing
- **black** for code formatting
- **flake8** for linting
- **mypy** for type checking

### IDE Setup

#### VS Code

Recommended extensions:
- Python
- Docker
- GitLens
- Prettier
- Thunder Client (for API testing)

```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

#### PyCharm

1. Open project directory
2. Configure Python interpreter (virtual environment)
3. Enable Black formatter
4. Configure flake8 and mypy inspections
5. Set up Docker Compose run configurations

### Testing Guidelines

#### Unit Tests

```python
# tests/unit/test_character_manager.py
import pytest
from unittest.mock import Mock, patch

from src.characters.manager import CharacterManager


class TestCharacterManager:
    """Unit tests for CharacterManager."""
    
    @pytest.fixture
    def manager(self):
        """Create character manager for testing."""
        return CharacterManager(config={"default": "assistant"})
    
    def test_character_creation(self, manager):
        """Test character creation."""
        character = manager.create_character("Test", "Friendly")
        assert character.name == "Test"
        assert character.personality == "Friendly"
    
    @patch('src.characters.manager.logger')
    def test_logging(self, mock_logger, manager):
        """Test that operations are logged."""
        manager.create_character("Test", "Friendly")
        mock_logger.info.assert_called()
```

#### Integration Tests

```python
# tests/integration/test_api_integration.py
import pytest
from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_chat_flow(client):
    """Test complete chat flow."""
    # Send message
    response = client.post(
        "/api/v1/chat/message",
        json={"message": "Hello", "character_id": "assistant"}
    )
    assert response.status_code == 200
    
    # Verify response structure
    data = response.json()
    assert "response" in data
    assert "session_id" in data
```

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community chat
- **Pull Requests**: Code review and collaboration

### Getting Help

1. **Check documentation** first
2. **Search existing issues** for similar problems
3. **Create detailed issue** with reproduction steps
4. **Be patient and respectful** in all interactions

### Recognition

Contributors are recognized in:
- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributor graphs**

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to Chatacter Backend! 🚀