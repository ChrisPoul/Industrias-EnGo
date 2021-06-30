from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, 
    DateTime
)
from EnGo.models import db, MyModel


class Warehouse(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    address = Column(String(200), nullable=False, unique=True)
    date = Column(DateTime, nullable=False, default=datetime.now)
    products = db.relationship(
        'Product',
        backref="warehouse",
        cascade="all, delete-orphan"
    )
    warehouse_expenses = db.relationship(
        'WarehouseExpense',
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
    def expenses(self):
        return [warehouse_expense.expense for warehouse_expense in self.warehouse_expenses]

    def add_expense(self, expense):
        from EnGo.models.expense import WarehouseExpense
        warehouse_expense = WarehouseExpense(
            warehouse_id=self.id,
            expense_id=expense.id
        )
        warehouse_expense.add()
        
