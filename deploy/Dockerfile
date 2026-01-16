# 1. Используем официальный образ Python
FROM python:3.12

WORKDIR /app
RUN pip install --no-cache-dir uv

COPY pyproject.toml .
COPY uv.lock .

# Аргумент, который определяет, нужно ли устанавливать тесты
ARG INSTALL_TESTS=false

# Синхронизируем зависимости: 
# Если INSTALL_TESTS=true, устанавливаем и основную группу, и группу tests
RUN if [ "$INSTALL_TESTS" = "true" ] ; then \
    uv sync --frozen --group tests ; \
    else \
    uv sync --frozen ; \
    fi

COPY alembic.ini .
COPY pytest.ini .
COPY src/ ./src/
COPY migrations/ ./migrations/

# Добавляем путь к установленным библиотекам в PATH
ENV PATH="/app/.venv/bin:$PATH"

RUN uv pip install --no-cache --system -e .

# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8010"]
