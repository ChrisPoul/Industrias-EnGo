from EnGo.models import db, MyModel
from sqlalchemy import (
    Column, Integer, String,
    Text
)
from EnGo.models.receipt import Receipt
from EnGo.models.sold_product import SoldProduct


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

