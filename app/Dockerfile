FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

EXPOSE 8501

ENV PATH="/app/.venv/bin:$PATH"

# CMD ["uv", "run", "basic.py"]
CMD ["uv", "run", "streamlit", "run", "chat.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
