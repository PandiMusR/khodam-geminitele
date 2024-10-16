FROM --platform=$BUILDPLATFORM python:3.10-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM --platform=$TARGETPLATFORM python:3.10-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY . .

RUN useradd -m pythun
USER pythun

CMD ["python", "main.py"]
