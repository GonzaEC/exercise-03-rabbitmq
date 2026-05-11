FROM python:3.14-slim
WORKDIR /app
RUN pip install --no-cache-dir pika
RUN useradd -m appuser
USER appuser
COPY main.py .
CMD ["python", "main.py"]
