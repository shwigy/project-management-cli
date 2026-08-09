"""Task model: belongs to one Project, optionally assigned to a contributor."""

VALID_STATUSES = ("pending", "in-progress", "complete")


class Task:
    """A unit of work within a project. Many-to-many with contributors via assigned_to."""

    _next_id = 1
    _registry = {}

    def __init__(self, title, project_id, assigned_to=None, status="pending", task_id=None):
        if task_id is None:
            task_id = Task._next_id
            Task._next_id += 1
        else:
            Task._next_id = max(Task._next_id, task_id + 1)
        self.task_id = task_id
        self.title = title
        self.project_id = project_id
        self.assigned_to = assigned_to
        self.status = status
        Task._registry[self.task_id] = self

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in VALID_STATUSES:
            raise ValueError(f"status must be one of {VALID_STATUSES}, got {value!r}")
        self._status = value

    def mark_complete(self):
        """Convenience method to flip status to complete."""
        self.status = "complete"

    @classmethod
    def all(cls):
        return list(cls._registry.values())

    @classmethod
    def find_by_id(cls, task_id):
        return cls._registry.get(task_id)

    @classmethod
    def for_project(cls, project_id):
        """All tasks belonging to a given project id."""
        return [t for t in cls._registry.values() if t.project_id == project_id]

    @classmethod
    def reset(cls):
        cls._registry = {}
        cls._next_id = 1

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "project_id": self.project_id,
            "assigned_to": self.assigned_to,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            project_id=data.get("project_id"),
            assigned_to=data.get("assigned_to"),
            status=data.get("status", "pending"),
            task_id=data["task_id"],
        )

    def __str__(self):
        assignee = f" (assigned: {self.assigned_to})" if self.assigned_to else ""
        return f"[{self.task_id}] {self.title} - {self.status}{assignee}"

    def __repr__(self):
        return f"Task(task_id={self.task_id!r}, title={self.title!r}, status={self.status!r})"
