FROM python:3.10
WORKDIR /app
COPY test2.py /app
COPY .env /app
RUN pip install kafka-python requests python-dotenv
CMD ["python", "test2.py"]