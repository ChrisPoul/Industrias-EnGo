import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class MyModel:

    def add(self):
        db.session.add(self)
        commit_to_db()
    
    def update(self):
        commit_to_db()

    def delete(self):
        db.session.delete(self)
        commit_to_db()


def init_db():
    db.drop_all()
    db.create_all()
    create_admin_user("Chris")


def create_admin_user(username):
    from .permission import Permission
    from .user import User
    admin_permission = Permission(
        permission_name="admin"
    )
    admin_permission.add()
    admin_user = User(
        username=username,
        password="0000"
    )
    admin_user.add()
    admin_user.add_permission(admin_permission)


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized database")


def commit_to_db():
    db.session.commit()


def has_nums(some_string):
    nums = "1234567890"
    for char in some_string:
        if char in nums:
            return True

    return False
