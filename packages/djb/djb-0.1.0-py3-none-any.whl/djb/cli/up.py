import click

# from djb.cli.project import project
from djb.cli.djbrc import djbrc
from djb.cli.install import install
from djb.cli.install import update as _update


@click.command()
@click.option(
    "--project-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True),
    default=".",
    show_default=True,
    help="Path to djb project.",
)
@click.option(
    "--update",
    is_flag=True,
    help="""
    Update installed project dependencies and configure project environment.
    """,
)
@click.pass_context
def up(ctx, project_path, update):
    """
    Install development dependencies and configure project env.

    Shorthand for `djb install && djb djbrc`. Additionally, `djb up --update`
    is shorthand for `djb update && djb djbrc`.

    This command verifies and installs project dependencies, then updates
    the project's `.djbrc` script based on the current project state.

    Tip: It's best to run `djb up` as `djb up && source .djbrc` to ensure that
    your shell environment reflects any changes.
    """
    print(f"Update: {update}")
    if update:
        ctx.invoke(_update)
    else:
        ctx.invoke(install)
    ctx.invoke(djbrc, project_path=project_path)
