from . import ExpenseTest
from EnGo.models.expense import Expense


class TestValidateEmptyValues(ExpenseTest):

    def test_should_not_return_error_given_valid_expense(self):
        expense = Expense(
            concept="Valid Name",
            type="Test Type"
        )
        error = expense.validation.validate()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_empyt_value(self):
        expense = Expense(
            concept="",
            type="Test Type"
        )
        error = expense.validation.validate()

        self.assertNotEqual(error, None)


class TestValidateUniqueValues(ExpenseTest):

    def test_should_not_return_error_given_valid_expense(self):
        expense = Expense(
            concept="Valid Name"
        )
        error = expense.validation.validate()

        self.assertEqual(error, None)

    def test_should_return_error_given_repeated_value(self):
        expense = Expense(
            concept="Test Expense"
        )
        error = expense.validation.validate()

        self.assertNotEqual(error, None)
    
    def test_should_not_return_error_given_expense_already_in_db(self):
        error = self.expense.validation.validate()

        self.assertEqual(error, None)
