from . import ExpenseTest
from EnGo.models.expense import Expense


class TestAdd(ExpenseTest):

    def test_should_add_expense_given_valid_expense(self):
        expense = Expense(
            concept="Valid Name",
            type_id=self.expense_type.id
        )
        expense.request.add()

        self.assertIn(expense, self.db.session)
    
    def test_should_not_add_expense_given_invalid_expense(self):
        expense = Expense(
            concept="",
            type_id=self.expense_type.id
        )
        expense.request.add()

        self.assertNotIn(expense, self.db.session)


class TestUpdate(ExpenseTest):

    def test_should_update_expense_given_valid_change(self):
        self.expense.concept = "New Concept"
        self.expense.request.update()
        self.db.session.rollback()

        self.assertEqual(self.expense.concept, "New Concept")
    
    def test_should_not_update_expense_given_invalid_change(self):
        self.expense.concept = ""
        self.expense.request.update()
        self.db.session.rollback()

        self.assertNotEqual(self.expense.concept, "")