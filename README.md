# Project Management CLI

A command-line tool for managing users, projects, and tasks — built for the
Summative Lab on Python CLI applications. Supports creating users, assigning
them projects, adding tasks to projects, and persisting everything to a local
JSON file between runs.

## Features

- **Users**: create and list users (name + email).
- **Projects**: create projects owned by a user, with a description and due
  date; list all projects or filter by owner.
- **Tasks**: add tasks to a project, optionally assigned to a contributor;
  list tasks per project; mark tasks complete.
- **Relationships**: one-to-many User → Project, one-to-many Project → Task,
  with tasks additionally carrying an `assigned_to` contributor (many-to-many
  in spirit — a project can have tasks assigned across multiple people).
- **Persistence**: all data is saved to `data/data.json` after every write
  command and reloaded automatically on startup. Missing or corrupt data
  files are handled gracefully (treated as empty).
- **Pretty output**: tables rendered with [rich](https://github.com/Textualize/rich).
- **Flexible due dates**: due dates accept natural formats ("Sept 1 2026",
  "09/01/2026", "2026-09-01") via [python-dateutil](https://dateutil.readthedocs.io/),
  normalized to `YYYY-MM-DD` for storage.

## Setup

Requires Python 3.8+. Dependencies are managed with [Pipenv](https://pipenv.pypa.io/):

```bash
pipenv install --dev
pipenv shell
```

A plain `requirements.txt` is also included if you'd rather use a standard
virtualenv:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running CLI commands

All commands are run through `main.py`.

```bash
# Users
python3 main.py add-user --name "Alex" --email "alex@example.com"
python3 main.py list-users

# Projects
python3 main.py add-project --user "Alex" --title "CLI Tool" --description "Build the CLI" --due-date 2026-09-01
python3 main.py list-projects
python3 main.py list-projects --user "Alex"

# Tasks
python3 main.py add-task --project "CLI Tool" --title "Implement add-task" --assigned-to "Alex"
python3 main.py list-tasks --project "CLI Tool"
python3 main.py complete-task --task-id 1
```

Run `python3 main.py --help` or `python3 main.py <command> --help` for full
option details.

## Project structure

```
main.py              # CLI entry point
src/
  models/             # Person, User, Project, Task classes
  cli/                # argparse setup (parser.py) and command handlers (commands.py)
  utils/               # storage.py (JSON I/O), dates.py (due-date validation)
data/data.json        # persisted users/projects/tasks
tests/                 # pytest unit tests for models, storage, and CLI commands
Pipfile / Pipfile.lock # dependency management
requirements.txt       # plain-pip fallback
```

## Design notes

- `Person` is a lightweight base class for shared name/email fields; `User`
  inherits from it.
- Each model keeps a class-level registry (`_registry`) and auto-incrementing
  ID counter, with `all()`, `find_by_id()`, and similar lookup classmethods.
- `name`/`email`/`title`/`status` are exposed via `@property` with validation
  in the setters (e.g. a `Task.status` must be one of `pending`,
  `in-progress`, `complete`).
- `to_dict()` / `from_dict()` on each model handle JSON serialization.

## Testing

```bash
python3 -m pytest -q
```

Tests cover model validation and relationships, JSON save/load round-tripping
(including missing/malformed file handling), and CLI command behavior using
mocked argparse namespaces.

## Known issues / limitations

- Lookups by name/title are case-insensitive but must be exact matches (no
  fuzzy search).
- No CLI commands to edit/delete users, projects, or tasks — only create,
  list, and complete-task.
- Single flat JSON file with no concurrent-write protection; fine for a
  single-user CLI, not for concurrent access.
