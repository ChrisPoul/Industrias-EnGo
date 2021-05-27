from sqlalchemy import(
    Column, Integer, String
)
from EnGo.models import db, MyModel


class RawMaterial(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    material = Column(String(100), nullable=False, unique=True)
    price = Column(Integer, nullable=False)
