from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

from chatacter.settings import get_settings

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
    return FileResponse(
        path=settings.assets.audio, media_type="audio/wav", filename="AUDIO.wav"
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="localhost", port=8001, reload=True)
