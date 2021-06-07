


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


class ExpenseTypeRequest:

    def __init__(self, expense_type):
        self.expense_type = expense_type

    def add(self):
        error = self.expense_type.validation.validate()
        if not error:
            self.expense_type.add()

        return error
