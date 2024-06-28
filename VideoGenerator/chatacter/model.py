import time
from transformers import  logging

from chatacter.sadtalker.predict import Predictor
from chatacter.settings import get_settings

settings = get_settings()

logging.set_verbosity_debug()

def generate_video() -> dict:
    start_time = time.time()
    predictor = Predictor()
    predictor.setup()
    try:
        predictor.predict(
            source_image=settings.assets.image + settings.character + ".jpg",
            driven_audio=settings.assets.audio,
            enhancer="gfpgan",
            preprocess="full",
        )
    except Exception as e:
        end_time = time.time()
        return {"status": e, "time": end_time - start_time}
    end_time = time.time()
    return {
        "video": settings.assets.video,
        "status": "ok",
        "time": end_time - start_time,
    }
