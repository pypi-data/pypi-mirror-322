import itertools
import os
from pathlib import Path
import re
import shutil
import subprocess
import traceback
from typing import List

import click

from djb.cli.constants import DJB_REPO_URL, ERR, NXT, OBS, SUC, TIP, WRN


def command_exists(command: str) -> bool:
    return shutil.which(command) is not None


def missing_binaries(binaries: List[str]):
    missing_binaries = []
    for binary in binaries:
        if not command_exists(binary):
            missing_binaries.append(binary)
    return missing_binaries


def install_or_update_tool(
    ctx: click.Context,
    update: bool,
    name: str,
    binaries: str | List[str],
    in_cmds: str | List[str],
    up_cmds: str | List[str],
):
    update = update or ctx.obj.update
    binaries = binaries if isinstance(binaries, list) else [binaries]
    in_cmds = in_cmds if isinstance(in_cmds, list) else [in_cmds]
    up_cmds = up_cmds if isinstance(up_cmds, list) else [up_cmds]

    if update:
        if missing_binaries_ := missing_binaries(binaries):
            if len(missing_binaries_) < len(binaries):
                click.echo(
                    f"{WRN} `{name}` update requested but `{name}` is not fully installed yet. The following binaries are missing: {' '.join(missing_binaries_)}"
                )
            else:
                click.echo(
                    f"{WRN} `{name}` update requested but `{name}` is not installed yet."
                )
            click.echo(f"{TIP} Use `djb up && source .djbrc` to install `{name}`.")
        else:
            click.echo(f"{NXT} `{name}` updating...")
            try:
                for cmd in up_cmds:
                    if ctx.obj.verbose:
                        click.echo(f"{NXT} Executing `{cmd}`...")
                    subprocess.run(cmd, shell=True, check=True)
                if missing_binaries_ := missing_binaries(binaries):
                    click.echo(
                        f"{WRN} `{name}` updated without errors, but the following binaries are now missing: {' '.join(missing_binaries_)}"
                    )
                else:
                    click.echo(f"{SUC} `{name}` updated.")
            except subprocess.CalledProcessError as e:
                click.echo(
                    f"{ERR} `{name}` failed to execute update command `{cmd}`: {e}",
                    err=True,
                )
                if ctx.obj.debug:
                    traceback.print_exc()

    else:
        if not missing_binaries(binaries):
            click.echo(f"{SUC} `{name}` is already installed.")
            return

        click.echo(f"{NXT} `{name}` installing...")
        try:
            for cmd in in_cmds:
                if ctx.obj.verbose:
                    click.echo(f"{NXT} Executing `{cmd}`...")
                subprocess.run(cmd, shell=True, check=True)
            if missing_binaries_ := missing_binaries(binaries):
                click.echo(
                    f"{WRN} `{name}` installed without errors, but the following binaries are still missing: {' '.join(missing_binaries_)}"
                )
            else:
                click.echo(f"{SUC} `{name}` installed.")
        except subprocess.CalledProcessError as e:
            click.echo(
                f"{ERR} `{name}` failed to execute install command `{cmd}`: {e}",
                err=True,
            )
            if ctx.obj.debug:
                traceback.print_exc()


@click.command()
@click.option(
    "-u", "--update", is_flag=True, help="Update homebrew to the latest version."
)
@click.pass_context
def homebrew(ctx, update):
    """Install homebrew."""
    install_or_update_tool(
        ctx,
        update,
        name="homebrew",
        binaries="brew",
        in_cmds='/bin/bash -c "$(curl -LsSf https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
        up_cmds="brew update",
    )


@click.command()
@click.option("-u", "--update", is_flag=True, help="Update uv to the latest version.")
@click.pass_context
def uv(ctx, update):
    """Install uv."""
    install_or_update_tool(
        ctx,
        update,
        name="uv",
        binaries="uv",
        in_cmds="curl -LsSf https://astral.sh/uv/install.sh | sh",
        up_cmds="uv self update",
    )


@click.command()
@click.option("-u", "--update", is_flag=True, help="Pull the latest version of djb.")
@click.option(
    "--project-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True),
    default=os.getenv("DJB_PROJECT_DIR", "."),
    show_default=True,
    help="Path to your djb project.",
)
@click.option(
    "-r",
    "--djb-repo-url",
    default=DJB_REPO_URL,
    show_default=True,
    help="Git repository URL for djb.",
)
@click.option(
    "-d",
    "--djb-lib-path",
    type=click.Path(file_okay=False, dir_okay=True, writable=True),
    default="./djb",
    show_default=True,
    help="A project-relative path where the djb repository is installed.",
)
@click.pass_context
def editable_djb(ctx, update, project_path, djb_repo_url, djb_lib_path):
    """
    Optional; install djb as an editable dependency.

    Note: --djb-lib-path is added to your .gitignore.
    """
    update = update or ctx.obj.update

    if not command_exists("uv"):
        click.echo(f"{ERR} `uv` is not installed or not in PATH.")
        click.echo(f"{TIP} `uv` and djb's other development dependencies are installed using `djb up && source .djbrc`.")
        ctx.exit(1)    

    # Ensure project directory exists and switch to it.
    project_dir = Path(project_path).resolve()
    if not project_dir.exists():
        click.echo(f"{ERR} Project directory {project_dir} does not exist.")
        ctx.exit(1)
    os.chdir(project_dir)

    djb_dir = project_dir / djb_lib_path
    if djb_dir.exists():
        if update:
            click.echo(f"{NXT} Updating djb in {djb_dir}...")
            try:
                subprocess.run(["git", "-C", str(djb_dir), "pull"], check=True)
                click.echo(f"{SUC} djb updated.")
            except subprocess.CalledProcessError as e:
                click.echo(
                    f"{ERR} Failed to update djb repository in {djb_dir}: {e}",
                    err=True,
                )
                if ctx.obj.debug:
                    traceback.print_exc()
                ctx.exit(1)
        else:
            click.echo(f"{OBS} djb repository is already present at '{djb_dir}'.")
    else:
        if update:
            click.echo(
                f"{WRN} `editable-djb` update requested but an editable djb is not installed yet."
            )
            click.echo(f"{TIP} Use `djb install editable-djb` to install djb in editable mode.")
            ctx.exit(1) 

        click.echo(f"{NXT} Cloning djb repository from {djb_repo_url} into {djb_dir}...")
        try:
            subprocess.run(["git", "clone", djb_repo_url, str(djb_dir)], check=True)
            click.echo(f"{SUC} djb repository cloned.")
        except subprocess.CalledProcessError as e:
            click.echo(
                f"{ERR} Failed to clone djb repository from {djb_repo_url}: {e}",
                err=True,
            )
            if ctx.obj.debug:
                traceback.print_exc()
            ctx.exit(1)

    # Install djb in editable mode
    click.echo(f"{NXT} Installing djb in editable mode from '{djb_dir}'...")
    try:
        cmd = [
            "uv", "pip", "install",
            "--project", str(project_dir), 
            "--editable", str(djb_dir),
            "--reinstall-package", "djb",
        ]
        if ctx.obj.verbose:
            click.echo(f"Running `uv pip install` command: {cmd}")
        subprocess.run(cmd, check=True)
        click.echo(f"{SUC} djb installed in editable mode.")
    except subprocess.CalledProcessError as e:
        click.echo(
            f"{ERR} Failed to install djb in editable mode from {djb_dir}: {e}",
            err=True,
        )
        if ctx.obj.debug:
            traceback.print_exc()
        ctx.exit(1)

    # Add djb_dir to .gitignore if not already present
    gitignore_path = project_dir / ".gitignore"
    if gitignore_path.exists():
        with open(gitignore_path, "r") as f:
            gitignore_content = f.read()
    else:
        gitignore_content = ""
    if not re.search(rf"^{re.escape(djb_lib_path)}$", gitignore_content, re.MULTILINE):
        with open(gitignore_path, "a") as f:
            f.write(f"\n# editable djb dir\n{str(djb_lib_path)}\n")
        click.echo(f"{NXT} Added {djb_dir} to .gitignore.")
    else:
        if ctx.obj.verbose:
            click.echo(f"{OBS} {djb_dir} is already in .gitignore.")



DEFAULT_INSTALLERS = [homebrew, uv]
EDITABLE_DJB_INSTALLERS = [editable_djb]


@click.group(chain=True, invoke_without_command=True)
@click.pass_context
def install(ctx):
    """
    Install development dependencies.
    """
    if not ctx.invoked_subcommand:
        click.echo(f"{NXT} Verifying and installing dependencies...")
        for installer in DEFAULT_INSTALLERS:
            ctx.invoke(installer)


@click.group(chain=True, invoke_without_command=True)
@click.pass_context
def update(ctx):
    """
    Update development dependencies.
    """
    ctx.obj.update = True
    if not ctx.invoked_subcommand:
        click.echo(f"{NXT} Verifying and updating dependencies...")
        for installer in DEFAULT_INSTALLERS:
            ctx.invoke(installer)


for installer in itertools.chain(
    DEFAULT_INSTALLERS,
    EDITABLE_DJB_INSTALLERS,
):
    install.add_command(installer)
    update.add_command(installer)
