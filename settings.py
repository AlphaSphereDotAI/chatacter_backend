from functools import lru_cache

from pydantic import BaseModel


class SadTalkerSettings(BaseModel):
    path: str = "sadtalker"
    checkpoints: str = "sadtalker/checkpoints"
    gfpgan: str = "sadtalker/gfpgan/weights"


class AssetsSettings(BaseModel):
    audio: str = "assets/AUDIO.wav"
    image: str = "assets/Einstein.jpg"
    video: str = "assets/VIDEO.mp4"


class BarkSettings(BaseModel):
    path: str = "bark-small"


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
