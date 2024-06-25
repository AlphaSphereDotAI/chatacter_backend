FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

# COPY .venv /app/.venv
COPY . /app
WORKDIR /app

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

# RUN apt-get update
# RUN apt-get install ffmpeg -y
# RUN apt-get install x264 -y
# RUN apt-get full-upgrade -y
# RUN apt-get autoremove

RUN conda init
RUN conda update -v -y conda
RUN conda install -c conda-forge -y \
    imageio=2.19.3 \
    imageio-ffmpeg=0.4.7 \
    librosa=0.9.2  \
    pydub=0.25.1  \
    kornia=0.6.8  \
    yacs=0.1.8  \
    scikit-image=0.19.3  \
    facexlib=0.3.0  \
    trimesh=3.9.20 \
    fastapi \
    huggingface_hub \
    langchain-groq \
    opencv \
    transformers \
    pydantic \
    libsndfile \
    accelerate \
    optimum \
    uvicorn \
    pysoundfile
RUN pip install -v --use-pep517 \
    langchain-community \
    langchain-qdrant \
    gfpgan \
    wget \
    cog \
    face_alignment==1.3.5 \
    opencv-python-headless \
    unstructured[all-docs] \
    basicsr==1.4.2