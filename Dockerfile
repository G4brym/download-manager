FROM python:3.6.8-alpine
LABEL maintainer="G4brym"

ENV DB_LOC=/config/db.sqlite3
ENV DOWNLOADS_PATH=/downloads

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir -m 777 /config
RUN mkdir -m 777 /downloads

RUN addgroup -S appgroup -g 1000 && adduser -S appuser -G appgroup -u 1000
USER appuser

COPY . .

VOLUME /config
VOLUME /downloads

EXPOSE 8000
CMD [ "gunicorn", "manager:app", "-b 0.0.0.0:8000" ]
