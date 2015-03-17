# ramses-example
Example of a Pyramid app that uses [ramses](https://github.com/brandicted/ramses)

    - example.raml: RAML specs
    - schemas/*.json: schemas w/ property definitions

## install
```
$ pip install -r requirements.prod .
```

## run
```
$ pserve local.ini
```

## play

### POST
```
$ curl -XPOST ':8080/stories' -H 'Content-Type: application/json' -d '{"name":"New Story","description":"This is a new story"}'
```

### GET
```
$ curl ':8080/stories/1'
```

### DELETE
```
$ curl -XDELETE ':8080/stories/1'
```
