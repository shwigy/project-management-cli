"""Base class for anyone tracked in the system."""


class Person:
    """Common identity fields shared by any human record (name + email)."""

    def __init__(self, name, email):
        self.name = name
        self.email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not str(value).strip():
            raise ValueError("name cannot be empty")
        self._name = str(value).strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if value and "@" not in str(value):
            raise ValueError(f"invalid email: {value!r}")
        self._email = value

    def __str__(self):
        return f"{self.name} <{self.email}>"
