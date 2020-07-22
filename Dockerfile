FROM lsiobase/alpine:3.11
LABEL maintainer="G4brym"

RUN \
 echo "**** install build packages ****" && \
 apk add --no-cache --upgrade --virtual=build-dependencies \
	curl \
	git \
	musl-dev \
	py3-pip \
	python3-dev \
	zlib-dev && \
 echo "**** install runtime packages ****" && \
 apk add --no-cache --upgrade \
	uwsgi \
	uwsgi-python && \
 echo "**** install download-manager ****"

 COPY . /app/downloads

 RUN echo "**** install pip packages ****" && \
 cd /app/downloads && \
 pip3 install --no-cache-dir -r requirements.txt && \
 echo "**** cleanup ****" && \
 apk del --purge \
	build-dependencies && \
 rm -rf \
	/root/.cache \
	/tmp/*

# copy local files
COPY root/ /

# ports and volumes
EXPOSE 8000
VOLUME /app/config
VOLUME /downloads
