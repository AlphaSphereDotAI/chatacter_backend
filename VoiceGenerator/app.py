from chatacter.model import generate_audio
from chatacter.settings import get_settings
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI(
    debug=True,
    title="Character Voice Generator",
    description="Character Voice Generator API",
)
settings = get_settings()


@app.get("/")
async def is_alive():
    return JSONResponse(
        content={"message": "Chatacter Voice Generator is alive!", "status": "ok"}
    )


@app.get("/get_settings")
async def get_settings():
    return JSONResponse(content=settings.model_dump())


@app.get("/get_audio")
def get_audio(text: str):
    generate_audio(text)
    return FileResponse(
        path=settings.assets.audio, media_type="audio/wav", filename="AUDIO.wav"
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="localhost", port=8001, reload=True)
