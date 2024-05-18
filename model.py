import pandas as pd
# from dotenv_vault import load_dotenv
from huggingface_hub import snapshot_download
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from sadtalker.predict import Predictor
from scipy.io.wavfile import write
from transformers import AutoModelForTextToWaveform, AutoProcessor

CONFIG = pd.read_json("config.json")
# load_dotenv()

snapshot_download(repo_id="suno/bark-small", local_dir=CONFIG["model"]["bark"])
processor = AutoProcessor.from_pretrained(CONFIG["model"]["bark"])
model = AutoModelForTextToWaveform.from_pretrained(CONFIG["model"]["bark"])
processor = AutoProcessor.from_pretrained(CONFIG["model"]["bark"])
model = AutoModelForTextToWaveform.from_pretrained(CONFIG["model"]["bark"])
chat = ChatGroq(model_name="llama3-70b-8192", verbose=True)


def generate_audio(response):
    """generate audio"""
    print("\tChatacter is generating the audio...")
    inputs = processor(response, return_tensors="pt")
    audio = model.generate(**inputs)
    print("\tAudio generated with Rate 24000")
    print("\tSaving audio...")
    write(CONFIG["assets"]["audio"], 24000, audio.squeeze(0).numpy())


def generate_video():
    """generate video"""
    print("\tChatacter is generating the video...")
    predictor = Predictor()
    predictor.setup()
    predictor.predict(
        source_image=CONFIG["assets"]["source_image"],
        driven_audio=CONFIG["assets"]["audio"],
        enhancer="gfpgan",
        preprocess="full",
    )


def get_response(query):
    """get response function"""
    print(f"Sending '{query}' to Chatacter...")
    print("Thinking...")
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Ack as Napoleon Bonaparte. Answer in one statement."),
            ("human", "{text}"),
        ]
    )
    chain = prompt | chat
    response = chain.invoke({"text": query})
    return response.content
