FROM python:3.12-slim
WORKDIR /app
COPY pip install --no-cache-dir -r requirements.txt
COPY hello.py .
CMD ["python", "hello.py"]