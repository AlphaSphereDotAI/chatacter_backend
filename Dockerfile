FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

COPY . /app
WORKDIR /app

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install ffmpeg -y
RUN apt-get install x264 -y
RUN apt-get install wget -y
RUN apt-get full-upgrade -y
RUN apt-get autoremove

RUN mkdir ./app/chatacter/sadtalker/checkpoints  
RUN wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar -O  ./app/chatacter/sadtalker/checkpoints/mapping_00109-model.pth.tar
RUN wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00229-model.pth.tar -O  ./app/chatacter/sadtalker/checkpoints/mapping_00229-model.pth.tar
RUN wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_256.safetensors -O  ./app/chatacter/sadtalker/checkpoints/SadTalker_V0.0.2_256.safetensors
RUN wget -nc https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_512.safetensors -O  ./app/chatacter/sadtalker/checkpoints/SadTalker_V0.0.2_512.safetensors
RUN wget -nc https://huggingface.co/vinthony/SadTalker-V002rc/resolve/main/epoch_00190_iteration_000400000_checkpoint.pt?download=true -O ./app/chatacter/sadtalker/checkpoints/epoch_00190_iteration_000400000_checkpoint.pt

RUN mkdir -p ./app/chatacter/sadtalker/gfpgan/weights
RUN wget -nc https://github.com/xinntao/facexlib/releases/download/v0.1.0/alignment_WFLW_4HG.pth -O ./app/chatacter/sadtalker/gfpgan/weights/alignment_WFLW_4HG.pth
RUN wget -nc https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth -O ./app/chatacter/sadtalker/gfpgan/weights/detection_Resnet50_Final.pth 
RUN wget -nc https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth -O ./app/chatacter/sadtalker/gfpgan/weights/GFPGANv1.4.pth 
RUN wget -nc https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth -O ./app/chatacter/sadtalker/gfpgan/weights/parsing_parsenet.pth 

RUN conda init
RUN conda update -y conda
RUN conda env update
CMD ["fastapi", "dev"]
