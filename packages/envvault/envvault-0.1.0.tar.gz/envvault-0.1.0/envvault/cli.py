import os
import subprocess

import click

from .core import CredentialsManager


def open_editor(file_path):
    """
    Opens the file with the default editor.

    :param file_path: File path.
    """
    editor = os.getenv(
        "EDITOR", "vim"
    )  # Defaults to vim, can be set to other editors via environment variable
    subprocess.call([editor, file_path])


@click.group()
def cli():
    """Manage encrypted environment variables."""
    pass


@cli.command()
@click.option(
    "--env",
    default="development",
    help="Environment name (e.g., development, production).",
)
def init(env):
    """Initialize a new master key and create an empty .env.enc file."""
    manager = CredentialsManager(env_name=env)
    manager.create_empty_env_enc()
    click.echo(
        f"Master key created for {env} environment and empty .env.enc file created."
    )


@cli.command()
@click.option(
    "--env",
    default="development",
    help="Environment name (e.g., development, production).",
)
def edit(env):
    """Decrypt, edit, and re-encrypt the .env.enc file."""
    manager = CredentialsManager(env_name=env)

    # Ensure the master key and .env.enc file exist
    manager.ensure_files_exist()

    try:
        # Decrypts to a temporary file
        temp_file_path = manager.decrypt_to_temp()
        click.echo(f"Decrypted to temporary file: {temp_file_path}")

        # Opens editor
        click.echo(f"Opening editor to edit {temp_file_path}...")
        open_editor(temp_file_path)

        # Re-encrypts
        manager.encrypt_from_temp(temp_file_path)
    finally:
        # Cleans up temporary file
        manager.cleanup_temp_file(temp_file_path)


@cli.command()
@click.option(
    "--env",
    default="development",
    help="Environment name (e.g., development, production).",
)
def view(env):
    """Decrypt and view the .env.enc file."""
    manager = CredentialsManager(env_name=env)
    try:
        env_vars = manager.decrypt_env()
        for key, value in env_vars.items():
            click.echo(f"{key}={value}")
    except FileNotFoundError as e:
        click.echo(str(e), err=True)


if __name__ == "__main__":
    # Execute the CLI application
    cli()
