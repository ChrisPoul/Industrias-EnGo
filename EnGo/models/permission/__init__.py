from sqlalchemy import (
    Column, Integer, String,
    Text
)
from EnGo.models import db, MyModel

permission_attributes = [
    "permission_name",
    "description"
]


class Permission(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    permission_name = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=True, unique=False)
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
        return Permission.query.filter_by(permission_name=name).first()

    @property
    def views(self):
        return [view_permission.view for view_permission in self.view_permissions]

    @property
    def users(self):
        return [user_permission.user for user_permission in self.user_permissions]

    @property
    def validation(self):
        from .validation import PermissionValidation
        return PermissionValidation(self)

    def is_admin(self):
        if self.permission_name == "Admin":
            return True
        
        return False
