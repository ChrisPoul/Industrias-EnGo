from datetime import datetime
from functools import cached_property
from EnGo.models import db, MyModel
from sqlalchemy import (
    Column, Integer, String,
    Text, ForeignKey, DateTime
)


class Product(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=True, unique=False)
    price = Column(Integer, nullable=False, default=0)
    sold_products = db.relationship(
        'SoldProduct',
        backref="product",
        cascade="all, delete-orphan"
    )
    finished_products = db.relationship(
        'FinishedProduct',
        backref="product",
        cascade="all, delete-orphan"
    )
    unit = "pz"

    def get(id):
        return Product.query.get(id)

    def get_all():
        return Product.query.all()

    def search(search_term):
        return Product.query.filter_by(code=search_term).first()

    @property
    def validation(self):
        from .validation import ProductValidation
        return ProductValidation(self)

    @property
    def request(self):
        from .request import ProductRequest
        return ProductRequest(self)

    @cached_property
    def inventory(self):
        inventory = {}
        for sold_product in self.sold_products:
            try:
                inventory[sold_product.unit]
            except KeyError:
                inventory[sold_product.unit] = 0
            inventory[sold_product.unit] -= sold_product.quantity
        for finished_product in self.finished_products:
            try:
                inventory[finished_product.unit]
            except KeyError:
                inventory[finished_product.unit] = 0
            inventory[finished_product.unit] += finished_product.quantity

        return inventory


class SoldProduct(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    receipt_id = Column(Integer, ForeignKey('receipt.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    unit = Column(String(10), nullable=False, default="pz")
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(Integer, nullable=False, default=0)
    date = Column(DateTime, nullable=False, default=datetime.now)

    def get(id):
        return SoldProduct.query.get(id)

    @property
    def code(self):
        return self.product.code

    @property
    def description(self):
        return self.product.description

    @property
    def total(self):
        try:
            total = self.quantity * self.price
        except TypeError:
            total = 0

        return total

    @property
    def validation(self):
        from .validation import SoldProductValidation
        return SoldProductValidation(self)

    def get_unique_key(self, attribute):
        return f"{attribute}_{self.id}"


class FinishedProduct(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    warehouse_id = Column(Integer, ForeignKey('warehouse.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    unit = Column(String(10), nullable=False, default="pz")
    cost = Column(Integer, nullable=False, default=0)
    date = Column(DateTime, nullable=False, default=datetime.now)

    @property
    def code(self):
        return self.product.code

    @property
    def description(self):
        return self.product.description

    @property
    def price(self):
        return self.product.price

    @property
    def validation(self):
        from .validation import FinishedProductValidation
        return FinishedProductValidation(self)

    @property
    def request(self):
        from .request import FinishedProductRequest
        return FinishedProductRequest(self)
