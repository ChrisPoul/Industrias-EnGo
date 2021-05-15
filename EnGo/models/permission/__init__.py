from sqlalchemy import (
    Column, Integer, String
)
from EnGo.models import db, MyModel


class Permission(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    view_permissions = db.relationship(
        "ViewPermission",
        backref="permission",
        cascade="all, delete-orphan"
    )
    user_permissions = db.relationship(
        'UserPermission',
        backref="permission",
        cascade="all, delete-orphan"
    )

    def get(id):
        return Permission.query.get(id)

    def get_all():
        return Permission.query.all()

    def search(name):
        return Permission.query.filter_by(name=name).first()
