FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ARG SERVICE_NAME=api
ENV SERVICE_NAME=${SERVICE_NAME}
CMD ["sh", "-c", "if [ \"$SERVICE_NAME\" = \"worker\" ]; then python worker.py; else uvicorn main:app --host 0.0.0.0 --port 8000; fi"]
