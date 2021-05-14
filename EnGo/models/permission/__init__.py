from sqlalchemy import (
    Column, Integer, String
)
from EnGo.models import db, MyModel


class Permission(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    views = db.relationship(
        "View",
        backref="parent",
        cascade="all, delete-orphan"
    )
    user_permissions = db.relationship(
        'UserPermission',
        backref="permission",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def get(id):
        return Permission.query.get(id)

    def search(name):
        return Permission.query.filter_by(name=name).first()
