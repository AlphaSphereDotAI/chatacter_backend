from functools import lru_cache
from pydantic import BaseModel


class SadTalkerSettings(BaseModel):
    path: str = "chatacter/sadtalker"
    checkpoints: str = "chatacter/sadtalker/checkpoints"
    gfpgan: str = "chatacter/sadtalker/gfpgan/weights"


class AssetsSettings(BaseModel):
    audio: str = "chatacter/assets/AUDIO.wav"
    image: str = "chatacter/assets/Einstein.jpg"
    video: str = "chatacter/assets/VIDEO.mp4"


class BarkSettings(BaseModel):
    path: str = "chatacter/bark-small"


class Settings(BaseModel):
    app_name: str = "Chatacter"
    assets: AssetsSettings = AssetsSettings()
    sadtalker: SadTalkerSettings = SadTalkerSettings()
    bark: BarkSettings = BarkSettings()


@lru_cache
def get_settings():
    return Settings()


if __name__ == "__main__":
    settings = get_settings()
    print(settings.model_dump_json(indent=4))
