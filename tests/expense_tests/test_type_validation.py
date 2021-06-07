from . import ExpenseTest
from EnGo.models.expense import ExpenseType


class TestValidate(ExpenseTest):

    def test_should_not_return_error_given_valid_expense_type(self):
        expense_type = ExpenseType(
            name="Valid Type"
        )
        error = expense_type.validation.validate()

        self.assertEqual(error, None)

    def test_should_return_error_given_repeated_value(self):
        expense_type = ExpenseType(
            name="Test Type"
        )
        error = expense_type.validation.validate()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_empty_value(self):
        expense_type = ExpenseType(
            name=""
        )
        error = expense_type.validation.validate()

        self.assertNotEqual(error, None)


class TestValidateUniqueValues(ExpenseTest):

    def test_should_not_return_error_given_unique_value(self):
        expense_type = ExpenseType(
            name="Unique Expense Type"
        )
        error = expense_type.validation.validate_unique_values()

        self.assertEqual(error, None)

    def test_should_return_error_given_repeated_value(self):
        expense_type = ExpenseType(
            name="Test Type"
        )
        error = expense_type.validation.validate_unique_values()

        self.assertNotEqual(error, None)

    def test_should_not_return_error_given_expense_type_already_in_db(self):
        error = self.expense_type.validation.validate_unique_values()

        self.assertEqual(error, None)


class TestValidateUniqueValues(ExpenseTest):

    def test_should_not_return_error_given_no_empty_values(self):
        expense_type = ExpenseType(
            name="Test Type"
        )
        error = expense_type.validation.validate_empty_values()

        self.assertEqual(error, None)

    def test_should_return_error_given_empty_value(self):
        expense_type = ExpenseType(
            name=""
        )
        error = expense_type.validation.validate_empty_values()

        self.assertNotEqual(error, None)