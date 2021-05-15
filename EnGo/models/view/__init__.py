from sqlalchemy import (
    Column, Integer, String,
    ForeignKey
)
from EnGo.models import db, MyModel


class View(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    permission_id = Column(Integer, ForeignKey('permission.id'))

    def get(id):
        return View.query.get(id)

    def get_all():
        return View.query.all()

    def search(name):
        return View.query.filter_by(name=name).first()
