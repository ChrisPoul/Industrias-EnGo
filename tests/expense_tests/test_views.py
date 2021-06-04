from EnGo.models import expense
from . import ExpenseTest
from flask import url_for
from EnGo.models.expense import Expense

### LOGED IN USER HAS PERMISSISON (LUHP) ###
### LOGED IN USER HAS NO PERMISSION (LUHNP) ###


class ExpenseViewTest:

    def __init__(self):
        ExpenseTest.setUp(self)
        self.create_test_users()


class TestAddView(ExpenseViewTest):

    def test_should_add_expense_given_valid_expense_and_LUHP(self):
        self.login_user(self.admin_user)
        expense_data = dict(
            concept="Valid Concept",
            type="Valid Type"
        )
        with self.client as client:
            client.post(
                url_for('expense.add'),
                data=expense_data
            )
        
        self.assertFalse(Expense.search("Valid Concept"))
    
    def test_should_not_add_expense_given_invalid_expense_and_LUHP(self):
        self.login_user(self.admin_user)
        expense_data = dict(
            concept="",
            type="Valid Type"
        )
        with self.client as client:
            client.post(
                url_for('expense.add'),
                data=expense_data
            )
        
        self.assertFalse(Expense.search("Valid Concept")