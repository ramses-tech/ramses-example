# `ramses-example`
Example of a Pyramid app using [ramses](https://github.com/brandicted/ramses)
    - example.raml: RAML specs
    - schemas/*.json: schemas and property definitions

## Installation
```
$ pip install -r requirements.txt
$ cp local.ini.template local.ini
$ nano local.ini
```
The setting `nefertari.engine` can be set to either `nefertari_mongodb` or `nefertari_sqla`

## Run
```
$ pserve local.ini
```

## Play
```
$ curl -XPOST ':8080/stories' -H 'Content-Type: application/json' -d '{"name":"New Story","description":"This is a new story"}'
$ curl ':8080/stories/1'
$ curl -XDELETE ':8080/stories/1'
```
