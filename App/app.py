import requests
from chatacter.model import get_response
from chatacter.settings import get_settings
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI(debug=True)
settings = get_settings()


@app.get("/")
async def is_alive():
    return {"message": "Chatacter is alive!", "status": "ok"}


@app.get("/get_settings")
async def get_settings():
    return settings.model_dump()


@app.get("/get_text")
def get_text(query: str, character: str):
    res, time = get_response(query, character)
    return JSONResponse(
        content=res,
        headers={"time": time},
    )


@app.get("/get_audio")
def get_audio(text: str):
    response_audio = requests.get(
        f"{settings.host.voice_generator}get_audio?text={text}"
    )
    with open(settings.assets.audio, "wb") as f:
        f.write(response_audio.content)
    return FileResponse(
        path=settings.assets.audio,
        media_type="audio/wav",
        filename="AUDIO.wav",
    )


@app.get("/get_video")
def get_video(character: str):
    send_audio = requests.post(
        f"{settings.host.video_generator}set_audio",
        files={"file": open(settings.assets.audio, "rb")},
    )
    response_video = requests.get(
        f"{settings.host.video_generator}get_video?character={character}"
    )
    with open(settings.assets.video, "wb") as f:
        f.write(response_video.content)
    return FileResponse(
        settings.assets.video,
        media_type="video/mp4",
        filename="VIDEO.mp4",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="localhost",
        port=8000,
        reload=True,
    )
