# Download Manager

## 1. Project Information's
This project is a file downloader and scheduler, just like [pyload](https://github.com/pyload/pyload), but it was build from
the start to be docker native and to have an api interface to schedule downloads automatically.

This project is using the [FastAPI](https://github.com/tiangolo/fastapi) framework, which automatically builds a swagger
documentation based on the api endpoints. This brings to this project a simple web interface that
also allows you to schedule downloads from your browser without having to make an api request using postman.

You can see an example of the [swagger documentation here](https://g4brym.github.io/docker-download-manager/).


## 2. Features
- Automatically download files to the local file system
- Portable (using docker)
- File download authentication using custom headers
- Schedule files using the Swagger interface
- Schedule files using the API
- Easy file identification (due to the custom hash function as primary key, see below)
- Automatically retry downloads (5 times by default, but can be edited in env vars)
- Manually retry files after all the automatically retries have failed
- Edit file download url or headers after you have scheduled it for download
- API authentication


### 2.1 File identification
This project doesn't use the typical incremental id for file identification because that would mean that the system
that is communicating with this api has to save that, in order to be able to check file status afterward.

Instead of that, we decided to use an MD5 hash of the file path + filename, this makes it much easier to
retry a download or check if it is already done without having to search by name or save the id of the download.
For reference everytime, you schedule a download the response will always have the file hash in case you want to save it
or compare it with your local hash.

This is also a good measure because it makes sure that we don't ever download the same file twice, because if you try to
schedule a new download using the same path and name, this project will only update the download url and headers of the
previous schedule.

### 2.2 File path's
Because this run's inside a docker container, when scheduling a new download, you should always use relative paths.
Then when saving the file we will append that to the downloads volume.


## 3. Usage
Here are some example snippets to help you get started creating a container.

### docker

```
docker create \
  --name=manager \
  --net=host \
  -e PUID=1000 \
  -e PGID=1000 \
  -e API_KEY=some_random_key \
  -v /path/to/config:/config \
  -v /path/to/downloads:/downloads \
  --restart unless-stopped \
  g4brym/download-manager
```


### docker-compose

Compatible with docker-compose v2 schemas.

```
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
      - /path/to/config:/config
      - /path/to/downloads:/downloads
    restart: unless-stopped
```


## 4. Parameters
Container images are configured using parameters passed at runtime (such as those above). These parameters are separated by a colon and indicate `<external>:<internal>` respectively. For example, `-p 8000:80` would expose port `80` from inside the container to be accessible from the host's IP on port `8000` outside the container.

| Parameter | Function |
| :----: | --- |
| `--net=host` | Use Host Networking |
| `-e PUID=1000` | for UserID - see below for explanation |
| `-e PGID=1000` | for GroupID - see below for explanation |
| `-e API_KEY=some_random_key` | Api key to interact with the server |
| `-e MAX_RETRIES=5` | This is the number of retries the project will try to automatically download a file |
| `-v /config` | Contains all configuration and generated files for the application to run, including the sqlite db |
| `-v /downloads` | Where your completed downloads should go |


## 5. User / Group Identifiers

When using volumes (`-v` flags) permissions issues can arise between the host OS and the container, we avoid this issue
by allowing you to specify the user `PUID` and group `PGID`.

Ensure any volume directories on the host are owned by the same user you specify and any permissions issues will vanish
like magic.

In this instance `PUID=1000` and `PGID=1000`, to find yours use `id user` as below:

```
  $ id username
    uid=1000(dockeruser) gid=1000(dockergroup) groups=1000(dockergroup)
```


## 6. API Documentation / Swagger UI
API Documentation is available in the OpenAPI format with Swagger UI
[Here](https://g4brym.github.io/docker-download-manager/)
