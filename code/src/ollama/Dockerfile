cat Dockerfile 
FROM ollama/ollama:latest

# Set working directory
WORKDIR /root

# Create directories for models and config
RUN mkdir -p /root/.ollama/models
RUN mkdir -p /config

# Environment variables
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_MODELS=/root/.ollama/models

# Expose the Ollama API port
EXPOSE 11434

# Set up healthcheck to monitor Ollama service
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:11434/api/health || exit 1

# Define volumes for persisting models and configuration
VOLUME ["/root/.ollama/models", "/config"]

# Start Ollama service
CMD ["ollama", "serve"]
