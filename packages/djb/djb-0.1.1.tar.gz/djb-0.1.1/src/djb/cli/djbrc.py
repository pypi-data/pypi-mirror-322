import os
from pathlib import Path

import click

from djb.cli.click_util import project_dir_option
from djb.cli.constants import ERR, SUC


@click.command()
@project_dir_option()
def djbrc(project):
    """
    Update `.djbrc` script based on the project's current state.

    Tip: It's best to run `djb djbrc` as `djb djbrc && source .djbrc` to ensure
    that your shell environment reflects any changes.
    """
    click.echo("→ Updating .djbrc...")
    project_path = Path(project).resolve()
    djbrc_file_path = project_path / ".djbrc"

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
export DJB_PROJECT_DIR={project_path}
"""
    try:
        with djbrc_file_path.open("w") as file:
            file.write(djbrc_content)
        click.echo(f"{SUC} Updated '{djbrc_file_path}'.")
    except Exception as e:
        click.echo(f"{ERR} Failed to update '{djbrc_file_path}': {e}", err=True)
