import click
from fdm_cli.commands import content, dirs, files, list, purge


@click.group()
@click.version_option("0.0.1")
def cli():
    """
    FDM-CLI >> File & Directory Manager CLI Tool.

    A command line utility (CLI) for file and directory operations.
    Provides commands to list files, create directories and files,
    purge files and directories, and display file contents.
    """
    pass


cli.add_command(list)
cli.add_command(dirs)
cli.add_command(files)
cli.add_command(purge)
cli.add_command(content)
