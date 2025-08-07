# Use the official uv image with Python 3.12 pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set environment variables for uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Set working directory
WORKDIR /app

# Copy dependency files first to leverage Docker cache
COPY pyproject.toml uv.lock ./

# Install dependencies with cache mount for faster builds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# Copy the rest of the application
COPY . .

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Expose Streamlit default port
EXPOSE 8501

# Set the PATH to use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uv", "run", "main.py"]