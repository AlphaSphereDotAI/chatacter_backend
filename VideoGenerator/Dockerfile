FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive \
    TCNN_CUDA_ARCHITECTURES=86 \
    CUDA_HOME=/opt/conda

RUN apt-get update && \
    apt-get install --no-install-recommends ffmpeg gcc git build-essential python3-dev libasound2-dev portaudio19-dev -y && \
    apt-get full-upgrade -y && \
    apt-get autoremove && \
    apt-get clean && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/*

RUN conda install nvidia/label/cuda-11.7.0::cuda-toolkit -y

RUN git clone --recursive https://github.com/ashawkey/torch-ngp.git && \
    cd torch-ngp && \
    pip install --no-cache-dir -v -r requirements.txt --use-pep517 && \
    pip install --no-cache-dir -v git+https://github.com/facebookresearch/pytorch3d.git@stable

RUN cd ./chatacter/GeneFacePlusPlus && \
    pip install ./modules/radnerfs/encoders/freqencoder -v && \
    pip install ./modules/radnerfs/encoders/shencoder -v && \
    pip install ./modules/radnerfs/encoders/gridencoder -v && \
    pip install ./modules/radnerfs/raymarching -v

WORKDIR /app
COPY requirements.txt .
RUN pip install -v --no-cache-dir -r requirements.txt && \
    mim install mmcv==2.1.0

COPY . .

EXPOSE 8002

CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]
