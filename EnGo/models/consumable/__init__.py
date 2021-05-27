from sqlalchemy import (
    Column, Integer, String
)
from EnGo.models import db, MyModel


class Consumable(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    consumable_name = Column(String(200), nullable=False, unique=True)
    price = Column(Integer, nullable=False, default=0)
