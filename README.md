# Group Task Board

Independent SEG4105 Lab 8 application for assigning and completing group tasks.

## Group
- Ali, Almis
- Al-Khawaldeh, Yusuf
- Du, Jack
- Luu, Bryan
- Yatera, Mohamed

## Run locally
Requires Python 3.12. No third-party packages are needed.

```sh
python3 -m pip install -r requirements.txt
python3 -m taskboard.server
```

Open http://localhost:8080. The local database is stored in `data/tasks.db`.
Set `PORT` or `TASKBOARD_DB` to change these defaults.

## Tests
```sh
python3 -m unittest discover -s tests -v
```

This is a local teaching application. It has no authentication and should be
run on localhost, not exposed as a public multi-user service.
