import os
from pathlib import Path

import click

from djb.cli.constants import ERR, SUC


@click.command()
@click.option(
    "--project-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True),
    default=os.getenv("DJB_PROJECT_DIR", "."),
    show_default=True,
    help="Path to your djb project.",
)
def djbrc(project_path):
    """
    Update `.djbrc` script based on the project's current state.

    Tip: It's best to run `djb djbrc` as `djb djbrc && source .djbrc` to ensure
    that your shell environment reflects any changes.
    """
    click.echo("→ Updating .djbrc...")
    project_dir = Path(project_path).resolve()
    djbrc_file = project_dir / ".djbrc"

    # Update `.djbrc`
    djbrc_content = f"""\
# .djbrc

# Ensure .djbrc can only be sourced.
# This works because return only works inside a function or a sourced script.
( return 0 2>/dev/null ) || {{
    echo "$(basename "$0") must be sourced. Use: \\`. "$0"\\`" >&2
    exit 1
}}

# Exports.
export DJB_PROJECT_DIR={project_dir}
"""
    try:
        with djbrc_file.open("w") as file:
            file.write(djbrc_content)
        click.echo(f"{SUC} Updated {djbrc_file}")
    except Exception as e:
        click.echo(f"{ERR} Failed to update {djbrc_file}: {e}", err=True)
