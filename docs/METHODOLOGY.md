# Development Methodology

## 1. Software Development Lifecycle (SDLC)
- Framework: iterative incremental development with a Kanban-style task flow.
- Planning & Tracking: create a GitHub Issue with acceptance criteria; move work through To do, In progress, Review and Done. A Project board is an optional visual view, not a prerequisite to the lab workflow.
- Deliver a small verified increment before taking the next task. Review changes and record follow-up work in Issues.

## 2. Version Control & Branching Strategy
- Workflow: GitHub Flow.
- `main`: verified, runnable source.
- `feature/*`, `fix/*`, `docs/*`: short-lived branches from current main.
- The lab branches are `feature/add-documentation` and `docs/architecture-and-methodology`.
- Commit convention: short plain-language descriptions of the completed action, for example `Wrote documentation`, `Fixed task validation`, or `Took screenshots of lab steps`.
- Push a branch, open a pull request, inspect its diff and test results, merge, pull main, then delete the merged branch.

## 3. Code Review & Definition of Done (DoD)
1. The application starts and its affected workflow works locally.
2. `python3 -m unittest discover -s tests -v` passes.
3. README and affected documentation match the implementation.
4. The pull request diff is reviewed before merging. Group development should obtain another member's review when available; do not claim a review that was not actually performed.
5. No credentials, local database files, caches or generated logs are committed.
6. For image changes, build the container and verify its health endpoint and task workflow.

## 4. Testing & Quality Assurance Strategy
- Unit tests: Python `unittest` verifies title/assignee validation, missing IDs, HTML escaping and SQLite persistence/completion. Focus on these behaviors rather than an unmeasured coverage percentage.
- HTTP integration test: a temporary database and a loopback HTTP server verify health, task creation, completion, invalid input and missing routes.
- CI: GitHub Actions runs the same tests on pushes and pull requests with Python 3.12.
- System test: run the image on a free localhost port, check `/health`, add a task, complete it and inspect `/api/tasks`.
- Portability: publish `1.0` and `latest`, remove the lab image tags, pull the remote image and repeat the health/task checks.
- Evidence: capture real Terminal, GitHub, application and Docker Hub results for the report.
