from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Chatacter"
    assets: dict = {
        "audio": "assets/AUDIO.wav",
        "image": "assets/Einstein.jpg",
        "video": "assets/VIDEO.mp4",
    }
    model: dict = {
        "bark": "bark-small",
        "sadtalker": {
            "base": "sadtalker",
            "checkpoints": "sadtalker/checkpoints",
            "gfpgan": "sadtalker/gfpgan/weights",
        },
    }
