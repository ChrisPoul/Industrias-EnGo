from . import Expense, ExpenseType
from EnGo.errors.messages import repeated_value_error
from EnGo.models import validate_empty_values, validate_obj_num_attrs


class ExpenseValidation:

    def __init__(self, expense):
        self.expense = expense
        self.error = None

    def validate(self):
        self.validate_empty_values()
        if not self.error:
            self.validate_nums()

        return self.error
    
    def validate_empty_values(self):
        expense_attributes = [
            'concept',
            'cost',
            'quantity',
            'unit'
        ]
        self.error = validate_empty_values(self.expense, expense_attributes)
        
        return self.error
    
    def validate_nums(self):
        expense_nums = [
            'cost',
            'quantity'
        ]
        self.error = validate_obj_num_attrs(self.expense, expense_nums)
    
        return self.error


class ExpenseTypeValidation:

    def __init__(self, expense_type):
        self.expense_type = expense_type
        self.error = None

    def validate(self):
        self.validate_empty_values()
        if not self.error:
            self.validate_unique_values()

        return self.error

    def validate_unique_values(self):
        expense_type = ExpenseType.search(self.expense_type.name)
        if expense_type and expense_type is not self.expense_type:
            self.error = repeated_value_error

        return self.error

    def validate_empty_values(self):
        self.error = validate_empty_values(self.expense_type, ["name"])

        return self.error