from chatacter.model import generate_video
from chatacter.settings import get_settings
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(debug=True)
settings = get_settings()


@app.get("/")
async def is_alive():
    return {"message": "Chatacter Video Generator is alive!", "status": "ok"}


@app.get("/get_settings")
async def get_settings():
    return settings.model_dump()


@app.get("/get_video")
def get_video():
    generate_video()
    return FileResponse(settings.assets.video, media_type="video/mp4")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8002, reload=True)
