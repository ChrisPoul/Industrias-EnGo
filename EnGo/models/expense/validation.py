from . import Expense
from EnGo.errors.messages import repeated_value_error
from EnGo.models import validate_empty_values


class ExpenseValidation:

    def __init__(self, expense):
        self.expense = expense
        self.error = None

    def validate(self):
        self.validate_empty_values()
        if not self.error:
            self.validate_unique_values()

        return self.error
    
    def validate_empty_values(self):
        expense_attributes = [
            'concept',
            'type',
            'cost'
        ]
        self.error = validate_empty_values(self.expense, expense_attributes)
        
        return self.error
    
    def validate_unique_values(self):
        expense = Expense.search(self.expense.concept)
        if expense and expense is not self.expense:
            self.error = repeated_value_error

        return self.error