import os

from typing import Any, Optional, Type

import click


class Off:
    def __init__(self, name="Off"):
        self.name = name

    def __bool__(self):
        return False
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def project_dir_option():
    """Reusable option for specifying the djb project directory."""
    return click.option(
        "--project",
        type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True),
        default=os.getenv("DJB_PROJECT_DIR", "."),
        envvar="DJB_PROJECT_DIR",
        show_default=True,
        show_envvar=True,
        help="Path to djb project directory.",
        metavar="DIR",
    )
