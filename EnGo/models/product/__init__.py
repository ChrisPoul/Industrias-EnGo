from datetime import datetime
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
    
    


class SoldProduct(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    receipt_id = Column(Integer, ForeignKey('receipt.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    unit = Column(String(10), nullable=False, default="pz")
    quantity = Column(Integer, nullable=False, default=0)
    quantity_ref = Column(Integer, nullable=False, default=0)
    price = Column(Integer, nullable=False, default=0)

    def get(id):
        return SoldProduct.query.get(id)

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

    def update_product_inventory(self):
        quantity_change = int(self.quantity) - self.quantity_ref
        self.product.inventory -= quantity_change
        self.quantity_ref = self.quantity


from EnGo.models.warehouse import FinishedProduct