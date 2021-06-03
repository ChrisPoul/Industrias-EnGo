from sqlalchemy import (
    Column, Integer, String
)
from EnGo.models import db, MyModel


class Expense(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    concept = Column(String(200), nullable=False, unique=True)
    type = Column(String(50), nullable=False, default="")
    cost = Column(Integer, nullable=False, default=0)
    registered_expenses = db.relationship(
        'RegisteredExpense',
        backref="expense",
        cascade="all, delete-orphan"
    )

    def get(id):
        return Expense.query.get(id)
    
    def get_all():
        return Expense.query.all()
    
    def search(search_term):
        return Expense.query.filter_by(concept=search_term).first()
    
    @property
    def validation(self):
        from .validation import ExpenseValidation
        return ExpenseValidation(self)
    
    @property
    def request(self):
        from .request import ExpenseRequest
        return ExpenseRequest(self)
