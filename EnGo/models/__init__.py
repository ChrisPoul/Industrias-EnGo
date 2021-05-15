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
    from .user import User, UserPermission
    permission = Permission(
        name="admin"
    )
    permission.add()
    user = User(
        username=username,
        password="0000"
    )
    user.add()
    user_permission = UserPermission(
        user_id=user.id,
        permission_id=permission.id
    )
    user_permission.add()


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized database")


def commit_to_db():
    db.session.commit()
