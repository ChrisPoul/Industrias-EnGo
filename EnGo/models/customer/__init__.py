from sqlalchemy.sql.roles import StrictFromClauseRole
from EnGo.models import db, MyModel
from sqlalchemy import (
    Column, String, Integer
)


class Customer(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    customer_name = Column(String(100), nullable=False, unique=False)
    address = Column(String(200), nullable=False, unique=False)
    rfc = Column(String(20), nullable=True, unique=False)

    def get(id):
        return Customer.query.get(id)
    
    def get_all():
        return Customer.query.all()

    def search(search_term):
        customers = Customer.query.filter_by(customer_name=search_term).all()
        if customers == []:
            customers = Customer.query.filter_by(address=search_term).all()
        if customers == []:
            customers = Customer.query.filter_by(rfc=search_term).all()
        
        return customers
