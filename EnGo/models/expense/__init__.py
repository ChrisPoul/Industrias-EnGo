from datetime import datetime
from sqlalchemy import (
    Column, Integer, String,
    ForeignKey, DateTime
)
from EnGo.models import db, MyModel


class Expense(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    concept = Column(String(200), nullable=False, unique=False)
    type_id = Column(Integer, ForeignKey('expense_type.id'), nullable=False)
    cost = Column(Integer, nullable=False, default=0)
    unit = Column(String(20), nullable=False, default="pz")
    quantity = Column(Integer, nullable=False, default=0)
    warehouse_expenses = db.relationship(
        'WarehouseExpense',
        backref="expense",
        cascade="all, delete-orphan"
    )

    def get(id):
        return Expense.query.get(id)
    
    def get_all():
        return Expense.query.all()
    
    def search_all(search_term):
        return Expense.query.filter_by(concept=search_term).all()
    
    @property
    def validation(self):
        from .validation import ExpenseValidation
        return ExpenseValidation(self)
    
    @property
    def request(self):
        from .request import ExpenseRequest
        return ExpenseRequest(self)


class WarehouseExpense(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    expense_id = Column(Integer, ForeignKey('expense.id'), nullable=False)
    warehouse_id = Column(Integer, ForeignKey('warehouse.id'), nullable=False)

    
class ExpenseType(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    expenses = db.relationship(
        'Expense',
        backref='type',
        cascade='all, delete-orphan'
    )
