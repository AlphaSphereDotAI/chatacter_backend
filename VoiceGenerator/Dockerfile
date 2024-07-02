FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

RUN apt-get update && \
    apt-get full-upgrade -y && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -v --no-cache-dir -r requirements.txt

RUN mkdir -p ./chatacter/bark-small && \
    huggingface-cli download suno/bark-small --local-dir ./chatacter/bark-small

COPY . .

EXPOSE 8001

CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8001"]
