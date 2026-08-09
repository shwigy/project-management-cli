"""User model: a Person who owns projects (one-to-many User -> Project)."""

from .person import Person


class User(Person):
    """A registered user of the tracker. Inherits identity from Person."""

    _next_id = 1
    _registry = {}

    def __init__(self, name, email=None, user_id=None):
        super().__init__(name, email)
        if user_id is None:
            user_id = User._next_id
            User._next_id += 1
        else:
            User._next_id = max(User._next_id, user_id + 1)
        self.user_id = user_id
        self.project_ids = []
        User._registry[self.user_id] = self

    def add_project(self, project):
        """Link a project to this user (one-to-many relationship)."""
        if project.project_id not in self.project_ids:
            self.project_ids.append(project.project_id)
        project.owner_id = self.user_id

    @classmethod
    def all(cls):
        """Return every registered user."""
        return list(cls._registry.values())

    @classmethod
    def find_by_name(cls, name):
        """Case-insensitive lookup of a user by name."""
        for user in cls._registry.values():
            if user.name.lower() == name.lower():
                return user
        return None

    @classmethod
    def find_by_id(cls, user_id):
        return cls._registry.get(user_id)

    @classmethod
    def reset(cls):
        """Clear the in-memory registry (used before loading from disk)."""
        cls._registry = {}
        cls._next_id = 1

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "project_ids": self.project_ids,
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(name=data["name"], email=data.get("email"), user_id=data["user_id"])
        user.project_ids = data.get("project_ids", [])
        return user

    def __str__(self):
        return f"[{self.user_id}] {self.name} <{self.email}> - {len(self.project_ids)} project(s)"

    def __repr__(self):
        return f"User(user_id={self.user_id!r}, name={self.name!r})"
