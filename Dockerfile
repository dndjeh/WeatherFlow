FROM python:3.10

WORKDIR /app

COPY producer.py . 
COPY consumer.py .
COPY .env .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt