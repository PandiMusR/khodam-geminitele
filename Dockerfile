FROM python:3.10-slim

RUN apt-get update && apt-get install -y gcc build-essential python3-dev libgrpc-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD ["python", "main.py"]