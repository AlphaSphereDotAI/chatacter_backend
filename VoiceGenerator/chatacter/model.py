import time

from chatacter.settings import get_settings
from huggingface_hub import snapshot_download
from scipy.io.wavfile import write
from transformers import AutoModel, AutoProcessor, logging

settings = get_settings()

snapshot_download(repo_id="suno/bark-small", local_dir=settings.bark.path)
processor = AutoProcessor.from_pretrained(settings.bark.path)
model = AutoModel.from_pretrained(settings.bark.path, cache_dir=settings.bark.path)
model = model.to_bettertransformer()
model.enable_cpu_offload()
logging.set_verbosity_debug()


def generate_audio(response):
    start_time = time.time()
    inputs = processor(response, return_tensors="pt")
    audio = model.generate(**inputs)
    write(
        settings.assets.audio,
        model.generation_config.sample_rate,
        audio.cpu().squeeze(0).numpy(),
    )
    end_time = time.time()
    return {
        "audio_dir": settings.assets.audio,
        "rate": model.generation_config.sample_rate,
        "text": response,
        "status": "ok",
        "time": end_time - start_time,
    }
