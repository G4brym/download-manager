FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
LABEL maintainer="G4brym"

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./downloads /app/downloads
COPY ./main.py /app/
COPY ./schema.sql /app/
COPY ./prestart.sh /app/

ENV MAX_WORKERS=1
ENV PORT=8000

VOLUME /app/config
VOLUME /downloads
EXPOSE 8000
