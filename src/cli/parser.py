"""argparse CLI structure for the project management tool."""

import argparse

from src.cli import commands


def build_parser():
    parser = argparse.ArgumentParser(
        prog="pmcli",
        description="A simple multi-user project & task tracker.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_add_user = subparsers.add_parser("add-user", help="Create a new user")
    p_add_user.add_argument("--name", required=True)
    p_add_user.add_argument("--email", required=False)
    p_add_user.set_defaults(func=commands.add_user)

    p_list_users = subparsers.add_parser("list-users", help="List all users")
    p_list_users.set_defaults(func=commands.list_users)

    p_add_project = subparsers.add_parser("add-project", help="Create a project for a user")
    p_add_project.add_argument("--user", required=True, help="Owner's name")
    p_add_project.add_argument("--title", required=True)
    p_add_project.add_argument("--description", required=False, default="")
    p_add_project.add_argument("--due-date", dest="due_date", required=False, help="YYYY-MM-DD")
    p_add_project.set_defaults(func=commands.add_project)

    p_list_projects = subparsers.add_parser("list-projects", help="List projects")
    p_list_projects.add_argument("--user", required=False, help="Filter by owner's name")
    p_list_projects.set_defaults(func=commands.list_projects)

    p_add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    p_add_task.add_argument("--project", required=True, help="Project title")
    p_add_task.add_argument("--title", required=True)
    p_add_task.add_argument("--assigned-to", dest="assigned_to", required=False)
    p_add_task.set_defaults(func=commands.add_task)

    p_list_tasks = subparsers.add_parser("list-tasks", help="List tasks for a project")
    p_list_tasks.add_argument("--project", required=True, help="Project title")
    p_list_tasks.set_defaults(func=commands.list_tasks)

    p_complete_task = subparsers.add_parser("complete-task", help="Mark a task complete")
    p_complete_task.add_argument("--task-id", dest="task_id", type=int, required=True)
    p_complete_task.set_defaults(func=commands.complete_task)

    return parser
