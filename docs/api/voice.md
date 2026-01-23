# Vocalizr API Reference

The Vocalizr service provides AI-powered voice synthesis and audio generation capabilities for the Chatacter Backend system.

## Base URL

```
http://localhost:8001
```

## Table of Contents

- [Authentication](#authentication)
- [Voice Generation](#voice-generation)
- [Voice Models](#voice-models)
- [Audio Processing](#audio-processing)
- [Asset Management](#asset-management)
- [Health & Status](#health--status)

## Authentication

The Vocalizr API uses the same authentication mechanism as the main Chattr service.

### Headers

```http
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY
```

## Voice Generation

### Generate Speech from Text

Convert text to speech using various voice models.

```http
POST /api/v1/generate/speech
```

**Request Body:**
```json
{
    "text": "Hello, this is a test of the voice generation system!",
    "voice_model": "default",
    "language": "en",
    "speaker_id": "female_1",
    "settings": {
        "speed": 1.0,
        "pitch": 1.0,
        "volume": 1.0,
        "emotion": "neutral",
        "style": "conversational"
    },
    "output_format": "wav",
    "sample_rate": 22050
}
```

**Response:**
```json
{
    "request_id": "voice_req_123",
    "status": "processing",
    "estimated_time_seconds": 5,
    "created_at": "2024-01-15T10:30:00Z"
}
```

### Generate Character Voice

Generate speech with character-specific voice settings.

```http
POST /api/v1/generate/character-voice
```

**Request Body:**
```json
{
    "text": "Hello there! How can I assist you today?",
    "character_id": "assistant",
    "emotion": "friendly",
    "context": "greeting",
    "enable_effects": true,
    "output_format": "mp3"
}
```

**Response:**
```json
{
    "request_id": "char_voice_124",
    "status": "processing",
    "character_id": "assistant",
    "estimated_time_seconds": 3,
    "created_at": "2024-01-15T10:32:00Z"
}
```

### Clone Voice from Sample

Create a voice clone from audio samples.

```http
POST /api/v1/generate/voice-clone
```

**Request Body (multipart/form-data):**
```
audio_samples: [audio files]
voice_name: "custom_voice_1"
description: "Professional male voice"
target_language: "en"
quality: "high"
```

**Response:**
```json
{
    "request_id": "clone_req_125",
    "status": "processing",
    "voice_name": "custom_voice_1",
    "estimated_time_seconds": 120,
    "created_at": "2024-01-15T10:35:00Z"
}
```

### Get Generation Status

Check the status of a voice generation request.

```http
GET /api/v1/generate/status/{request_id}
```

**Response (Processing):**
```json
{
    "request_id": "voice_req_123",
    "status": "processing",
    "progress": 75,
    "current_step": "audio_synthesis",
    "estimated_remaining_seconds": 2,
    "created_at": "2024-01-15T10:30:00Z",
    "started_at": "2024-01-15T10:30:02Z"
}
```

**Response (Completed):**
```json
{
    "request_id": "voice_req_123",
    "status": "completed",
    "progress": 100,
    "result": {
        "audio_url": "/assets/audio/voice_123.wav",
        "waveform_url": "/assets/audio/voice_123_waveform.png",
        "metadata": {
            "duration_seconds": 4.2,
            "sample_rate": 22050,
            "channels": 1,
            "format": "wav",
            "file_size_bytes": 185472,
            "bitrate_kbps": 352
        },
        "voice_analysis": {
            "pitch_hz": 180.5,
            "speaking_rate_wpm": 165,
            "energy_level": 0.7,
            "emotion_detected": "neutral"
        }
    },
    "created_at": "2024-01-15T10:30:00Z",
    "completed_at": "2024-01-15T10:30:05Z",
    "processing_time_seconds": 5
}
```

**Response (Failed):**
```json
{
    "request_id": "voice_req_123",
    "status": "failed",
    "error": {
        "code": "TEXT_TOO_LONG",
        "message": "Text exceeds maximum length limit",
        "details": "Maximum 1000 characters allowed"
    },
    "created_at": "2024-01-15T10:30:00Z",
    "failed_at": "2024-01-15T10:30:03Z"
}
```

### Stream Speech Generation

Generate speech with real-time streaming.

```http
POST /api/v1/generate/speech/stream
```

**Request Body:**
```json
{
    "text": "This is streaming text-to-speech generation.",
    "voice_model": "default",
    "chunk_size": 1024,
    "format": "wav"
}
```

**Response:** Audio stream (chunked transfer encoding)

## Voice Models

### List Available Voice Models

Get a list of available voice synthesis models.

```http
GET /api/v1/models
```

**Response:**
```json
{
    "models": [
        {
            "id": "coqui-tts",
            "name": "Coqui TTS",
            "description": "High-quality neural text-to-speech",
            "type": "neural_tts",
            "languages": ["en", "es", "fr", "de", "it"],
            "speakers": [
                {
                    "id": "female_1",
                    "name": "Sarah",
                    "gender": "female",
                    "age_range": "adult",
                    "accent": "american"
                },
                {
                    "id": "male_1",
                    "name": "James",
                    "gender": "male",
                    "age_range": "adult",
                    "accent": "british"
                }
            ],
            "supported_emotions": ["neutral", "happy", "sad", "angry", "excited"],
            "max_text_length": 1000,
            "average_generation_time_seconds": 3.5
        },
        {
            "id": "bark",
            "name": "Bark",
            "description": "Expressive multilingual voice synthesis",
            "type": "generative_tts",
            "languages": ["en", "zh", "fr", "de", "hi", "it", "ja", "ko", "pl", "pt", "ru", "es", "tr"],
            "features": ["emotional_expression", "background_noise", "music_generation"],
            "max_text_length": 500,
            "average_generation_time_seconds": 8.2
        }
    ]
}
```

### Get Model Details

Get detailed information about a specific voice model.

```http
GET /api/v1/models/{model_id}
```

**Response:**
```json
{
    "id": "coqui-tts",
    "name": "Coqui TTS",
    "description": "High-quality neural text-to-speech with natural prosody",
    "version": "1.0.2",
    "type": "neural_tts",
    "capabilities": {
        "languages": ["en", "es", "fr", "de", "it"],
        "max_text_length": 1000,
        "min_text_length": 1,
        "supported_formats": ["wav", "mp3", "flac"],
        "sample_rates": [16000, 22050, 44100],
        "supports_ssml": true,
        "supports_emotions": true,
        "supports_speed_control": true,
        "supports_pitch_control": true
    },
    "speakers": [
        {
            "id": "female_1",
            "name": "Sarah",
            "gender": "female",
            "age_range": "adult",
            "accent": "american",
            "description": "Professional, clear female voice",
            "sample_url": "/assets/samples/female_1_sample.wav"
        }
    ],
    "parameters": {
        "speed": {
            "min": 0.5,
            "max": 2.0,
            "default": 1.0,
            "description": "Speech rate multiplier"
        },
        "pitch": {
            "min": 0.5,
            "max": 2.0,
            "default": 1.0,
            "description": "Pitch adjustment factor"
        }
    },
    "performance": {
        "average_generation_time_seconds": 3.5,
        "real_time_factor": 0.8,
        "quality_score": 4.7,
        "total_generations": 5420
    },
    "requirements": {
        "gpu_memory_gb": 2,
        "cpu_cores": 2,
        "ram_gb": 4
    }
}
```

### Load Voice Model

Preload a voice model for faster generation.

```http
POST /api/v1/models/{model_id}/load
```

**Request Body:**
```json
{
    "language": "en",
    "speaker_id": "female_1"
}
```

**Response:**
```json
{
    "model_id": "coqui-tts",
    "language": "en",
    "speaker_id": "female_1",
    "status": "loading",
    "estimated_load_time_seconds": 8,
    "started_at": "2024-01-15T10:40:00Z"
}
```

### List Loaded Models

Get currently loaded voice models.

```http
GET /api/v1/models/loaded
```

**Response:**
```json
{
    "loaded_models": [
        {
            "model_id": "coqui-tts",
            "language": "en",
            "speaker_id": "female_1",
            "loaded_at": "2024-01-15T10:40:08Z",
            "memory_usage_mb": 512,
            "last_used_at": "2024-01-15T10:45:00Z"
        }
    ],
    "total_memory_usage_mb": 512,
    "available_memory_mb": 3584
}
```

## Audio Processing

### Apply Audio Effects

Apply post-processing effects to generated audio.

```http
POST /api/v1/audio/effects
```

**Request Body (multipart/form-data):**
```
audio_file: [audio file]
effects: {
    "normalize": true,
    "noise_reduction": 0.5,
    "reverb": {
        "room_size": 0.3,
        "damping": 0.5
    },
    "equalizer": {
        "low": 1.0,
        "mid": 1.2,
        "high": 0.8
    }
}
```

**Response:**
```json
{
    "request_id": "effects_req_126",
    "status": "processing",
    "estimated_time_seconds": 3,
    "created_at": "2024-01-15T10:50:00Z"
}
```

### Convert Audio Format

Convert audio between different formats.

```http
POST /api/v1/audio/convert
```

**Request Body (multipart/form-data):**
```
audio_file: [audio file]
target_format: "mp3"
target_sample_rate: 44100
target_bitrate: 192
mono: false
```

**Response:**
```json
{
    "request_id": "convert_req_127",
    "status": "processing",
    "target_format": "mp3",
    "estimated_time_seconds": 2,
    "created_at": "2024-01-15T10:52:00Z"
}
```

### Analyze Audio

Analyze audio characteristics and quality.

```http
POST /api/v1/audio/analyze
```

**Request Body (multipart/form-data):**
```
audio_file: [audio file]
analysis_type: "full"
```

**Response:**
```json
{
    "file_info": {
        "format": "wav",
        "duration_seconds": 4.2,
        "sample_rate": 22050,
        "channels": 1,
        "file_size_bytes": 185472
    },
    "audio_analysis": {
        "fundamental_frequency_hz": 180.5,
        "pitch_range": {
            "min_hz": 120.3,
            "max_hz": 245.7
        },
        "speaking_rate_wpm": 165,
        "pause_ratio": 0.12,
        "energy_statistics": {
            "mean": 0.7,
            "max": 0.95,
            "std": 0.18
        },
        "spectral_features": {
            "spectral_centroid_hz": 2150.8,
            "spectral_rolloff_hz": 4820.3,
            "zero_crossing_rate": 0.065
        }
    },
    "quality_metrics": {
        "snr_db": 28.5,
        "thd_percent": 0.8,
        "clarity_score": 4.6,
        "naturalness_score": 4.3
    }
}
```

## Asset Management

### List Generated Audio

Get a list of generated audio files.

```http
GET /api/v1/assets/audio
```

**Query Parameters:**
- `limit`: Maximum number of results (default: 50, max: 100)
- `offset`: Pagination offset (default: 0)
- `model`: Filter by voice model
- `speaker`: Filter by speaker ID
- `start_date`: Filter by creation date (ISO 8601)
- `end_date`: Filter by creation date (ISO 8601)

**Response:**
```json
{
    "audio_files": [
        {
            "id": "audio_123",
            "url": "/assets/audio/voice_123.wav",
            "waveform_url": "/assets/audio/voice_123_waveform.png",
            "text": "Hello, this is a test of the voice generation system!",
            "voice_model": "coqui-tts",
            "speaker_id": "female_1",
            "metadata": {
                "duration_seconds": 4.2,
                "sample_rate": 22050,
                "file_size_bytes": 185472,
                "format": "wav"
            },
            "created_at": "2024-01-15T10:30:05Z"
        }
    ],
    "total_count": 342,
    "has_more": true
}
```

### Get Audio Details

Get detailed information about a specific audio file.

```http
GET /api/v1/assets/audio/{audio_id}
```

**Response:**
```json
{
    "id": "audio_123",
    "url": "/assets/audio/voice_123.wav",
    "waveform_url": "/assets/audio/voice_123_waveform.png",
    "text": "Hello, this is a test of the voice generation system!",
    "voice_model": "coqui-tts",
    "speaker_id": "female_1",
    "settings": {
        "speed": 1.0,
        "pitch": 1.0,
        "emotion": "neutral",
        "language": "en"
    },
    "metadata": {
        "duration_seconds": 4.2,
        "sample_rate": 22050,
        "channels": 1,
        "format": "wav",
        "file_size_bytes": 185472,
        "bitrate_kbps": 352
    },
    "analysis": {
        "pitch_hz": 180.5,
        "speaking_rate_wpm": 165,
        "energy_level": 0.7,
        "quality_score": 4.5
    },
    "generation_info": {
        "request_id": "voice_req_123",
        "processing_time_seconds": 5,
        "model_version": "1.0.2"
    },
    "created_at": "2024-01-15T10:30:05Z"
}
```

### Delete Audio

Delete a generated audio file.

```http
DELETE /api/v1/assets/audio/{audio_id}
```

**Response:**
```json
{
    "audio_id": "audio_123",
    "status": "deleted",
    "freed_space_bytes": 185472,
    "deleted_at": "2024-01-15T11:00:00Z"
}
```

## Health & Status

### Health Check

Check service health and model status.

```http
GET /api/v1/health
```

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2024-01-15T11:00:00Z",
    "version": "1.0.0",
    "uptime_seconds": 7200,
    "system_info": {
        "cpu_count": 8,
        "memory_total_gb": 16.0,
        "memory_used_gb": 4.2,
        "memory_available_gb": 11.8
    },
    "gpu_info": {
        "available": true,
        "count": 1,
        "devices": [
            {
                "id": 0,
                "name": "NVIDIA GeForce RTX 4090",
                "memory_total_gb": 24.0,
                "memory_used_gb": 2.1,
                "utilization_percent": 15
            }
        ]
    },
    "loaded_models": [
        {
            "model_id": "coqui-tts",
            "language": "en",
            "speaker_id": "female_1",
            "memory_usage_mb": 512
        }
    ],
    "queue_status": {
        "pending_requests": 0,
        "processing_requests": 1,
        "completed_today": 342
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
        "total": 2847,
        "today": 342,
        "per_hour": 47.5,
        "success_rate_percent": 97.8
    },
    "generation": {
        "average_time_seconds": 3.8,
        "median_time_seconds": 3.2,
        "fastest_time_seconds": 1.1,
        "slowest_time_seconds": 15.6,
        "real_time_factor": 0.85
    },
    "queue": {
        "current_length": 1,
        "max_length_today": 8,
        "average_wait_time_seconds": 2.1
    },
    "storage": {
        "total_audio_files": 2847,
        "total_size_gb": 12.3,
        "available_space_gb": 487.7
    },
    "models": {
        "coqui-tts": {
            "generations": 2234,
            "success_rate": 98.1,
            "average_time_seconds": 3.5
        },
        "bark": {
            "generations": 613,
            "success_rate": 96.7,
            "average_time_seconds": 8.2
        }
    }
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_TEXT` | 400 | Text is empty or contains invalid characters |
| `TEXT_TOO_LONG` | 400 | Text exceeds maximum length limit |
| `INVALID_VOICE_MODEL` | 400 | Specified voice model is invalid |
| `INVALID_SPEAKER` | 400 | Specified speaker ID is invalid |
| `UNSUPPORTED_FORMAT` | 400 | Requested audio format is not supported |
| `MODEL_NOT_LOADED` | 404 | Voice model is not currently loaded |
| `AUDIO_NOT_FOUND` | 404 | Audio file not found |
| `INSUFFICIENT_MEMORY` | 507 | Not enough memory to load model |
| `GENERATION_FAILED` | 500 | Voice generation process failed |
| `MODEL_LOAD_FAILED` | 500 | Failed to load voice model |

## SDK Example

### Python SDK

```python
import requests
import time
import base64

class VocalizrClient:
    def __init__(self, base_url="http://localhost:8001", api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}" if api_key else None
        }
    
    def generate_speech(self, text, voice_model="coqui-tts", **kwargs):
        """Generate speech from text"""
        data = {
            "text": text,
            "voice_model": voice_model,
            **kwargs
        }
        response = requests.post(
            f"{self.base_url}/api/v1/generate/speech",
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
    
    def wait_for_completion(self, request_id, timeout=60):
        """Wait for generation to complete"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            status = self.get_status(request_id)
            if status["status"] == "completed":
                return status
            elif status["status"] == "failed":
                raise Exception(f"Generation failed: {status['error']['message']}")
            time.sleep(1)
        raise TimeoutError("Generation timed out")
    
    def list_models(self):
        """Get available voice models"""
        response = requests.get(
            f"{self.base_url}/api/v1/models",
            headers=self.headers
        )
        return response.json()

# Usage
client = VocalizrClient(api_key="your-api-key")

# Generate speech
result = client.generate_speech(
    "Hello, this is a test of voice generation!",
    voice_model="coqui-tts",
    speaker_id="female_1",
    settings={
        "speed": 1.1,
        "emotion": "happy"
    }
)

# Wait for completion
final_result = client.wait_for_completion(result["request_id"])
print(f"Audio URL: {final_result['result']['audio_url']}")
print(f"Duration: {final_result['result']['metadata']['duration_seconds']} seconds")
```

---

For more examples and advanced usage, see the [Development Guide](../development.md).