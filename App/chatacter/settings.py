from functools import lru_cache

from pydantic import BaseModel


class AssetsSettings(BaseModel):
    audio: str = "chatacter/assets/audio/AUDIO.wav"
    image: str = "chatacter/assets/image/"
    video: str = "chatacter/assets/video/VIDEO.mp4"


class HostSettings(BaseModel):
    voice_generator: str = "http://localhost:8001/"
    video_generator: str = "http://localhost:8002/"


class Settings(BaseModel):
    app_name: str = "Chatacter"
    assets: AssetsSettings = AssetsSettings()
    character: str = str()
    host: HostSettings = HostSettings()


@lru_cache
def get_settings():
    return Settings()


if __name__ == "__main__":
    settings = get_settings()
    print(settings.model_dump_json(indent=4))
