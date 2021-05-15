from sqlalchemy import (
    Column, Integer, String,
    ForeignKey
)
from EnGo.models import db, MyModel


class View(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
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
        return View.query.filter_by(name=name).first()


class ViewPermission(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    view_id = Column(Integer, ForeignKey('view.id'), nullable=False)
    permission_id = Column(Integer, ForeignKey('permission.id'), nullable=False)
