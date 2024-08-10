import time

import torch
from chatacter.settings import get_settings
from scipy.io.wavfile import write
from transformers import AutoModel, AutoProcessor, logging

settings = get_settings()

device = "cuda" if torch.cuda.is_available() else "cpu"
processor = AutoProcessor.from_pretrained(settings.bark.name)
model = AutoModel.from_pretrained(settings.bark.name, torch_dtype=torch.float16).to(
    device
)
model = model.to_bettertransformer()
model.enable_cpu_offload()
logging.set_verbosity_debug()


def generate_audio(response):
    print("Device available: ", model.device)
    start_time = time.time()
    inputs = processor(
        text=[response], return_tensors="pt", voice_preset="v2/en_speaker_6"
    )
    inputs = inputs.to(device)
    audio = model.generate(**inputs)
    audio = audio.cpu().squeeze(0).numpy()
    sample_rate = model.generation_config.sample_rate
    write(
        f"{settings.assets.audio}AUDIO.wav",
        sample_rate,
        audio,
    )
    end_time = time.time()
    return {
        "audio_dir": settings.assets.audio,
        "rate": model.generation_config.sample_rate,
        "text": response,
        "status": "ok",
        "time": end_time - start_time,
    }
