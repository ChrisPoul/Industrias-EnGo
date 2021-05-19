from EnGo.models import db, MyModel
from datetime import datetime
from sqlalchemy import (
    Column, Integer, DateTime
)


class Receipt(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=datetime.now)
    sold_products = db.relationship(
        'SoldProduct',
        backref="receipt",
        cascade="all, delete-orphan"
    )

    def get(id):
        return Receipt.query.get(id)

    def get_all():
        return Receipt.query.all()

    @property
    def products(self):
        return [sold_product.product for sold_product in self.sold_products]

    def add_product(self, product):
        from EnGo.models.product import SoldProduct
        sold_product = SoldProduct(
            receipt_id=self.id,
            product_id=product.id
        )
        sold_product.add()

