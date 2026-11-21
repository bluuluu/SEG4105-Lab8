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

## Documentation
- [Software Components](docs/COMPONENTS.md)
- [System Architecture](docs/ARCHITECTURE.md)
- [Development Methodology](docs/METHODOLOGY.md)

## Docker
```sh
docker build -t group-task-board:1.0 .
docker run --rm -p 127.0.0.1:8088:8080 group-task-board:1.0
```
Open http://localhost:8088. Port 8088 avoids an existing local service on 8080.

Published image:
```sh
docker run --rm -p 127.0.0.1:8088:8080 bryanluu123/seg4105-lab8:latest
```

For persistent task data, add `-v lab8-task-data:/app/data` to the run command.
The image runs as UID 10001. It contains no accounts, credentials or saved tasks.

## Git workflow used in the lab
- `feature/add-documentation`: initial README, reviewed and merged via PR.
- `docs/architecture-and-methodology`: three technical documents and README index.
- Linked documentation issue closed automatically through the second merged PR.

## Lab report and evidence
- [Lab 8 report (PDF)](docs/SEG4105%20-%20Lab%208.pdf)
- [Commands](docs/LAB_COMMANDS.txt)
- [Screenshots](docs/screenshots/)
