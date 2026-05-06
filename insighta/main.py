import click
from insighta.auth import login, logout, whoami
from insighta.profiles.commands import profiles

# -------------------------
# MAIN COMMAND
# -------------------------
@click.group()
def cli():
    pass

# -------------------------
# LOGIN COMMAND
# -------------------------
@cli.command(name="login")
def login_cmd():
    login()

# -------------------------
# PROFILES COMMAND
# -------------------------
cli.add_command(profiles)

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    cli()

# -------------------------
# LOGOUT COMMAND
# -------------------------
@cli.command()
def logout_cmd():
    logout()


# -------------------------
# WHOAMI COMMAND
# -------------------------
@cli.command()
def whoami_cmd():
    whoami()