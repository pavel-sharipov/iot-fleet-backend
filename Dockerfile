# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

WORKDIR /app

# Runtime env (good defaults)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# ---------- Production image ----------
FROM base AS prod
COPY app /app/app
COPY tests /app/tests

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
