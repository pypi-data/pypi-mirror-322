import click

from djb.cli.djbrc import djbrc
from djb.cli.install import install
from djb.cli.create import create
from djb.cli.up import up


class OrderedGroup(click.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_order = []

    def add_command(self, cmd, name=None):
        super().add_command(cmd, name)
        self.command_order.append(name or cmd.name)

    def list_commands(self, ctx):
        return self.command_order


class AppContext:
    def __init__(self):
        # Global options.
        self.debug = False
        self.verbose = False

        # djb update options.
        self.update = False


@click.group(cls=OrderedGroup)
@click.option("--debug", is_flag=True, help="Enable debug output.")
@click.option("--verbose", is_flag=True, help="Enable verbose output.")
@click.pass_context
def cli(
    ctx,
    debug,
    verbose,
):
    """
    djb (dj_bun): playin' dev and deploy since 1984 🎶
    """
    ctx.ensure_object(AppContext)
    ctx.obj.debug = debug
    ctx.obj.verbose = verbose


cli.add_command(create)
cli.add_command(up)
cli.add_command(djbrc)
cli.add_command(install)


def main():
    cli(max_content_width=100)


if __name__ == "__main__":
    main()
