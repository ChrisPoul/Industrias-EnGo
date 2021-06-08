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
    finished_products = db.relationship(
        'FinishedProduct',
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
    def products(self):
        return [finished_product.product for finished_product in self.finished_products]

    def add_product(self, product):
        from EnGo.models.product import FinishedProduct
        finished_product = FinishedProduct(
            product_id=product.id,
            warehouse_id=self.id
        )
        finished_product.add()
    
    @property
    def expenses(self):
        return [warehouse_expense.expense for warehouse_expense in self.warehouse_expenses]

    def add_expense(self, expense):
        from EnGo.models.expense import WarehouseExpense
        warehouse_expense = WarehouseExpense(
            expense_id=expense.id,
            warehouse_id=self.id
        )
        warehouse_expense.add()

    def search_expenses(self, search_term):
        return [expense for expense in self.expenses if expense.concept == search_term]
        
