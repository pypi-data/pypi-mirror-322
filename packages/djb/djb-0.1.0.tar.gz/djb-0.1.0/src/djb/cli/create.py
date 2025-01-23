import re
import readline  # noqa
import subprocess
import sys
from pathlib import Path

import click

from djb.cli.constants import TEMPLATE_REPO_URL, ERR, FAI, NXT, OBS, SUC


# RFC 1123 regex to validate that a project name is compatible with k8s.
RFC_1123_REGEX = r"^(?!-)[a-z0-9-]{1,63}(?<!-)(\.(?!-)[a-z0-9-]{1,63}(?<!-))*$"

PROJECT_NAME_REQUIREMENTS = """\b
For the project name to be compatible with a wide range of tools, it must
follow the DNS label standard as defined by RFC 1123:
\b
- contain at most 63 characters
- contain only lowercase alphanumeric characters or '-'
- start with an alphanumeric character
- end with an alphanumeric character
"""

PROJECT_DOCSTRING = f"""
Create a new djb project.

Prompts you for a project name, unless provided via --project-name.

The project is created in a new directory with the given name.

{PROJECT_NAME_REQUIREMENTS}
"""


def validate_project_name(name):
    """
    Validate input against RFC 1123 hostname rules.
    """
    if not re.match(RFC_1123_REGEX, name):
        raise click.BadParameter(
            f"'{name}' is not a valid project name.\n{PROJECT_NAME_REQUIREMENTS}"
        )
    return name


def readline_prompt(prompt, validator, max_retries=3):
    for _ in range(max_retries):
        print(prompt, file=sys.stderr, end=":\n", flush=True)
        user_input = input("> ")
        try:
            return validator(user_input)
        except click.BadParameter as e:
            print(f"{ERR} {e}", file=sys.stderr)
    raise click.ClickException(f"{FAI} Maximum retries exceeded.")


@click.command(help=PROJECT_DOCSTRING)
@click.option("--project-name", help="The name of your project.")
@click.option(
    "-r",
    "--template-repo-url",
    default=TEMPLATE_REPO_URL,
    show_default=True,
    help="Git repository URL for the djb project template.",
)
@click.option(
    "-w",
    "--write-project-path-file",
    type=click.File("w"),
    help="Write project path to this file.",
)
def create(project_name, template_repo_url, write_project_path_file):
    # TODO: Warn if we are already inside a djb project.

    # Welcome!
    click.echo("Welcome to djb!\n")
    click.echo("This script will create a new djb project.\n")
    click.echo("Let's get started!\n")

    # Prompt for project_name if it is not provided.
    if project_name:
        validate_project_name(project_name)
    else:
        project_name = readline_prompt(
            "Please enter your project name", validate_project_name
        )

    # Create project directory.
    project_path = Path(project_name)
    if project_path.exists():
        click.echo(
            f"{OBS} The directory '{project_name}' already exists. Using the existing directory."
        )
    else:
        project_path.mkdir(parents=True)
        click.echo(f"{SUC} Created project directory.")

    # Clone djb project template.
    try:
        click.echo(
            f"{NXT} Cloning repository from '{template_repo_url}' into '{project_path}'..."
        )
        subprocess.run(["git", "clone", template_repo_url, project_path], check=True)
        click.echo(f"{SUC} Repository cloned.")
    except Exception as e:
        click.echo(f"{ERR} Failed to clone repository. {e}")

    # If given a file, write the project path to it.
    if write_project_path_file:
        write_project_path_file.write(str(project_path))


if __name__ == "__main__":
    create()
