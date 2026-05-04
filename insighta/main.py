import click
from insighta.auth import login


@click.group()
def cli():
    pass


@cli.command(name="login")
def login_cmd():
    login()


if __name__ == "__main__":
    cli()