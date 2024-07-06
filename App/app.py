from chatacter.model import get_response
from chatacter.settings import get_settings
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
import requests

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
        content=res,    headers={"time": time}
    )


@app.get("/get_audio")
def get_audio(text: str):
    response_audio = requests.get(f"http://localhost:8001/get_audio?text={text}")
    with open("./assets/audio/AUDIO.wav", "wb") as f:
        f.write(response_audio.content)
    return FileResponse(
        path="./assets/audio/AUDIO.wav",
        media_type="audio/wav",
        filename="AUDIO.wav",
    )


@app.get("/get_video")
def get_video(character: str):
    send_audio = requests.post(f"http://localhost:8002/set_audio", files={"file": open("./assets/audio/AUDIO.wav", "rb")})
    response_video = requests.get(f"http://localhost:8002/get_video?character={character}")
    with open("./assets/video/VIDEO.mp4", "wb") as f:
        f.write(response_video.content)
    return FileResponse("./assets/video/VIDEO.mp4", media_type="video/mp4",
        filename="VIDEO.mp4",)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
