from functools import lru_cache

from pydantic import BaseModel


class ModelConfig(BaseModel):
    path: str
    checkpoints: str
    gfpgan: str


class Assets(BaseModel):
    audio: str
    image: str
    video: str


class Settings(BaseModel):
    app_name: str = "Chatacter"
    assets: Assets = Assets(
        audio="assets/AUDIO.wav",
        image="assets/Einstein.jpg",
        video="assets/VIDEO.mp4",
    )
    sadtalker: ModelConfig = ModelConfig(
        path="sadtalker",
        checkpoints="sadtalker/checkpoints",
        gfpgan="sadtalker/gfpgan/weights",
    )
    bark: ModelConfig = ModelConfig(path="bark-small")


@lru_cache
def get_settings():
    return Settings()
