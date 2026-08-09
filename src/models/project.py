"""Project model: belongs to one User, has many Tasks."""


class Project:
    """A project owned by a user, containing zero or more tasks."""

    _next_id = 1
    _registry = {}

    def __init__(self, title, owner_id, description="", due_date=None, project_id=None):
        if project_id is None:
            project_id = Project._next_id
            Project._next_id += 1
        else:
            Project._next_id = max(Project._next_id, project_id + 1)
        self.project_id = project_id
        self.title = title
        self.owner_id = owner_id
        self.description = description
        self.due_date = due_date
        self.task_ids = []
        Project._registry[self.project_id] = self

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not str(value).strip():
            raise ValueError("title cannot be empty")
        self._title = str(value).strip()

    def add_task(self, task):
        """Link a task to this project (one-to-many relationship)."""
        if task.task_id not in self.task_ids:
            self.task_ids.append(task.task_id)
        task.project_id = self.project_id

    @classmethod
    def all(cls):
        return list(cls._registry.values())

    @classmethod
    def find_by_title(cls, title):
        """Case-insensitive lookup of a project by title."""
        for project in cls._registry.values():
            if project.title.lower() == title.lower():
                return project
        return None

    @classmethod
    def find_by_id(cls, project_id):
        return cls._registry.get(project_id)

    @classmethod
    def for_user(cls, user_id):
        """All projects owned by a given user id."""
        return [p for p in cls._registry.values() if p.owner_id == user_id]

    @classmethod
    def reset(cls):
        cls._registry = {}
        cls._next_id = 1

    def to_dict(self):
        return {
            "project_id": self.project_id,
            "title": self.title,
            "owner_id": self.owner_id,
            "description": self.description,
            "due_date": self.due_date,
            "task_ids": self.task_ids,
        }

    @classmethod
    def from_dict(cls, data):
        project = cls(
            title=data["title"],
            owner_id=data.get("owner_id"),
            description=data.get("description", ""),
            due_date=data.get("due_date"),
            project_id=data["project_id"],
        )
        project.task_ids = data.get("task_ids", [])
        return project

    def __str__(self):
        due = f", due {self.due_date}" if self.due_date else ""
        return f"[{self.project_id}] {self.title}{due} - {len(self.task_ids)} task(s)"

    def __repr__(self):
        return f"Project(project_id={self.project_id!r}, title={self.title!r})"
