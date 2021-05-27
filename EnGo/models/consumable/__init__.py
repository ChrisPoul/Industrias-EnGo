from EnGo.models.raw_material import RawMaterial
from sqlalchemy import (
    Column, Integer, String
)
from EnGo.models import db, MyModel


class Consumable(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    consumable_name = Column(String(200), nullable=False, unique=True)
    price = Column(Integer, nullable=False, default=0)

    def get(id):
        return Consumable.query.get(id)
    
    def get_all():
        return Consumable.query.all()
    
    def search(search_term):
        return Consumable.query.filter_by(consumable_name=search_term).first()

