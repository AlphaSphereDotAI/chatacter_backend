FROM ghcr.io/prefix-dev/pixi:jammy-cuda-11.7.1

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install --no-install-recommends cuda -y && \
    apt-get full-upgrade -y && \
    apt-get autoremove && \
    apt-get clean && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/*

RUN pixi init && \
    pixi add python==3.9 pip && \
    pixi project channel add pytorch nvidia conda-forge && \
    pixi add ffmpeg && \
    pixi run pip install --no-cache-dir -v torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

RUN git clone https://github.com/yerfor/GeneFacePlusPlus.git && \
    cd GeneFacePlusPlus && \
    pixi run pip install --no-cache-dir -v git+https://github.com/facebookresearch/pytorch3d.git@stable && \
    pixi run pip install --no-cache-dir -v ./modules/radnerfs/encoders/freqencoder -v && \
    pixi run pip install --no-cache-dir -v ./modules/radnerfs/encoders/shencoder -v && \
    pixi run pip install --no-cache-dir -v ./modules/radnerfs/encoders/gridencoder -v && \
    pixi run pip install --no-cache-dir -v ./modules/radnerfs/raymarching -v 

WORKDIR /app
COPY requirements.txt .
RUN pixi run pip install -v --no-cache-dir -r requirements.txt --use-pep517 && \
    pixi run mim install mmcv==2.1.0

COPY . .

EXPOSE 8002

CMD ["pixi", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8002"]
