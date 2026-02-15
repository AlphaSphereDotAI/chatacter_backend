# Chattr App API Reference

The Chattr service provides the main chat interface and orchestration layer for the Chatacter Backend system.

## Base URL

```
http://localhost:8000
```

## Table of Contents

- [Authentication](#authentication)
- [Chat Endpoints](#chat-endpoints)
- [Character Management](#character-management)
- [Media Generation](#media-generation)
- [Health & Status](#health--status)
- [WebSocket API](#websocket-api)

## Authentication

The Chattr API uses API key authentication for programmatic access.

### Headers

```http
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY
```

## Chat Endpoints

### Send Message

Send a message to a character and receive a response.

```http
POST /api/v1/chat/message
```

**Request Body:**
```json
{
    "message": "Hello, how are you today?",
    "character_id": "assistant",
    "session_id": "user-session-123",
    "context": {
        "user_name": "Alice",
        "conversation_history": true
    }
}
```

**Response:**
```json
{
    "response": "Hello Alice! I'm doing well, thank you for asking. How can I help you today?",
    "character_id": "assistant",
    "session_id": "user-session-123",
    "timestamp": "2024-01-15T10:30:00Z",
    "media": {
        "audio_url": "/assets/audio/response_123.wav",
        "video_url": "/assets/video/response_123.mp4"
    },
    "metadata": {
        "tokens_used": 45,
        "response_time_ms": 1200,
        "confidence": 0.95
    }
}
```

### Get Conversation History

Retrieve conversation history for a session.

```http
GET /api/v1/chat/history/{session_id}
```

**Query Parameters:**
- `limit` (optional): Maximum number of messages (default: 50)
- `offset` (optional): Pagination offset (default: 0)

**Response:**
```json
{
    "session_id": "user-session-123",
    "messages": [
        {
            "id": "msg_001",
            "timestamp": "2024-01-15T10:30:00Z",
            "role": "user",
            "content": "Hello, how are you today?",
            "character_id": "assistant"
        },
        {
            "id": "msg_002",
            "timestamp": "2024-01-15T10:30:01Z",
            "role": "assistant",
            "content": "Hello! I'm doing well...",
            "media": {
                "audio_url": "/assets/audio/response_123.wav"
            }
        }
    ],
    "total_count": 24,
    "has_more": true
}
```

### Clear Conversation

Clear conversation history for a session.

```http
DELETE /api/v1/chat/history/{session_id}
```

**Response:**
```json
{
    "message": "Conversation history cleared successfully",
    "session_id": "user-session-123",
    "cleared_at": "2024-01-15T10:35:00Z"
}
```

## Character Management

### List Available Characters

Get a list of all available characters.

```http
GET /api/v1/characters
```

**Response:**
```json
{
    "characters": [
        {
            "id": "assistant",
            "name": "Assistant",
            "description": "A helpful and friendly AI assistant",
            "personality": "Professional, helpful, and knowledgeable",
            "avatar_url": "/assets/avatars/assistant.png",
            "voice_model": "default",
            "capabilities": ["text", "voice", "video"]
        },
        {
            "id": "creative",
            "name": "Creative Writer",
            "description": "An imaginative AI focused on creative tasks",
            "personality": "Creative, artistic, and inspiring",
            "avatar_url": "/assets/avatars/creative.png",
            "voice_model": "expressive",
            "capabilities": ["text", "voice"]
        }
    ]
}
```

### Get Character Details

Get detailed information about a specific character.

```http
GET /api/v1/characters/{character_id}
```

**Response:**
```json
{
    "id": "assistant",
    "name": "Assistant",
    "description": "A helpful and friendly AI assistant",
    "personality": "Professional, helpful, and knowledgeable",
    "avatar_url": "/assets/avatars/assistant.png",
    "voice_model": "default",
    "video_model": "stable-video",
    "capabilities": ["text", "voice", "video"],
    "configuration": {
        "temperature": 0.7,
        "max_tokens": 4096,
        "system_prompt": "You are a helpful assistant..."
    },
    "statistics": {
        "total_conversations": 1542,
        "average_rating": 4.8,
        "last_updated": "2024-01-15T09:00:00Z"
    }
}
```

### Update Character Configuration

Update character settings and personality.

```http
PUT /api/v1/characters/{character_id}
```

**Request Body:**
```json
{
    "name": "Updated Assistant",
    "description": "An enhanced AI assistant",
    "personality": "More casual and friendly",
    "configuration": {
        "temperature": 0.8,
        "max_tokens": 2048
    }
}
```

## Media Generation

### Generate Voice

Generate voice audio for text.

```http
POST /api/v1/media/voice
```

**Request Body:**
```json
{
    "text": "Hello, this will be converted to speech",
    "character_id": "assistant",
    "voice_settings": {
        "speed": 1.0,
        "pitch": 1.0,
        "emotion": "neutral"
    }
}
```

**Response:**
```json
{
    "audio_url": "/assets/audio/voice_456.wav",
    "duration_seconds": 3.2,
    "file_size_bytes": 51200,
    "format": "wav",
    "generated_at": "2024-01-15T10:40:00Z"
}
```

### Generate Video

Generate video content for text.

```http
POST /api/v1/media/video
```

**Request Body:**
```json
{
    "text": "A serene landscape with mountains",
    "character_id": "assistant",
    "video_settings": {
        "width": 1024,
        "height": 1024,
        "duration_seconds": 5,
        "style": "realistic"
    }
}
```

**Response:**
```json
{
    "video_url": "/assets/video/video_789.mp4",
    "thumbnail_url": "/assets/video/video_789_thumb.jpg",
    "duration_seconds": 5.0,
    "resolution": "1024x1024",
    "file_size_bytes": 2048000,
    "generated_at": "2024-01-15T10:45:00Z"
}
```

### Get Media Status

Check the status of media generation requests.

```http
GET /api/v1/media/status/{request_id}
```

**Response:**
```json
{
    "request_id": "media_req_123",
    "status": "completed",
    "progress": 100,
    "media_type": "video",
    "result": {
        "video_url": "/assets/video/video_789.mp4",
        "duration_seconds": 5.0
    },
    "created_at": "2024-01-15T10:40:00Z",
    "completed_at": "2024-01-15T10:45:00Z"
}
```

## Health & Status

### Health Check

Check service health and status.

```http
GET /api/v1/health
```

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:50:00Z",
    "version": "1.0.0",
    "uptime_seconds": 86400,
    "services": {
        "llm_api": "healthy",
        "vector_database": "healthy",
        "voice_generator": "healthy",
        "video_generator": "healthy",
        "redis": "healthy"
    },
    "resource_usage": {
        "cpu_percent": 45.2,
        "memory_percent": 62.1,
        "gpu_memory_percent": 78.5
    }
}
```

### System Metrics

Get detailed system metrics.

```http
GET /api/v1/metrics
```

**Response:**
```json
{
    "requests_total": 15420,
    "requests_per_minute": 24.5,
    "average_response_time_ms": 1200,
    "error_rate_percent": 0.05,
    "active_sessions": 142,
    "characters": {
        "assistant": {
            "conversations_today": 842,
            "average_rating": 4.8
        }
    },
    "media_generation": {
        "voice_requests_today": 324,
        "video_requests_today": 156,
        "average_generation_time_seconds": 8.5
    }
}
```

## WebSocket API

### Connect to Chat Stream

Real-time chat communication via WebSocket.

```javascript
// Connection
const ws = new WebSocket('ws://localhost:8000/api/v1/ws/chat');

// Authentication
ws.send(JSON.stringify({
    type: 'auth',
    token: 'your-api-key',
    session_id: 'user-session-123'
}));

// Send message
ws.send(JSON.stringify({
    type: 'message',
    character_id: 'assistant',
    content: 'Hello there!'
}));

// Receive response
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};
```

### WebSocket Message Types

#### Authentication
```json
{
    "type": "auth",
    "token": "your-api-key",
    "session_id": "user-session-123"
}
```

#### Send Message
```json
{
    "type": "message",
    "character_id": "assistant",
    "content": "Hello there!",
    "metadata": {
        "user_name": "Alice"
    }
}
```

#### Receive Response
```json
{
    "type": "response",
    "character_id": "assistant",
    "content": "Hello Alice! How can I help you?",
    "timestamp": "2024-01-15T10:30:00Z",
    "media": {
        "audio_url": "/assets/audio/response_123.wav"
    }
}
```

#### Typing Indicator
```json
{
    "type": "typing",
    "character_id": "assistant",
    "is_typing": true
}
```

#### Error Messages
```json
{
    "type": "error",
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retry_after_seconds": 60
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Request body is invalid |
| `UNAUTHORIZED` | 401 | API key is missing or invalid |
| `FORBIDDEN` | 403 | Access denied for this resource |
| `NOT_FOUND` | 404 | Requested resource not found |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Internal server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

## SDK Examples

### Python SDK

```python
import requests
import websocket
import json

class ChatacterClient:
    def __init__(self, base_url="http://localhost:8000", api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}" if api_key else None
        }
    
    def send_message(self, message, character_id="assistant", session_id=None):
        response = requests.post(
            f"{self.base_url}/api/v1/chat/message",
            headers=self.headers,
            json={
                "message": message,
                "character_id": character_id,
                "session_id": session_id
            }
        )
        return response.json()
    
    def get_characters(self):
        response = requests.get(
            f"{self.base_url}/api/v1/characters",
            headers=self.headers
        )
        return response.json()

# Usage
client = ChatacterClient(api_key="your-api-key")
response = client.send_message("Hello!", session_id="my-session")
print(response["response"])
```

### JavaScript SDK

```javascript
class ChatacterClient {
    constructor(baseUrl = 'http://localhost:8000', apiKey = null) {
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
    }
    
    async sendMessage(message, characterId = 'assistant', sessionId = null) {
        const response = await fetch(`${this.baseUrl}/api/v1/chat/message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`
            },
            body: JSON.stringify({
                message: message,
                character_id: characterId,
                session_id: sessionId
            })
        });
        return response.json();
    }
    
    async getCharacters() {
        const response = await fetch(`${this.baseUrl}/api/v1/characters`, {
            headers: {
                'Authorization': `Bearer ${this.apiKey}`
            }
        });
        return response.json();
    }
}

// Usage
const client = new ChatacterClient('http://localhost:8000', 'your-api-key');
const response = await client.sendMessage('Hello!', 'assistant', 'my-session');
console.log(response.response);
```

---

For more examples and advanced usage, see the [Development Guide](../development.md).