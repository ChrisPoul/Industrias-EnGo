


class ExpenseRequest:

    def __init__(self, expense):
        self.expense = expense
        self.error = None
    
    def add(self):
        self.error = self.expense.validation.validate()
        if not self.error:
            self.expense.add()
        
        return self.error
    
    def update(self):
        self.error = self.expense.validation.validate()
        if not self.error:
            self.expense.update()
        
        return self.error
