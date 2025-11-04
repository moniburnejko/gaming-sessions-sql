## contributing to gaming sessions sql
thanks for your interest in contributing! this project showcases a complete analytics workflow with python, sql (PostgreSQL), and visualization.

### ways to contribute
- report bugs using the bug report issue template
- propose features using the feature request issue template
- improve documentation
- add tests or refactor code
- enhance sql models/queries or python data generation/analysis

### getting started (local development)
prerequisites:
- python 3.10+
- postgreSQL 13+ (local or container)
- git

recommended tools:
- virtualenv or uv/poetry
- black and ruff for python formatting/linting

setup:
1. fork and clone the repository.
2. create and activate a virtual environment.
3. install dependencies:
   - `pip install -r requirements.txt`
4. configure database access via environment variables, e.g.:
   - `DATABASE_URL=postgresql://user:password@localhost:5432/gaming`
5. run scripts/notebooks as documented in the repo to reproduce datasets, queries, and visuals.

### style guide
python:
- use black for formatting and ruff for linting where available.
- prefer type hints and docstrings.

sql (PostgreSQL):
- uppercase keywords (SELECT, FROM, WHERE).
- snake_case for identifiers (tables, columns).
- use CTEs for readability; avoid deeply nested subqueries when a CTE helps clarity.
- add comments for non-trivial logic.

commits:
- use clear, imperative messages (e.g., “Add session cohort retention query”).
- conventional commits (feat, fix, docs, refactor, chore) are welcome but not required.

branches and PRs:
- create feature branches from the default branch (e.g., `feat/<short-desc>` or `chore/<short-desc>`).
- keep PRs focused and small when possible.
- include tests or sample data updates when relevant.
- fill out the PR template completely.

### testing
- include unit or integration tests where sensible (python-side).
- for sql changes, include example queries, expected outputs, or explain plans if performance-sensitive.

### reporting security issues
please do not open public issues for security concerns. contact the maintainer privately if possible; if unsure, open an issue with minimal details and request a private follow-up.

### code of conduct
by participating, you agree to abide by our [code of conduct](./code_of_conduct.md).
