# ESTÁGIO 1: BUILDER
FROM python:3.9 as builder

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /venv && \
    /venv/bin/pip install --no-cache-dir --upgrade pip && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

# ESTÁGIO 2: FINAL
FROM python:3.9-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /venv /venv

COPY . .

# Usuário não-root
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# PATH para o venv
ENV PATH="/venv/bin:$PATH"

# Comando padrão para desenvolvimento (reload)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/app"]
