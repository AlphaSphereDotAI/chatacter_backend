# Visualizr API Reference

The Visualizr service provides AI-powered video generation capabilities for the Chatacter Backend system.

## Base URL

```
http://localhost:8002
```

## Table of Contents

- [Authentication](#authentication)
- [Video Generation](#video-generation)
- [Model Management](#model-management)
- [Asset Management](#asset-management)
- [Health & Status](#health--status)

## Authentication

The Visualizr API uses the same authentication mechanism as the main Chattr service.

### Headers

```http
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY
```

## Video Generation

### Generate Video from Text

Create a video based on text description.

```http
POST /api/v1/generate/video
```

**Request Body:**
```json
{
    "prompt": "A serene mountain landscape at sunset with golden light",
    "negative_prompt": "blurry, low quality, distorted",
    "width": 1024,
    "height": 1024,
    "num_frames": 24,
    "fps": 8,
    "num_inference_steps": 25,
    "guidance_scale": 7.5,
    "seed": 42,
    "model": "stable-video-diffusion",
    "style": "cinematic"
}
```

**Response:**
```json
{
    "request_id": "video_req_123",
    "status": "processing",
    "estimated_time_seconds": 30,
    "queue_position": 2,
    "created_at": "2024-01-15T10:30:00Z"
}
```

### Generate Video from Image

Create a video animation from a source image.

```http
POST /api/v1/generate/video/from-image
```

**Request Body (multipart/form-data):**
```
image: [image file]
motion_prompt: "gentle swaying in the wind"
duration_seconds: 3
fps: 24
motion_strength: 0.7
```

**Response:**
```json
{
    "request_id": "video_req_124",
    "status": "processing",
    "estimated_time_seconds": 25,
    "created_at": "2024-01-15T10:32:00Z"
}
```

### Generate Character Animation

Create character-specific animations and movements.

```http
POST /api/v1/generate/character-animation
```

**Request Body:**
```json
{
    "character_id": "assistant",
    "action": "greeting",
    "emotion": "happy",
    "background": "office",
    "duration_seconds": 5,
    "resolution": "1024x1024",
    "animation_style": "natural"
}
```

**Response:**
```json
{
    "request_id": "anim_req_125",
    "status": "processing",
    "character_id": "assistant",
    "estimated_time_seconds": 45,
    "created_at": "2024-01-15T10:35:00Z"
}
```

### Get Generation Status

Check the status of a video generation request.

```http
GET /api/v1/generate/status/{request_id}
```

**Response (Processing):**
```json
{
    "request_id": "video_req_123",
    "status": "processing",
    "progress": 65,
    "current_step": "frame_generation",
    "estimated_remaining_seconds": 12,
    "created_at": "2024-01-15T10:30:00Z",
    "started_at": "2024-01-15T10:30:05Z"
}
```

**Response (Completed):**
```json
{
    "request_id": "video_req_123",
    "status": "completed",
    "progress": 100,
    "result": {
        "video_url": "/assets/video/video_123.mp4",
        "thumbnail_url": "/assets/video/video_123_thumb.jpg",
        "preview_gif_url": "/assets/video/video_123_preview.gif",
        "metadata": {
            "duration_seconds": 3.0,
            "fps": 24,
            "resolution": "1024x1024",
            "file_size_bytes": 2048576,
            "format": "mp4",
            "codec": "h264"
        }
    },
    "created_at": "2024-01-15T10:30:00Z",
    "completed_at": "2024-01-15T10:30:35Z",
    "processing_time_seconds": 35
}
```

**Response (Failed):**
```json
{
    "request_id": "video_req_123",
    "status": "failed",
    "error": {
        "code": "GENERATION_FAILED",
        "message": "Video generation failed due to invalid prompt",
        "details": "The prompt contains unsupported content"
    },
    "created_at": "2024-01-15T10:30:00Z",
    "failed_at": "2024-01-15T10:30:15Z"
}
```

### Cancel Generation

Cancel a pending or processing video generation request.

```http
DELETE /api/v1/generate/{request_id}
```

**Response:**
```json
{
    "request_id": "video_req_123",
    "status": "cancelled",
    "cancelled_at": "2024-01-15T10:31:00Z",
    "message": "Generation request cancelled successfully"
}
```

## Model Management

### List Available Models

Get a list of available video generation models.

```http
GET /api/v1/models
```

**Response:**
```json
{
    "models": [
        {
            "id": "stable-video-diffusion",
            "name": "Stable Video Diffusion",
            "description": "High-quality text-to-video generation",
            "type": "text-to-video",
            "max_resolution": "1024x1024",
            "max_duration_seconds": 10,
            "supported_formats": ["mp4", "webm"],
            "gpu_memory_required_gb": 8,
            "average_generation_time_seconds": 30
        },
        {
            "id": "animatediff",
            "name": "AnimateDiff",
            "description": "Animation generation from static images",
            "type": "image-to-video",
            "max_resolution": "512x512",
            "max_duration_seconds": 5,
            "supported_formats": ["mp4", "gif"],
            "gpu_memory_required_gb": 6,
            "average_generation_time_seconds": 20
        }
    ]
}
```

### Get Model Details

Get detailed information about a specific model.

```http
GET /api/v1/models/{model_id}
```

**Response:**
```json
{
    "id": "stable-video-diffusion",
    "name": "Stable Video Diffusion",
    "description": "High-quality text-to-video generation with excellent motion quality",
    "version": "1.1",
    "type": "text-to-video",
    "capabilities": {
        "max_resolution": "1024x1024",
        "min_resolution": "256x256",
        "max_duration_seconds": 10,
        "min_duration_seconds": 1,
        "max_fps": 30,
        "min_fps": 8,
        "supported_formats": ["mp4", "webm", "avi"],
        "supports_negative_prompt": true,
        "supports_style_transfer": true
    },
    "requirements": {
        "gpu_memory_gb": 8,
        "vram_usage_gb": 6,
        "estimated_load_time_seconds": 15
    },
    "parameters": {
        "guidance_scale": {
            "min": 1.0,
            "max": 20.0,
            "default": 7.5,
            "description": "Controls adherence to prompt"
        },
        "num_inference_steps": {
            "min": 10,
            "max": 50,
            "default": 25,
            "description": "Number of denoising steps"
        }
    },
    "performance": {
        "average_generation_time_seconds": 30,
        "success_rate_percent": 95.2,
        "total_generations": 15420
    }
}
```

### Load Model

Preload a model into GPU memory for faster generation.

```http
POST /api/v1/models/{model_id}/load
```

**Response:**
```json
{
    "model_id": "stable-video-diffusion",
    "status": "loading",
    "estimated_load_time_seconds": 15,
    "started_at": "2024-01-15T10:40:00Z"
}
```

### Unload Model

Unload a model from GPU memory to free resources.

```http
POST /api/v1/models/{model_id}/unload
```

**Response:**
```json
{
    "model_id": "stable-video-diffusion",
    "status": "unloaded",
    "freed_memory_gb": 6.2,
    "unloaded_at": "2024-01-15T10:42:00Z"
}
```

## Asset Management

### List Generated Videos

Get a list of generated videos.

```http
GET /api/v1/assets/videos
```

**Query Parameters:**
- `limit`: Maximum number of results (default: 50, max: 100)
- `offset`: Pagination offset (default: 0)
- `model`: Filter by generation model
- `start_date`: Filter by creation date (ISO 8601)
- `end_date`: Filter by creation date (ISO 8601)

**Response:**
```json
{
    "videos": [
        {
            "id": "video_123",
            "url": "/assets/video/video_123.mp4",
            "thumbnail_url": "/assets/video/video_123_thumb.jpg",
            "prompt": "A serene mountain landscape at sunset",
            "model": "stable-video-diffusion",
            "metadata": {
                "duration_seconds": 3.0,
                "resolution": "1024x1024",
                "fps": 24,
                "file_size_bytes": 2048576
            },
            "created_at": "2024-01-15T10:30:35Z"
        }
    ],
    "total_count": 156,
    "has_more": true
}
```

### Get Video Details

Get detailed information about a specific video.

```http
GET /api/v1/assets/videos/{video_id}
```

**Response:**
```json
{
    "id": "video_123",
    "url": "/assets/video/video_123.mp4",
    "thumbnail_url": "/assets/video/video_123_thumb.jpg",
    "preview_gif_url": "/assets/video/video_123_preview.gif",
    "prompt": "A serene mountain landscape at sunset with golden light",
    "negative_prompt": "blurry, low quality",
    "model": "stable-video-diffusion",
    "parameters": {
        "width": 1024,
        "height": 1024,
        "num_frames": 24,
        "fps": 8,
        "guidance_scale": 7.5,
        "num_inference_steps": 25,
        "seed": 42
    },
    "metadata": {
        "duration_seconds": 3.0,
        "resolution": "1024x1024",
        "fps": 24,
        "file_size_bytes": 2048576,
        "format": "mp4",
        "codec": "h264",
        "bitrate_kbps": 5461
    },
    "generation_info": {
        "request_id": "video_req_123",
        "processing_time_seconds": 35,
        "gpu_memory_used_gb": 6.2
    },
    "created_at": "2024-01-15T10:30:35Z"
}
```

### Delete Video

Delete a generated video and its associated files.

```http
DELETE /api/v1/assets/videos/{video_id}
```

**Response:**
```json
{
    "video_id": "video_123",
    "status": "deleted",
    "freed_space_bytes": 2048576,
    "deleted_at": "2024-01-15T10:50:00Z"
}
```

## Health & Status

### Health Check

Check service health and GPU status.

```http
GET /api/v1/health
```

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:50:00Z",
    "version": "1.0.0",
    "uptime_seconds": 3600,
    "gpu_info": {
        "available": true,
        "count": 1,
        "devices": [
            {
                "id": 0,
                "name": "NVIDIA GeForce RTX 4090",
                "memory_total_gb": 24.0,
                "memory_used_gb": 6.2,
                "memory_free_gb": 17.8,
                "utilization_percent": 75,
                "temperature_celsius": 65
            }
        ]
    },
    "loaded_models": [
        {
            "id": "stable-video-diffusion",
            "memory_usage_gb": 6.2,
            "loaded_at": "2024-01-15T10:00:00Z"
        }
    ],
    "queue_status": {
        "pending_requests": 2,
        "processing_requests": 1,
        "completed_today": 156
    }
}
```

### System Metrics

Get detailed performance metrics.

```http
GET /api/v1/metrics
```

**Response:**
```json
{
    "requests": {
        "total": 1542,
        "today": 156,
        "per_hour": 15.6,
        "success_rate_percent": 95.2
    },
    "generation": {
        "average_time_seconds": 32.5,
        "median_time_seconds": 28.0,
        "fastest_time_seconds": 12.3,
        "slowest_time_seconds": 120.4
    },
    "queue": {
        "current_length": 3,
        "max_length_today": 15,
        "average_wait_time_seconds": 45.2
    },
    "storage": {
        "total_videos": 1542,
        "total_size_gb": 48.6,
        "available_space_gb": 451.4
    },
    "models": {
        "stable-video-diffusion": {
            "generations": 1234,
            "success_rate": 96.1,
            "average_time_seconds": 30.2
        },
        "animatediff": {
            "generations": 308,
            "success_rate": 92.5,
            "average_time_seconds": 18.7
        }
    }
}
```

## WebSocket API

### Real-time Generation Updates

Monitor video generation progress in real-time.

```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8002/api/v1/ws/generation');

// Subscribe to updates for a specific request
ws.send(JSON.stringify({
    type: 'subscribe',
    request_id: 'video_req_123'
}));

// Receive progress updates
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Progress:', data.progress, '%');
};
```

### WebSocket Message Types

#### Subscribe to Updates
```json
{
    "type": "subscribe",
    "request_id": "video_req_123"
}
```

#### Progress Update
```json
{
    "type": "progress",
    "request_id": "video_req_123",
    "status": "processing",
    "progress": 65,
    "current_step": "frame_generation",
    "estimated_remaining_seconds": 12
}
```

#### Completion Notification
```json
{
    "type": "completed",
    "request_id": "video_req_123",
    "result": {
        "video_url": "/assets/video/video_123.mp4",
        "thumbnail_url": "/assets/video/video_123_thumb.jpg"
    }
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_PROMPT` | 400 | Text prompt is invalid or empty |
| `INVALID_PARAMETERS` | 400 | Generation parameters are invalid |
| `MODEL_NOT_FOUND` | 404 | Requested model is not available |
| `REQUEST_NOT_FOUND` | 404 | Generation request not found |
| `INSUFFICIENT_GPU_MEMORY` | 507 | Not enough GPU memory available |
| `MODEL_LOAD_FAILED` | 500 | Failed to load generation model |
| `GENERATION_FAILED` | 500 | Video generation process failed |
| `QUEUE_FULL` | 503 | Generation queue is at capacity |

## SDK Example

### Python SDK

```python
import requests
import time

class VisualizrClient:
    def __init__(self, base_url="http://localhost:8002", api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}" if api_key else None
        }
    
    def generate_video(self, prompt, **kwargs):
        """Generate video from text prompt"""
        data = {"prompt": prompt, **kwargs}
        response = requests.post(
            f"{self.base_url}/api/v1/generate/video",
            headers=self.headers,
            json=data
        )
        return response.json()
    
    def get_status(self, request_id):
        """Get generation status"""
        response = requests.get(
            f"{self.base_url}/api/v1/generate/status/{request_id}",
            headers=self.headers
        )
        return response.json()
    
    def wait_for_completion(self, request_id, timeout=300):
        """Wait for generation to complete"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            status = self.get_status(request_id)
            if status["status"] == "completed":
                return status
            elif status["status"] == "failed":
                raise Exception(f"Generation failed: {status['error']['message']}")
            time.sleep(2)
        raise TimeoutError("Generation timed out")

# Usage
client = VisualizrClient(api_key="your-api-key")
result = client.generate_video("A beautiful sunset over mountains")
final_result = client.wait_for_completion(result["request_id"])
print(f"Video URL: {final_result['result']['video_url']}")
```

---

For more examples and advanced usage, see the [Development Guide](../development.md).