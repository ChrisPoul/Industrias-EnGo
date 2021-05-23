from EnGo.models import db, MyModel
from sqlalchemy import (
    Column, Integer, String,
    Text, ForeignKey
)
from EnGo.models.receipt import Receipt


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
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(Integer, nullable=False, default=0)

    def get(id):
        return SoldProduct.query.get(id)

    @property
    def total(self):
        return self.quantity * self.price

    def get_unique_key(self, attribute):
        return f"{attribute}_{self.id}"

