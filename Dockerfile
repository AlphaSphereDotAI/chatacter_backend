FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install --no-install-recommends ffmpeg x264 wget -y && \
    apt-get full-upgrade -y && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

RUN mkdir -p ./chatacter/sadtalker/checkpoints && \
    mkdir -p ./chatacter/sadtalker/gfpgan/weights && \
    mkdir -p ./chatacter/bark-small && \
    wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar -O  ./chatacter/sadtalker/checkpoints/mapping_00109-model.pth.tar && \
    wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00229-model.pth.tar -O  ./chatacter/sadtalker/checkpoints/mapping_00229-model.pth.tar && \
    wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_256.safetensors -O  ./chatacter/sadtalker/checkpoints/SadTalker_V0.0.2_256.safetensors && \
    wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_512.safetensors -O  ./chatacter/sadtalker/checkpoints/SadTalker_V0.0.2_512.safetensors && \
    wget -nc https://huggingface.co/vinthony/SadTalker-V002rc/resolve/main/epoch_00190_iteration_000400000_checkpoint.pt?download=true -O ./chatacter/sadtalker/checkpoints/epoch_00190_iteration_000400000_checkpoint.pt && \
    wget -nc https://github.com/xinntao/facexlib/releases/download/v0.1.0/alignment_WFLW_4HG.pth -O ./chatacter/sadtalker/gfpgan/weights/alignment_WFLW_4HG.pth && \
    wget -nc https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth -O ./chatacter/sadtalker/gfpgan/weights/detection_Resnet50_Final.pth && \
    wget -nc https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth -O ./chatacter/sadtalker/gfpgan/weights/GFPGANv1.4.pth && \
    wget -nc https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth -O ./chatacter/sadtalker/gfpgan/weights/parsing_parsenet.pth && \
    wget -nc https://huggingface.co/suno/bark-small/resolve/main/pytorch_model.bin?download=true -O ./chatacter/bark-small/pytorch_model.bin

RUN pip install -v --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["fastapi", "dev"]
