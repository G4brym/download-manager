FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10
LABEL maintainer="G4brym"

RUN apk add --no-cache su-exec bash gcc build-base

RUN addgroup -g 1000 webapp \
  && adduser -Ss /bin/false -u 1000 -G webapp -h /home/webapp webapp \
  && mkdir -m 777 /downloads && mkdir -m 777 /config \
  && chown webapp:webapp /config /app /downloads /home/webapp

VOLUME /config
VOLUME /downloads
WORKDIR /app
EXPOSE 8000

ENV PUID=1000 PGID=1000 \
    MAX_WORKERS=1 \
    WEB_CONCURRENCY=1 \
    PORT=8000 \
    ENVIRONMENT="PROD" \
    DATABASE_PATH="/config/db.sqlite3" \
    DOWNLOADS_PATH="/downloads"

RUN pip install -U setuptools pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
RUN make dev

RUN dos2unix /app/prestart.sh && chmod +x /app/prestart.sh
RUN dos2unix /app/start.sh && chmod +x /app/start.sh

ENTRYPOINT [ "/app/prestart.sh" ]
