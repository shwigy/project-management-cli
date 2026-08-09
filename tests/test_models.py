import pytest

from src.models import User, Project, Task


@pytest.fixture(autouse=True)
def reset_registries():
    """Ensure each test starts with clean model registries."""
    User.reset()
    Project.reset()
    Task.reset()
    yield
    User.reset()
    Project.reset()
    Task.reset()


def test_create_user_assigns_incrementing_ids():
    alex = User(name="Alex", email="alex@example.com")
    sam = User(name="Sam", email="sam@example.com")
    assert alex.user_id == 1
    assert sam.user_id == 2


def test_user_rejects_invalid_email():
    with pytest.raises(ValueError):
        User(name="Bad", email="not-an-email")


def test_user_rejects_empty_name():
    with pytest.raises(ValueError):
        User(name="   ", email="a@b.com")


def test_user_find_by_name_is_case_insensitive():
    User(name="Alex", email="alex@example.com")
    assert User.find_by_name("ALEX") is not None
    assert User.find_by_name("missing") is None


def test_add_project_links_user_and_project():
    alex = User(name="Alex", email="alex@example.com")
    project = Project(title="CLI Tool", owner_id=None)
    alex.add_project(project)
    assert project.project_id in alex.project_ids
    assert project.owner_id == alex.user_id
    assert Project.for_user(alex.user_id) == [project]


def test_project_rejects_empty_title():
    with pytest.raises(ValueError):
        Project(title="", owner_id=1)


def test_add_task_links_task_to_project():
    project = Project(title="CLI Tool", owner_id=1)
    task = Task(title="Write docs", project_id=None)
    project.add_task(task)
    assert task.task_id in project.task_ids
    assert task.project_id == project.project_id
    assert Task.for_project(project.project_id) == [task]


def test_task_default_status_is_pending():
    task = Task(title="Write docs", project_id=1)
    assert task.status == "pending"


def test_task_mark_complete():
    task = Task(title="Write docs", project_id=1)
    task.mark_complete()
    assert task.status == "complete"


def test_task_rejects_invalid_status():
    with pytest.raises(ValueError):
        Task(title="Write docs", project_id=1, status="bogus")


def test_user_to_dict_and_from_dict_round_trip():
    alex = User(name="Alex", email="alex@example.com")
    data = alex.to_dict()
    User.reset()
    restored = User.from_dict(data)
    assert restored.name == "Alex"
    assert restored.user_id == data["user_id"]
