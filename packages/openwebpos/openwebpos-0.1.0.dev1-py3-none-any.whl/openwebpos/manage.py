import click

from .initial_data import ROLES


def add_cli_commands(app):
    """Add custom commands to the Flask CLI."""

    from openwebpos.extensions import db
    from openwebpos.blueprints.user.models.role import Role
    from openwebpos.blueprints.user.models.user import User

    def populate_table(table, data):
        for row in data:
            table.create(**row)

    @app.cli.command("initdb", help="Initialize the database.")
    @click.option(
        "--populate", is_flag=True, help="Populate database with initial data."
    )
    @click.confirmation_option(
        prompt="This will drop existing tables if they exist. Proceed?",
        help="Confirm the action before proceeding.",
    )
    def initdb(populate):
        """Initialize the database."""

        click.echo("Dropping existing tables...")
        db.drop_all()
        click.echo("Done dropping existing tables!")

        click.echo("Initializing database...")
        db.create_all()
        click.echo("Done initializing database!")

        if populate:
            click.echo("Populating database with initial data...")
            populate_table(Role, ROLES)
            click.echo("Starting the admin user setup process.")
            click.echo("Please enter the following information:")
            click.echo("Username:")
            username = click.prompt("", type=str)
            click.echo("Email:")
            email = click.prompt("", type=str)
            click.echo("Password:")
            password = click.prompt("", type=str, hide_input=True)
            create_admin(username=username, email=email, password=password)
            click.echo("Done populating database!")

    def create_admin(username, email, password):
        """Create an admin user."""

        user_exists = User.query.count() > 0

        if user_exists:
            raise click.ClickException("Admin user already exists.")
        else:
            click.echo("Creating admin user...")
            admin_role_id = Role.query.filter_by(name="admin").first().id
            User.create(
                username=username,
                email=email,
                password=password,
                is_active=True,
                role_id=admin_role_id,
            )
            click.echo("Admin user created successfully.")

    app.cli.add_command(initdb)
