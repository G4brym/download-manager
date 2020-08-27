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


## API Usage
#### Application status
To check if the application is running you can execute an `GET` to `/`, and you will get the following response:
```json
{
  "status": "ok",
  "downloads": 25
}
```

The `downloads` field corresponds to the count of all past and scheduled downloads.


#### Download files
To schedule a new download just make a `POST` request to `/api/v1/download?key=debug` with the following structure in the body.
```json
{
  "links": [
    {
      "url": "http://something.com/example.zip",
      "name": "output_file_name.zip",
      "path": "something/folder/",
      "headers": {
        "test": "header"
      }
    }
  ]
}
```

The only required field is the `url`.

If you dont provide a name, the name will be retrived from the url.
If you dont provide a path, the file will be placed in the root of the `complete` folder configured during
the application setup.

The response from the server will include an `id` field that you can use to check the download status.

The `id` field is calculated with md5 from the sum of the `path` + `name`.
The `path` and `name` are both sanitized before hash, to remove an initial `/` maybe giving as a mistake and
to make sure the path makes sense and there are not `folder//file` or `folderfile`.
If you try to get an id from the example above you should make an md5 from the string
`something/folder/output_file_name.zip` and the result should be `054047d9253e8461cdb70dccccccbb5c`.
```json
{
  "downloads": [
    {
      "hash": "054047d9253e8461cdb70dccccccbb5c",
      "name": "output_file_name.zip",
      "completed": true
    }
  ]
}
```

If the file already exists, the `completed` field will return the state of the previous file.


#### Download status
To check if a download is already finished just execute an `GET` to `/api/v1/download/<hash>`, and you will get the following response:
```json
{
  "hash": "054047d9253e8461cdb70dccccccbb5c",
  "name": "output_file_name.zip",
  "path": "something/folder/",
  "url": "http://something.com/example.zip",
  "failed": 0,
  "completed": true
}
```

The `failed` number corresponds to a given error id, following the next schema:
 1. Server error
 2. Problem reaching the server
 3. Local IO problems (maybe no disk space available)


#### Retry a single failed download 
To retry a single failed download send an `POST` to `/api/v1/download/<hash>`, and you will get the following response:
```json
{
  "status": "ok"
}
```


#### Retry all failed downloads
To retry all the failed and non completed downloads, just send a `POST` to `/api/v1/download/retry?key=debug`,
the server should respond with this:
```json
{
  "status": "ok"
}
```

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
