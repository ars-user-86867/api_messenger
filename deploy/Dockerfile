# 1. Используем официальный образ Python
FROM python:3.12

WORKDIR /app
RUN pip install --no-cache-dir uv

COPY pyproject.toml .
COPY alembic.ini .
COPY src/ ./src/
COPY migrations/ ./migrations/

RUN uv pip install --no-cache --system -e .

# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8010"]
