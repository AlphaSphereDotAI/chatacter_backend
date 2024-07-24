FROM python:3.10-slim

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends libgl1-mesa-glx gcc g++ && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -v --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu121

COPY . .

EXPOSE 8000

CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]
