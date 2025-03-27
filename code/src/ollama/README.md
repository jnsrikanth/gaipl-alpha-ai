# GLPI AI Integration

This project integrates AI capabilities with GLPI using a containerized architecture including Ollama for model hosting.

## Project Structure

```
.
├── ollama/                         # Ollama service for AI model hosting
│   ├── Dockerfile                  # Ollama container configuration
│   ├── models/                     # Pre-downloaded models
│   └── config/                     # Ollama configuration
├── docker-compose.yml              # Container orchestration configuration
└── README.md                       # Project documentation
```

## Ollama Setup

Ollama is used to host and serve the LLM models locally. The service is containerized and configured to work with the rest of the application stack.

### Mistral Model

This project uses the Mistral model, which offers a great balance between performance and resource requirements.

#### Mistral Model Specifications

- **Model Name**: Mistral (mistral:7b)
- **Size**: 7 billion parameters
- **Quantization Options**:
  - mistral:7b (full precision)
  - mistral:7b-q4_0 (4-bit quantized)
  - mistral:7b-q4_K_M (4-bit quantized with key/value cache in fp16)
- **Context Length**: 8,192 tokens
- **RAM Requirements**:
  - Full precision: ~16GB RAM
  - 4-bit quantized: ~5-8GB RAM
- **Disk Space**: ~4-5GB (depending on quantization)
- **License**: Apache 2.0

#### Pulling the Mistral Model

To use the Mistral model with Ollama, it needs to be pulled first. The Docker setup will attempt to pull the model automatically, but you can also pull it manually:

```bash
# If using Ollama directly on your host:
ollama pull mistral:7b

# Or, for a more efficient version with 4-bit quantization:
ollama pull mistral:7b-q4_0
```

If you're using our Docker setup, you can pull the model via the container:

```bash
docker-compose exec ollama ollama pull mistral:7b-q4_0
```

#### Mistral Model Usage

The Mistral model can be used via the Ollama API. Here's a simple example:

```bash
# Basic prompt completion
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "mistral:7b-q4_0",
  "prompt": "Explain the importance of knowledge management systems:",
  "stream": false
}'
```

In your application code, you can use the Ollama client libraries to interact with the model:

```python
# Using the Python client
import ollama

response = ollama.generate(model='mistral:7b-q4_0', 
                          prompt='Write a brief summary of ITIL best practices')
print(response['response'])
```

#### Model Configuration

You can customize the model behavior by setting parameters in your requests:

```json
{
  "model": "mistral:7b-q4_0",
  "prompt": "Summarize this document: [document text]",
  "options": {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "num_predict": 100
  }
}
```

## Getting Started

1. Clone the repository
2. Build and start the services:
   ```bash
   docker-compose up -d
   ```
3. The Ollama service will automatically download the Mistral model on first use
4. Access the Ollama API at http://localhost:11434

## Environment Variables

The following environment variables can be set to customize the behavior:

| Variable | Description | Default |
|----------|-------------|---------|
| OLLAMA_HOST | Host address for Ollama API | 0.0.0.0 |
| OLLAMA_PORT | Port for Ollama API | 11434 |
| OLLAMA_MODELS | Comma-separated list of models to preload | mistral:7b-q4_0 |

## Troubleshooting

### Common Mistral Model Issues

1. **Out of Memory Errors**: 
   - If you encounter OOM errors, try using a more quantized version (mistral:7b-q4_0)
   - Increase the container memory limit in docker-compose.yml

2. **Slow First Response**: 
   - The first request to the model may be slow as the model loads into memory
   - Subsequent requests will be much faster

3. **Model Not Found**: 
   - Ensure the model has been pulled correctly
   - Check the Ollama logs: `docker-compose logs ollama`

4. **Model Loading Failures**:
   - If the model fails to load, check that you have sufficient disk space
   - Verify the model files aren't corrupted by re-pulling the model

