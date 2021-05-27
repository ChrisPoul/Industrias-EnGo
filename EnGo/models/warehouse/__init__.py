from sqlalchemy import (
    Column, Integer, String
)
from EnGo.models import db, MyModel


class Warehouse(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    address = Column(String(200), nullable=False, unique=True)
