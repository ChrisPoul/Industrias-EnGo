from . import ExpenseTest
from EnGo.models.expense import Expense


class TestAdd(ExpenseTest):

    def test_should_add_expense_given_valid_expense(self):
        expense = Expense(
            concept="Valid Name",
            type="Test Type"
        )
        expense.request.add()

        self.assertIn(expense, self.db.session)
    
    def test_should_not_add_expense_given_invalid_expense(self):
        expense = Expense(
            concept="",
            type="Test Type"
        )
        expense.request.add()

        self.assertNotIn(expense, self.db.session)