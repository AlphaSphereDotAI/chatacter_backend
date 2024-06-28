from functools import lru_cache

from pydantic import BaseModel

class AssetsSettings(BaseModel):
    audio: str = "./chatacter/assets/audio/AUDIO.wav"
    image: str = "./chatacter/assets/image/"
    video: str = "./chatacter/assets/video/VIDEO.mp4"


class BarkSettings(BaseModel):
    path: str = "./chatacter/bark-small"


class Settings(BaseModel):
    app_name: str = "Chatacter"
    assets: AssetsSettings = AssetsSettings()
    bark: BarkSettings = BarkSettings()


@lru_cache
def get_settings():
    return Settings()


if __name__ == "__main__":
    settings = get_settings()
    print(settings.model_dump_json(indent=4))
