import time
from huggingface_hub import snapshot_download
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from scipy.io.wavfile import write
from transformers import AutoModel, AutoProcessor, logging
from chatacter.settings import get_settings
import requests

settings = get_settings()
chat = ChatGroq(model_name="llama3-70b-8192", verbose=True)
logging.set_verbosity_debug()


def generate_audio(response) -> dict:
    start_time = time.time()
    try:
        audio_response = requests.get(f"{settings.host.voice_generator}?text={response}")
    except Exception as e:
        end_time = time.time()
        return {"status": e, "time": end_time - start_time}
    try:
        write(
            settings.assets.audio,
            model.generation_config.sample_rate,
            audio.cpu().squeeze(0).numpy(),
        )
    except Exception as e:
        end_time = time.time()
        return {"status": e, "time": end_time - start_time}
    end_time = time.time()
    return {
        "audio": settings.assets.audio,
        "rate": model.generation_config.sample_rate,
        "text": response,
        "status": audio_response.status_code,
        "time": end_time - start_time,
    }


def generate_video() -> dict:
    start_time = time.time()
    predictor = Predictor()
    predictor.setup()
    try:
        predictor.predict(
            source_image=settings.assets.image + settings.character + ".jpg",
            driven_audio=settings.assets.audio,
            enhancer="gfpgan",
            preprocess="full",
        )
    except Exception as e:
        end_time = time.time()
        return {"status": e, "time": end_time - start_time}
    end_time = time.time()
    return {
        "video": settings.assets.video,
        "status": "ok",
        "time": end_time - start_time,
    }


def get_response(query) -> dict:
    start_time = time.time()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Act as Napoleon Bonaparte. Answer in one statement."),
            ("human", "{text}"),
        ]
    )
    chain = prompt | chat
    try:
        response = chain.invoke({"text": query})
    except Exception as e:
        end_time = time.time()
        return {"status": e, "time": end_time - start_time}
    end_time = time.time()
    return {
        "response": response.content,
        "status": "ok",
        "time": end_time - start_time,
    }
