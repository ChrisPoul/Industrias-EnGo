from sqlalchemy import (
    Column, Integer, String,
    ForeignKey
)
from EnGo.models import db, MyModel
from EnGo.models.consumable import Consumable


class BoughtConsumable(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    consumable_id = Column(Integer, ForeignKey('consumable.id'), nullable=False)
    warehouse_id = Column(Integer, ForeignKey('warehouse.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(Integer, nullable=False, default=0)

    def get(id):
        return BoughtConsumable.query.get(id)

    def get_all():
        return BoughtConsumable.query.all()