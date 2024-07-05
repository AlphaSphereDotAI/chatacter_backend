import time
from transformers import logging
import subprocess
from chatacter.settings import get_settings

settings = get_settings()
logging.set_verbosity_debug()


def generate_video(character : str) -> str:
    start_time = time.time()
    subprocess.run(
        [
            "python",
            "inference.py",
            "--driven_audio",
            "./assets/audio/AUDIO.wav",
            "--source_image",
            f"./assets/image/{character}.jpg",
            "--result_dir",
            "./assets/results",
            "--still",
            "--preprocess",
            "full",
            "--enhancer",
            "gfpgan",
        ]
    )
    end_time = time.time()
    return str(end_time - start_time)
    
