from chatacter.model import generate_audio, generate_video, get_response
from chatacter.settings import get_settings
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(debug=True)
settings = get_settings()


@app.get("/")
async def is_alive():
    return {"message": "Chatacter is alive!", "status": "ok"}


@app.get("/get_settings")
async def get_settings():
    return settings.model_dump()


@app.post("/set_character")
def set_character(character: str):
    settings.character = character
    return {"status": "ok", "character": settings.character}


@app.post("/get_text")
def get_text(query: str):
    return get_response(query)


@app.get("/get_audio")
def get_audio(text: str):
    return generate_audio(text)


@app.get("/get_video")
def get_video():
    generate_video()
    return FileResponse(settings.assets.video, media_type="video/mp4")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
