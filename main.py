import click

@click.group()
def cli():
    pass

@cli.command()
def login():
    print("Starting login...")

if __name__ == "__main__":
    cli()