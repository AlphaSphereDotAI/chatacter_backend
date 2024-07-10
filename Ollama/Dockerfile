FROM ollama/ollama:latest

ENV DEBIAN_FRONTEND=noninteractive \
    OLLAMA_DEBUG=1

RUN ollama pull llama3

EXPOSE 11434

CMD ["ollama", "serve"]
