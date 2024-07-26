FROM ghcr.io/prefix-dev/pixi:jammy-cuda-12.3.1

SHELL ["/bin/bash", "-c"]
WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive \
    UV_NO_CACHE=true \
    UV_INDEX_STRATEGY=unsafe-best-match \
    UV_EXTRA_INDEX_URL=https://download.pytorch.org/whl/cu121 \
    PATH="/root/.pixi/bin:${PATH}"

RUN apt-get update && \
    apt-get install -y --no-install-recommends libgl1-mesa-glx gcc g++ libglib2.0-0 software-properties-common python-is-python3 && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    apt install -y python3.10
    apt-get full-upgrade -y && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pixi global install uv && \
    uv venv --seed && \
    uv pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]
