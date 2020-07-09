# docker-download-manager
Simple download manager with API integration

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
To schedule a new download just make a `POST` request to `/api/v1/download` with the following structure in the body.
```json
{
  "links": [
    {
      "url": "http://something.com/example.zip",
      "name": "output_file_name.zip",
      "path": "something/folder/"
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
