from datetime import datetime
from EnGo.models import db, MyModel
from sqlalchemy import (
    Column, String, Integer,
    DateTime
)

customer_attributes = [
    'customer_name',
    'address',
    'phone',
    'rfc'
]


class Customer(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    customer_name = Column(String(100), nullable=False, unique=False)
    address = Column(String(200), nullable=False, unique=False)
    phone = Column(String(15), nullable=False, unique=False, default="")
    email = Column(String(200), nullable=False, unique=False, default="")
    rfc = Column(String(20), nullable=True, unique=False)
    date = Column(DateTime, nullable=False, default=datetime.now)
    receipts = db.relationship(
        'Receipt',
        backref="customer",
        cascade="all, delete-orphan"
    )

    def get(id):
        return Customer.query.get(id)
    
    def get_all():
        return Customer.query.all()

    def search_all(search_term):
        customers = Customer.query.filter_by(customer_name=search_term).all()
        if customers == []:
            customers = Customer.query.filter_by(address=search_term).all()
        if customers == []:
            customers = Customer.query.filter_by(phone=search_term).all()
        if customers == []:
            customers = Customer.query.filter_by(rfc=search_term).all()
        
        return customers

    @property
    def validation(self):
        from .validation import CustomerValidation
        return CustomerValidation(self)
