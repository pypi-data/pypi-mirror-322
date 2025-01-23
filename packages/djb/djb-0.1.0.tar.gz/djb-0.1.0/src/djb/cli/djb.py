import click

from djb.cli.djbrc import djbrc
from djb.cli.install import install, update
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
def main(
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


main.add_command(create)
main.add_command(up)
main.add_command(djbrc)
main.add_command(install)
main.add_command(update)
