import warnings

from chatacter.model import generate_audio
from chatacter.settings import get_settings
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

warnings.filterwarnings("ignore")

app = FastAPI(
    debug=True,
    title="Character Voice Generator",
    description="Character Voice Generator API",
)
settings = get_settings()


@app.get("/")
async def is_alive():
    return JSONResponse(
        content={
            "message": "Chatacter Voice Generator is alive!",
        },
    )


@app.get("/get_settings")
async def get_settings():
    return JSONResponse(
        content=settings.model_dump(),
    )


@app.get("/get_audio")
def get_audio(text: str):
    print("Generating audio for: ", text)
    results = generate_audio(text)
    return FileResponse(
        path=f"{settings.assets.audio}AUDIO.wav",
        media_type="audio/wav",
        filename="AUDIO.wav",
        headers={
            "text": results["text"],
            "time": str(results["time"]),
            "rate": str(results["rate"]),
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="localhost", port=8001, reload=True)
