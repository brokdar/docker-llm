# Docker LLM Integration with Pydantic AI

This project demonstrates how to run Large Language Models (LLMs) using Docker's Model Runner on the host system and interact with them from containerized Python applications using Pydantic AI.

## Overview

The project showcases two main integration patterns:

- **Basic CLI interaction** (`basic.py`): Simple command-line interface for LLM queries
- **Web-based chat interface** (`chat.py`): Streamlit-powered chat application with streaming responses

## Docker Model Runner

Docker Model Runner simplifies managing, running, and deploying AI models using Docker. It provides:

- **Model Management**: Pull and push models to Docker Hub as OCI artifacts
- **OpenAI-Compatible APIs**: Serve models via standard REST endpoints
- **Resource Optimization**: Models load on-demand and unload when idle
- **Cross-Platform Support**: Works on Windows, macOS, and Linux with GPU acceleration

### Setup Requirements

1. **Docker Desktop** (Windows 4.41+, macOS 4.40+) or Docker Engine
2. **Enable Docker Model Runner** in Docker Desktop Beta features
3. **⚠️ CRITICAL**: Enable "host-side TCP support" in Docker Model Runner configuration - without this, containers cannot connect to the model server

## Project Structure

```text
├── docker-compose.yaml    # Container orchestration
├── app.env               # Environment configuration
└── app/
    ├── Dockerfile        # Python app container
    ├── pyproject.toml    # Python dependencies
    ├── basic.py          # CLI interaction example
    └── chat.py           # Streamlit chat interface
```

## Usage

### 1. Start Docker Model Runner

Pull and start an LLM model:

```bash
docker model pull ai/smollm2:latest
docker model run ai/smollm2:latest
```

### 2. Run the Application

Start both the LLM service and Python application:

```bash
docker compose up --build
```

This will:

- Pull the `ai/smollm2:latest` model via Docker Model Runner
- Build and run the Python application container
- Expose the Streamlit chat interface on <http://localhost:8501>

### 3. Interact with the LLM

- **Web Interface**: Visit <http://localhost:8501> for the Streamlit chat
- **CLI Interface**: Modify `docker-compose.yaml` to use `basic.py` instead of `chat.py`

## Configuration

The application connects to Docker Model Runner using these environment variables in `app.env`:

```env
BASE_URL=http://host.docker.internal:12434/engines/llama.cpp/v1/
MODEL_NAME=ai/smollm2:latest
API_KEY=dockermodelrunner
```

- `BASE_URL`: Docker Model Runner's OpenAI-compatible endpoint
- `MODEL_NAME`: The model identifier to use
- `API_KEY`: Authentication token (default: "dockermodelrunner") - can be anything, OpenAI-compliant models need a value here

## Key Features

- **Pydantic AI Integration**: Type-safe LLM interactions with structured data handling
- **Streaming Responses**: Real-time text generation in the chat interface
- **Message History**: Maintains conversation context across requests
- **Error Handling**: Graceful error management and user feedback
- **Container Networking**: Proper host-to-container communication setup

## Architecture

```text
Host System:
├── Docker Model Runner (port 12434)
│   └── LLM Model (ai/smollm2:latest)
└── Docker Container:
    └── Python App + Streamlit (port 8501)
        └── Pydantic AI → OpenAI API → Model Runner
```

The Python application runs in a container but communicates with the LLM running on the host via Docker Model Runner's API endpoint.
