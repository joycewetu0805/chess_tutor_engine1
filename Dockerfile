#
# Multi-stage build:
# 1) Build the Vite frontend
# 2) Run the FastAPI backend and serve the built frontend as static files
#

FROM node:22-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build


FROM python:3.12-slim AS backend
WORKDIR /app/backend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./

# Copy built frontend into backend so FastAPI can serve it.
RUN mkdir -p /app/backend/app/static
COPY --from=frontend-builder /app/frontend/dist/ /app/backend/app/static/

EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

