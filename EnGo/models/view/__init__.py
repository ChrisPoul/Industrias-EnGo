from sqlalchemy import (
    Column, Integer, String,
    ForeignKey
)
from EnGo.models import db, MyModel


class View(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    view_name = Column(String(100), nullable=False, unique=True)
    view_permissions = db.relationship(
        'ViewPermission',
        backref="view",
        cascade="all, delete-orphan"
    )

    @property
    def permissions(self):
        return [view_permission.permission for view_permission in self.view_permissions]

    def get(id):
        return View.query.get(id)

    def get_all():
        return View.query.all()

    def search(name):
        return View.query.filter_by(view_name=name).first()

    def requires_dev(self):
        for permission in self.permissions:
            if permission.is_dev():
                return True
        
        return False

    def add_permissions(self, permissions):
        for permission in permissions:
            self.add_permission(permission)

    def add_permission(self, permission):
        view_permission = ViewPermission(
            view_id=self.id,
            permission_id=permission.id
        )
        view_permission.add()

    def update_permissions(self, permissions):
        self.delete_permissions()
        self.add_permissions(permissions)

    def delete_permissions(self):
        for view_permission in self.view_permissions:
            view_permission.delete()


class ViewPermission(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    view_id = Column(Integer, ForeignKey('view.id'), nullable=False)
    permission_id = Column(Integer, ForeignKey('permission.id'), nullable=False)
