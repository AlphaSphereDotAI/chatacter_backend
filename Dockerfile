FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

COPY . /app
WORKDIR /app

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install ffmpeg x264 wget -y && \
    apt-get full-upgrade -y && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chatacter/sadtalker/scripts/download_models.sh

RUN pip install -r requirements.txt

CMD ["fastapi", "dev"]
