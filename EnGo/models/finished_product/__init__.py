from sqlalchemy import (
    Column, Integer, String,
    ForeignKey
)
from EnGo.models import db, MyModel
from EnGo.models.warehouse import Warehouse


class FinishedProduct(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    warehouse_id = Column(Integer, ForeignKey('warehouse.id'), nullable=False)
    inventory = Column(Integer, nullable=False, default=0)
    unit = Column(String(10), nullable=False, default="pz")
    cost = Column(Integer, nullable=False, default=0)

    def get(id):
        return FinishedProduct.query.get(id)

    def get_all():
        return FinishedProduct.query.all()
    