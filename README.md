# docker-download-manager
Simple download manager with API integration

## API Usage
##### Application status
To check if the application is running you can execute an `GET` to `/`, and you will get the following response:
```json
{
  "status": "ok"
}
```


##### Download files
To schedule a new download just make a `POST` request to `/api/v1/download` with the following structure in the body.
```json
{
  "links": [
    {
      "url": "http://something.com/example.zip",
      "name": "output_file_name.zip",
      "path": "/something/folder/"
    },
    ...
  ]
}
```

The only required field is the `url`.

If you dont provide a name, the name will be retrived from the url.
If you dont provide a path, the file will be placed in the root of the `complete` folder configured during
the application setup.

The response from the server will include an `id` field that you can use to check the download status.

The `id` field is calculated with md5 from the sum of the `path` + `name`.
If you try to get an id from the example above you should make an md5 from the string
`/something/folder/output_file_name.zip` and the result should be `039a920b4bd95396b38d3dc85263ebf9`.
```json
{
  "downloads": [
    {
      "id": "039a920b4bd95396b38d3dc85263ebf9",
      "name": "output_file_name.zip",
      "completed": false
    },
    ...
  ]
}
```

If the file already exists, the `completed` field will return the state of the previous file.


##### Download status
To check if a download is already finished just execute an `GET` to `/api/v1/status/{id}`, and you will get the following response:
```json
{
  "id": "039a920b4bd95396b38d3dc85263ebf9",
  "name": "output_file_name.zip",
  "completed": true
}
```
