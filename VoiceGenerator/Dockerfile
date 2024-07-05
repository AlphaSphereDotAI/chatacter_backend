FROM ghcr.io/prefix-dev/pixi:jammy-cuda-12.1.1

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

RUN apt-get update && \
    apt-get full-upgrade -y && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pixi init && \
    pixi add python==3.10 pip && \
    pixi project channel add pytorch nvidia conda-forge && \
    pixi run pip install --upgrade pip setuptools wheel && \
    pixi run pip install -v --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu121

RUN pixi run huggingface-cli download suno/bark-small

COPY . .

EXPOSE 8001

CMD ["pixi", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8001"]
