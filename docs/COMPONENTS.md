# Software Components

## 1. Component Inventory
| Component / Module | Directory / File Path | Primary Responsibility | Key Dependencies |
| :--- | :--- | :--- | :--- |
| HTTP entry point | `taskboard/server.py` | Routes requests, parses form data, enforces a 4096-byte body limit, returns HTTP responses | `http.server`, `urllib.parse`, TaskService, TaskStore, views |
| Presentation | `taskboard/views.py` | Renders the task form and task list; escapes user-provided HTML | `html.escape`, group roster from service |
| Core task service | `taskboard/service.py` | Validates titles and assignees; handles completion and missing tasks | TaskStore |
| Data storage | `taskboard/storage.py` | Creates the schema; lists, inserts and updates tasks with parameterized SQL | `sqlite3`, `pathlib` |
| Package | `taskboard/__init__.py` | Defines the independent taskboard Python package | Python 3.12 |
| Tests | `tests/test_taskboard.py` | Verifies persistence, validation, completion, HTML escaping and HTTP behavior | `unittest`, temporary SQLite files, local HTTP server |
| Continuous integration | `.github/workflows/tests.yml` | Runs the tests on pushes and pull requests | GitHub Actions, Python 3.12 |
| Dependency manifest | `requirements.txt` | Records that no third-party packages are required | Python standard library |

## 2. External Interfaces & APIs
- `GET /`: HTML task form and current task list.
- `POST /tasks`: form fields `title` and `assignee`; returns 303 to `/` after creation, or 400 for invalid input.
- `POST /tasks/<id>/complete`: marks an existing task complete; returns 303, or 404 for a missing task.
- `GET /api/tasks`: JSON array of tasks (`id`, `title`, `assignee`, `done`).
- `GET /health`: JSON `{"status":"ok","application":"group-task-board"}`.
- Unknown routes return 404. Bodies larger than 4096 bytes return 413.
- Environment: `PORT` defaults to `8080`; `TASKBOARD_DB` defaults to `data/tasks.db` locally.
- Output: HTML/JSON responses, SQLite writes and HTTP access logs on stderr.
- Database: `tasks(id INTEGER PRIMARY KEY, title TEXT, assignee TEXT, done INTEGER)`.
