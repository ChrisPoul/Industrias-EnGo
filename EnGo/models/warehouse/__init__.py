from datetime import datetime
from sqlalchemy import (
    Column, Integer, String,
    ForeignKey, DateTime
)
from EnGo.models import db, MyModel


class Warehouse(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    address = Column(String(200), nullable=False, unique=True)
    date = Column(DateTime, nullable=False, default=datetime.now)
    finished_products = db.relationship(
        'FinishedProduct',
        backref="warehouse",
        cascade="all, delete-orphan"
    )
    registered_expenses = db.relationship(
        'RegisteredExpense',
        backref="warehouse",
        cascade="all, delete-orphan"
    )

    def get(id):
        return Warehouse.query.get(id)

    def get_all():
        return Warehouse.query.all()
    
    def search(search_term):
        return Warehouse.query.filter_by(address=search_term).first()
    
    @property
    def request(self):
        from .request import WarehouseRequest
        return WarehouseRequest(self)
    
    @property
    def validation(self):
        from .validation import WarehouseValidation
        return WarehouseValidation(self)

    @property
    def products(self):
        return [finished_product.product for finished_product in self.finished_products]

    def add_product(self, product):
        finished_product = FinishedProduct(
            product_id=product.id,
            warehouse_id=self.id
        )
        finished_product.add()
    
    @property
    def expenses(self):
        return [registered_expense.expense for registered_expense in self.registered_expenses]

    def add_expense(self, expense):
        from EnGo.models.expense import RegisteredExpense
        try:
            expense.quantity
        except AttributeError:
            expense.quantity = 0
        try:
            expense.registered_type_id
        except AttributeError:
            expense.registered_type_id = expense.type_id
        registered_expense = RegisteredExpense(
            expense_id=expense.id,
            warehouse_id=self.id,
            type_id=expense.registered_type,
            cost=expense.cost,
            quantity=expense.quantity
        )
        registered_expense.add()


class FinishedProduct(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    warehouse_id = Column(Integer, ForeignKey('warehouse.id'), nullable=False)
    inventory = Column(Integer, nullable=False, default=0)
    unit = Column(String(10), nullable=False, default="pz")
    cost = Column(Integer, nullable=False, default=0)
    date = Column(DateTime, nullable=False, default=datetime.now)

    def get(id):
        return FinishedProduct.query.get(id)
