FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8000

# Env vars will come from docker-compose or runtime
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["./entrypoint.sh"]
