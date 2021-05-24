from EnGo.models import db, MyModel
from sqlalchemy import (
    Column, Integer, ForeignKey
)


class SoldProduct(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    receipt_id = Column(Integer, ForeignKey('receipt.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(Integer, nullable=False, default=0)

    def get(id):
        return SoldProduct.query.get(id)

    @property
    def total(self):
        return self.quantity * self.price

    def get_unique_key(self, attribute):
        return f"{attribute}_{self.id}"