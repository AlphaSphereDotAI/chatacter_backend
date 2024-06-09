from huggingface_hub import snapshot_download
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from scipy.io.wavfile import write
from transformers import AutoModelForTextToWaveform, AutoProcessor

from settings import get_settings
from sadtalker.predict import Predictor

settings = get_settings()

snapshot_download(repo_id="suno/bark-small", local_dir=settings.bark.path)
processor = AutoProcessor.from_pretrained(settings.bark.path)
model = AutoModelForTextToWaveform.from_pretrained(settings.bark.path)
processor = AutoProcessor.from_pretrained(settings.bark.path)
model = AutoModelForTextToWaveform.from_pretrained(settings.bark.path)
chat = ChatGroq(model_name="llama3-70b-8192", verbose=True)


def generate_audio(response):
    """generate audio"""
    print("\tChatacter is generating the audio...")
    inputs = processor(response, return_tensors="pt")
    audio = model.generate(**inputs)
    print("\tAudio generated with Rate 24000")
    print("\tSaving audio...")
    write(settings.assets.audio, 24000, audio.squeeze(0).numpy())


def generate_video():
    """generate video"""
    print("\tChatacter is generating the video...")
    predictor = Predictor()
    predictor.setup()
    predictor.predict(
        source_image=settings.assets.image,
        driven_audio=settings.assets.audio,
        enhancer="gfpgan",
        preprocess="full",
    )


def get_response(query):
    """get response function"""
    print(f"Sending '{query}' to Chatacter...")
    print("Thinking...")
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Act as Napoleon Bonaparte. Answer in one statement."),
            ("human", "{text}"),
        ]
    )
    chain = prompt | chat
    response = chain.invoke({"text": query})
    return response.content
