FROM ghcr.io/prefix-dev/pixi:jammy-cuda-11.7.1

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive \
    TCNN_CUDA_ARCHITECTURES=86

RUN apt-get update && \
    apt-get install --no-install-recommends cuda-11-8 git -y && \
    apt-get full-upgrade -y && \
    apt-get autoremove && \
    apt-get clean && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/*

RUN pixi init && \
    pixi add python==3.9 pip && \
    pixi project channel add pytorch nvidia conda-forge && \
    pixi add ffmpeg && \
    pixi run pip install --upgrade pip setuptools wheel && \
    pixi run pip install --no-cache-dir -v torch==2.0.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

RUN git clone --recursive https://github.com/ashawkey/torch-ngp.git && \
    cd torch-ngp && \
    # pixi run pip install --no-cache-dir -v ./raymarching -v && \
    # pixi run pip install --no-cache-dir -v ./gridencoder -v && \
    # pixi run pip install --no-cache-dir -v ./shencoder -v && \
    # pixi run pip install --no-cache-dir -v ./freqencoder -v && \
    pixi run pip install --no-cache-dir -v git+https://github.com/facebookresearch/pytorch3d.git@stable && \
    pixi run pip install --no-cache-dir -v git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch

WORKDIR /app
COPY requirements.txt .
RUN pixi run pip install -v --no-cache-dir -r requirements.txt --use-pep517 && \
    pixi run mim install mmcv==2.1.0

COPY . .

EXPOSE 8002

CMD ["pixi", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8002"]
