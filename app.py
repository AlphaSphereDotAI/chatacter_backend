import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from model import generate_audio, generate_video, get_response
import sentry_sdk
import os

sentry_sdk.init(
    dsn=os.environ['SENTRY'],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)
app = FastAPI()
CONFIG = pd.read_json("config.json")

@app.get("/")
async def is_alive():
    """hello world function"""
    return {
        "message": "Hello World",
        "status": "ok",
    }


@app.post("/get_text")
def get_text(query: str):
    """get text response function"""
    return get_response(query)


@app.get("/get_audio")
def get_audio(text: str):
    """generate the audio file"""
    return generate_audio(text)


@app.get("/get_video")
def get_video():
    """generate the video file"""
    generate_video()
    return FileResponse(CONFIG["video"], media_type="video/mp4")


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8001, reload=True)
