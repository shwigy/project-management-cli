"""Command implementations for the project management CLI.

Each function takes the parsed argparse namespace, mutates the in-memory
model registries, and (for write commands) persists via save_data().
"""

from rich.console import Console
from rich.table import Table

from src.models import User, Project, Task
from src.utils.storage import save_data
from src.utils.dates import parse_due_date

console = Console()


def add_user(args):
    if User.find_by_name(args.name):
        console.print(f"[red]User '{args.name}' already exists.[/red]")
        return
    user = User(name=args.name, email=args.email)
    save_data()
    console.print(f"[green]Created user:[/green] {user}")


def list_users(args):
    users = User.all()
    if not users:
        console.print("[yellow]No users yet.[/yellow]")
        return
    table = Table(title="Users")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Email")
    table.add_column("Projects")
    for user in users:
        table.add_row(str(user.user_id), user.name, user.email or "-", str(len(user.project_ids)))
    console.print(table)


def add_project(args):
    owner = User.find_by_name(args.user)
    if not owner:
        console.print(f"[red]No such user: {args.user}[/red]")
        return
    if Project.find_by_title(args.title):
        console.print(f"[red]Project '{args.title}' already exists.[/red]")
        return
    try:
        due_date = parse_due_date(args.due_date)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        return
    project = Project(
        title=args.title,
        owner_id=owner.user_id,
        description=args.description or "",
        due_date=due_date,
    )
    owner.add_project(project)
    save_data()
    console.print(f"[green]Created project:[/green] {project} for {owner.name}")


def list_projects(args):
    if args.user:
        owner = User.find_by_name(args.user)
        if not owner:
            console.print(f"[red]No such user: {args.user}[/red]")
            return
        projects = Project.for_user(owner.user_id)
        title = f"Projects for {owner.name}"
    else:
        projects = Project.all()
        title = "All Projects"

    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return

    table = Table(title=title)
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Owner")
    table.add_column("Due")
    table.add_column("Tasks")
    for project in projects:
        owner = User.find_by_id(project.owner_id)
        table.add_row(
            str(project.project_id),
            project.title,
            owner.name if owner else "-",
            project.due_date or "-",
            str(len(project.task_ids)),
        )
    console.print(table)


def add_task(args):
    project = Project.find_by_title(args.project)
    if not project:
        console.print(f"[red]No such project: {args.project}[/red]")
        return
    task = Task(title=args.title, project_id=project.project_id, assigned_to=args.assigned_to)
    project.add_task(task)
    save_data()
    console.print(f"[green]Created task:[/green] {task} in {project.title}")


def list_tasks(args):
    project = Project.find_by_title(args.project)
    if not project:
        console.print(f"[red]No such project: {args.project}[/red]")
        return
    tasks = Task.for_project(project.project_id)
    if not tasks:
        console.print("[yellow]No tasks for this project.[/yellow]")
        return
    table = Table(title=f"Tasks for {project.title}")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Status")
    table.add_column("Assigned To")
    for task in tasks:
        table.add_row(str(task.task_id), task.title, task.status, task.assigned_to or "-")
    console.print(table)


def complete_task(args):
    task = Task.find_by_id(args.task_id)
    if not task:
        console.print(f"[red]No such task id: {args.task_id}[/red]")
        return
    task.mark_complete()
    save_data()
    console.print(f"[green]Marked complete:[/green] {task}")
