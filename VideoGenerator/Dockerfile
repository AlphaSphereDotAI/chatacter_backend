FROM ghcr.io/prefix-dev/pixi:jammy-cuda-11.7.1

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install --no-install-recommends ffmpeg gcc git build-essential python3-dev libasound2-dev portaudio19-dev -y && \
    apt-get full-upgrade -y && \
    apt-get autoremove && \
    apt-get clean && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/*

RUN pixi init && \
    pixi add python==3.9 pip && \
    pixi project channel add https://repo.prefix.dev/pytorch https://repo.prefix.dev/nvidia https://repo.prefix.dev/conda-forge && \
    pixi add pytorch=2.0.1 torchvision torchaudio pytorch-cuda=11.8

RUN git clone https://github.com/yerfor/GeneFacePlusPlus.git && \
    cd GeneFacePlusPlus && \
    pixi run pip install ./modules/radnerfs/encoders/freqencoder -v && \
    pixi run pip install ./modules/radnerfs/encoders/shencoder -v && \
    pixi run pip install ./modules/radnerfs/encoders/gridencoder -v && \
    pixi run pip install ./modules/radnerfs/raymarching -v && \
    pixi run pip install --no-cache-dir -v git+https://github.com/facebookresearch/pytorch3d.git@stable

WORKDIR /app
COPY requirements.txt .
RUN pixi run pip install -v --no-cache-dir -r requirements.txt --use-pep517 && \
    pixi run mim install mmcv==2.1.0

COPY . .

EXPOSE 8002

CMD ["pixi", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8002"]
