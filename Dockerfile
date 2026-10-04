FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=/opt/venv PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-default-groups --group service

COPY exchange ./exchange
COPY trainer ./trainer
EXPOSE 8000
CMD ["uvicorn", "exchange.main:app", "--host", "0.0.0.0", "--port", "8000"]
