# `ramses-example`
Example of a Pyramid app using [ramses](https://github.com/brandicted/ramses)
    - example.raml: RAML specs
    - schemas/*.json: schemas and property definitions

## install
```
$ pip install -r requirements.txt
```

## run
```
$ pserve local.ini
```

## play
```
$ curl -XPOST ':8080/stories' -H 'Content-Type: application/json' -d '{"name":"New Story","description":"This is a new story"}'
$ curl ':8080/stories/1'
$ curl -XDELETE ':8080/stories/1'
```
