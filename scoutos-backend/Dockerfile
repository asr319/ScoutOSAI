FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Optional auto-reload can be enabled by setting UVICORN_RELOAD="--reload" at runtime
ENV UVICORN_RELOAD=""
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 $UVICORN_RELOAD"]
