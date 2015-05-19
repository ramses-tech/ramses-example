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

## Login
POST `<host>/api/auth/login`

```json
{
    "login": "<config.system.user>",
    "password": "<config.system.password>"
}

```
or in the browser:
```
<host>/api/auth/login?_m=POST&login=<config.system.user>&password=<config.system.password>
```

## Add mock data
```
$ mkdir mock
$ curl -o mock/Users.json https://raw.githubusercontent.com/brandicted/nefertari-example/master/mock/Users.json
$ curl -o mock/Profiles.json https://raw.githubusercontent.com/brandicted/nefertari-example/master/mock/Profiles.json
$ curl -o mock/Stories.json https://raw.githubusercontent.com/brandicted/nefertari-example/master/mock/Stories.json
$ nefertari.post2api -f ./mock/Users.json -u http://localhost:6543/api/users
$ nefertari.post2api -f ./mock/Profiles.json -u http://localhost:6543/api/users/{username}/profile
$ nefertari.post2api -f ./mock/Stories.json -u http://localhost:6543/api/stories
```
NOTE: set auth = false in local.ini file before executing
