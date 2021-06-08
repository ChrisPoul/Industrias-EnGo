from EnGo.models.expense import Expense
from EnGo.models.product import Product


class WarehouseRequest:

    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.error = None
    
    def add(self):
        error = self.warehouse.validation.validate()
        if not error:
            self.warehouse.add()
        
        return error
    
    def update(self):
        error = self.warehouse.validation.validate()
        if not error:
            self.warehouse.update()
        
        return error
    
    def add_expense(self, expense):
        self.error = expense.request.add()
        if not self.error:
            self.warehouse.add_expense(expense)
        
        return self.error
        
        