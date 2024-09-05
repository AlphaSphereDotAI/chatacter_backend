FROM ghcr.io/prefix-dev/pixi:jammy-cuda-12.3.1

SHELL ["/bin/bash", "-c"]

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive \
    UV_NO_CACHE=true \
    PATH="/root/.pixi/bin:${PATH}"

RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg x264 wget libgl1-mesa-glx libsndfile1 && \
    apt-get full-upgrade -y && \
    apt-get autoremove && \
    apt-get clean && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p ./checkpoints && \
    mkdir -p ./gfpgan/weights && \
    wget --progress=dot:giga -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar -O ./checkpoints/mapping_00109-model.pth.tar && \
    wget --progress=dot:giga -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00229-model.pth.tar -O ./checkpoints/mapping_00229-model.pth.tar && \
    wget --progress=dot:giga -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_256.safetensors -O ./checkpoints/SadTalker_V0.0.2_256.safetensors && \
    wget --progress=dot:giga -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_512.safetensors -O ./checkpoints/SadTalker_V0.0.2_512.safetensors && \
    wget --progress=dot:giga -nc https://huggingface.co/vinthony/SadTalker-V002rc/resolve/main/epoch_00190_iteration_000400000_checkpoint.pt?download=true -O ./checkpoints/epoch_00190_iteration_000400000_checkpoint.pt && \
    wget --progress=dot:giga -nc https://github.com/xinntao/facexlib/releases/download/v0.1.0/alignment_WFLW_4HG.pth -O ./gfpgan/weights/alignment_WFLW_4HG.pth && \
    wget --progress=dot:giga -nc https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth -O ./gfpgan/weights/detection_Resnet50_Final.pth && \
    wget --progress=dot:giga -nc https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth -O ./gfpgan/weights/GFPGANv1.4.pth && \
    wget --progress=dot:giga -nc https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth -O ./gfpgan/weights/parsing_parsenet.pth 

COPY pyproject.toml .

RUN pixi init && \
    pixi add python==3.9 pip && \
    pixi run pip install --upgrade pip setuptools wheel && \
    pixi run pip install -v --no-cache-dir -r requirements.txt --use-pep517 --extra-index-url https://download.pytorch.org/whl/cu113

COPY . .

EXPOSE 8002

CMD ["pixi", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8002"]
