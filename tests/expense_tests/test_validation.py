from . import ExpenseTest
from EnGo.models.expense import Expense


class TestValidate(ExpenseTest):

    def test_should_not_return_error_given_valid_expense(self):
        expense = Expense(
            concept="Valid Name",
            type_id=self.expense_type.id
        )
        error = expense.validation.validate()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_invalid_expense(self):
        expense = Expense(
            concept="",
            type_id=self.expense_type.id,
            cost="invalid cost"
        )
        error = expense.validation.validate()

        self.assertNotEqual(error, None)


class TestValidateEmptyValues(ExpenseTest):

    def test_should_not_return_error_given_no_empty_values(self):
        expense = Expense(
            concept="Valid Name",
            type_id=self.expense_type.id
        )
        error = expense.validation.validate_empty_values()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_empty_value(self):
        expense = Expense(
            concept="",
            type_id=self.expense_type.id
        )
        error = expense.validation.validate_empty_values()

        self.assertNotEqual(error, None)


class TestValidateNums(ExpenseTest):

    def test_should_not_return_error_given_valid_nums(self):
        expense = Expense(
            concept="Test Expense",
            type_id=self.expense_type.id,
            cost="10"
        )
        error = expense.validation.validate_nums()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_nums(self):
        expense = Expense(
            concept="Test Expense",
            type_id=self.expense_type.id,
            cost="invalid_num"
        )
        error = expense.validation.validate_nums()

        self.assertNotEqual(error, None)
