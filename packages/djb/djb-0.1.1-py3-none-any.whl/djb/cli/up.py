import os
import click

from djb.cli.click_util import project_dir_option
from djb.cli.djbrc import djbrc
from djb.cli.install import install


@click.command()
@project_dir_option()
@click.option(
    "--update",
    is_flag=True,
    help="""
    Update installed project dependencies and configure project environment.
    """,
)
@click.pass_context
def up(ctx, project, update):
    """
    Install development dependencies and configure project env.

    Shorthand for `djb install && djb djbrc`. Additionally, `djb up --update`
    is shorthand for `djb update && djb djbrc`.

    This command verifies and installs project dependencies, then updates
    the project's `.djbrc` script based on the current project state.

    Tip: It's best to run `djb up` as `djb up && source .djbrc` to ensure that
    your shell environment reflects any changes.
    """
    ctx.invoke(install, update=update)
    ctx.invoke(djbrc, project=project)
