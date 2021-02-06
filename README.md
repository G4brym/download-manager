# docker-download-manager
Simple download manager with API integration

## Usage
Here are some example snippets to help you get started creating a container.

### docker

```
docker create \
  --name=manager \
  --net=host \
  -e PUID=1000 \
  -e PGID=1000 \
  -e API_KEY=some_random_key \
  -v /path/to/config:/app/config \
  -v /path/to/downloads:/downloads \
  --restart unless-stopped \
  g4brym/download-manager
```


### docker-compose

Compatible with docker-compose v2 schemas.

```
---
version: "2.1"
services:
  manager:
    image: g4brym/download-manager
    container_name: manager
    network_mode: host
    environment:
      - PUID=1000
      - PGID=1000
      - API_KEY=some_random_key
    volumes:
      - /path/to/config:/app/config
      - /path/to/downloads:/downloads
    restart: unless-stopped
```


## Parameters
Container images are configured using parameters passed at runtime (such as those above). These parameters are separated by a colon and indicate `<external>:<internal>` respectively. For example, `-p 8000:80` would expose port `80` from inside the container to be accessible from the host's IP on port `8000` outside the container.

| Parameter | Function |
| :----: | --- |
| `--net=host` | Use Host Networking |
| `-e PUID=1000` | for UserID - see below for explanation |
| `-e PGID=1000` | for GroupID - see below for explanation |
| `-e API_KEY=some_random_key` | Api key to interact with the server |
| `-v /app/config` | Contains all configuration and generated files for the application to run, including the sqlite db |
| `-v /downloads` | Where your completed downloads should go |


## User / Group Identifiers

When using volumes (`-v` flags) permissions issues can arise between the host OS and the container, we avoid this issue by allowing you to specify the user `PUID` and group `PGID`.

Ensure any volume directories on the host are owned by the same user you specify and any permissions issues will vanish like magic.

In this instance `PUID=1000` and `PGID=1000`, to find yours use `id user` as below:

```
  $ id username
    uid=1000(dockeruser) gid=1000(dockergroup) groups=1000(dockergroup)
```


## API Documentation / Swagger UI
API Documentation is available in the OpenAPI format with Swagger UI
[Here](https://g4brym.github.io/docker-download-manager/)


### Docker hub build commands
```bash
docker build --tag download-manager:latest .
docker tag download-manager:latest g4brym/download-manager:latest
docker push g4brym/download-manager:latest 
```

## Credits

The base image for this docker application is provided by the [Linuxserver.io](https://www.linuxserver.io/),
especially a modified version of the [alpine docker image](https://github.com/linuxserver/docker-baseimage-alpine).

This readme file is also based on the work of the [Linuxserver.io](https://www.linuxserver.io/).
