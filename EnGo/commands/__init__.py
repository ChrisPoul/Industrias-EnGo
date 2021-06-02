import os
import click
from flask import current_app
from flask.cli import with_appcontext


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized database")


def init_db():
    # db.drop_all()
    # db.create_all()
    # create_admin_user("Admin")
    pass


def create_admin_user(username):
    from werkzeug.security import generate_password_hash
    from .permission import Permission
    from .user import User
    admin_permission = Permission(
        permission_name="Admin"
    )
    admin_permission.add()
    admin_user = User(
        username=username,
        password=generate_password_hash('0000')
    )
    admin_user.add()
    admin_user.add_permission(admin_permission)


@click.command("init-db")
def init_settings_command():
    init_settings()
    click.echo("Initialized Settings")


def init_settings():
    settings_path = os.path.join(current_app.instance_path, "settings.json")
    with open(settings_path, "w+") as settings_file:
        pass
