FROM ghcr.io/prefix-dev/pixi:jammy-cuda-12.1.1

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

RUN apt-get update && \
    apt-get install --no-install-recommends ffmpeg x264 wget libgl1-mesa-glx libsndfile1 -y && \
    apt-get full-upgrade -y && \
    apt-get autoremove && \
    apt-get clean && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p ./chatacter/sadtalker/checkpoints && \
    mkdir -p ./chatacter/sadtalker/gfpgan/weights && \
    wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar -O ./chatacter/sadtalker/checkpoints/mapping_00109-model.pth.tar && \
    wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00229-model.pth.tar -O ./chatacter/sadtalker/checkpoints/mapping_00229-model.pth.tar && \
    wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_256.safetensors -O ./chatacter/sadtalker/checkpoints/SadTalker_V0.0.2_256.safetensors && \
    wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_512.safetensors -O ./chatacter/sadtalker/checkpoints/SadTalker_V0.0.2_512.safetensors && \
    wget -nc https://huggingface.co/vinthony/SadTalker-V002rc/resolve/main/epoch_00190_iteration_000400000_checkpoint.pt?download=true -O ./chatacter/sadtalker/checkpoints/epoch_00190_iteration_000400000_checkpoint.pt && \
    wget -nc https://github.com/xinntao/facexlib/releases/download/v0.1.0/alignment_WFLW_4HG.pth -O ./chatacter/sadtalker/gfpgan/weights/alignment_WFLW_4HG.pth && \
    wget -nc https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth -O ./chatacter/sadtalker/gfpgan/weights/detection_Resnet50_Final.pth && \
    wget -nc https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth -O ./chatacter/sadtalker/gfpgan/weights/GFPGANv1.4.pth && \
    wget -nc https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth -O ./chatacter/sadtalker/gfpgan/weights/parsing_parsenet.pth 

COPY requirements.txt .
RUN pip install -v --no-cache-dir -r requirements.txt --use-pep517 --extra-index-url https://download.pytorch.org/whl/cu113

COPY . .

EXPOSE 8002

CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8002"]
