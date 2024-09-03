FROM ghcr.io/prefix-dev/pixi:jammy-cuda-12.3.1

SHELL ["/bin/bash", "-c"]

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive \
    UV_NO_CACHE=true \
    # UV_INDEX_STRATEGY=unsafe-best-match \
    # UV_EXTRA_INDEX_URL=https://download.pytorch.org/whl/cu121 \
    PATH="/root/.pixi/bin:${PATH}"

RUN apt-get update && \
    apt-get install -y --no-install-recommends clang g++ gcc libglib2.0-0 libgl1-mesa-glx && \
    apt-get full-upgrade -y && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .

RUN pixi global install uv && \
    uv python install 3.11 && \
    uv python pin 3.11 && \
    uv sync && \
    uv lock --upgrade && \
    uv run python -m nltk.downloader punkt && \
    uv run python -m nltk.downloader averaged_perceptron_tagger

COPY . .

EXPOSE 8000

CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]
