import click
from EnGo.models import db
from flask.cli import with_appcontext


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized database")


def init_db():
    db.drop_all()
    db.create_all()
    create_admin_user()
    create_dev_user()
    from .settings import init_settings
    init_settings()


def create_admin_user():
    from werkzeug.security import generate_password_hash
    from EnGo.models.permission import Permission
    from EnGo.models.user import User
    admin_permission = Permission(
        permission_name="Admin"
    )
    admin_permission.add()
    admin_user = User(
        username="Admin",
        password=generate_password_hash('0000')
    )
    admin_user.add()
    admin_user.add_permission(admin_permission)


def create_dev_user():
    from werkzeug.security import generate_password_hash
    from EnGo.models.permission import Permission
    from EnGo.models.user import User
    dev_permission = Permission.search("Dev")
    if not dev_permission:
        dev_permission = Permission(
            permission_name="Dev"
        )
        dev_permission.add()
    dev_user = User(
        username="Dev",
        password=generate_password_hash('0000')
    )
    dev_user.add()
    dev_user.add_permission(dev_permission)


@click.command("update-db")
@with_appcontext
def update_db_command():
    update_db()
    click.echo("Updated Database")


def update_db():
    from EnGo.models.warehouse import (
        Warehouse, FinishedProduct
    )
    Warehouse.__table__.drop(db.engine)
    FinishedProduct.__table__.drop(db.engine)
    from EnGo.models.expense import RegisteredExpense
    RegisteredExpense.__table__.drop(db.engine)
    db.create_all()
    create_dev_user()
