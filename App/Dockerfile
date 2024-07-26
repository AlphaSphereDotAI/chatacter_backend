FROM ghcr.io/prefix-dev/pixi:jammy-cuda-12.3.1

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive \
    # UV_NO_CACHE=true \
    UV_INDEX_STRATEGY=unsafe-best-match \
    UV_EXTRA_INDEX_URL=https://download.pytorch.org/whl/cu121
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends libgl1-mesa-glx gcc g++ libglib2.0-0 && \
    apt-get full-upgrade -y && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pixi init && \
    # pixi clean && \
    pixi add python=3.10 uv && \
    pixi run uv pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["pixi", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]
