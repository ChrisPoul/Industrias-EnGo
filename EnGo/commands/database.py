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
    create_admin_user("Admin")


def create_admin_user(username):
    from werkzeug.security import generate_password_hash
    from EnGo.models.permission import Permission
    from EnGo.models.user import User
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


@click.command("modify-tables")
@with_appcontext
def modify_tables_command():
    modify_tables()
    click.echo("Modified Tables")


def modify_tables():
    from EnGo.models.warehouse import Warehouse
    Warehouse.__table__.drop(db.engine)
    from EnGo.models.consumable import Consumable
    Consumable.__table__.drop(db.engine)
    from EnGo.models.raw_material import RawMaterial
    RawMaterial.__table__.drop(db.engine)
    db.create_all()
