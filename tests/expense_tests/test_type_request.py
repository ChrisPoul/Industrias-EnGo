from . import ExpenseTest
from EnGo.models.expense import ExpenseType


class TestAdd(ExpenseTest):

    def test_should_add_expense_type_given_valid_expense_type(self):
        expense_type = ExpenseType(
            name="Valid Type"
        )
        expense_type.request.add()

        self.assertIn(expense_type, self.db.session)

    def test_should_not_add_expense_type_given_invalid_expense_type(self):
        expense_type = ExpenseType(
            name=""
        )
        expense_type.request.add()

        self.assertNotIn(expense_type, self.db.session)


class TestUpdate(ExpenseTest):

    def test_should_update_expense_type_given_valid_changes(self):
        self.expense_type.name = "New Type"
        self.expense_type.request.update()
        self.db.session.rollback()

        self.assertEqual(self.expense_type.name, "New Type")

    def test_should_not_update_expense_type_given_invalid_changes(self):
        self.expense_type.name = ""
        self.expense_type.request.update()
        self.db.session.rollback()

        self.assertNotEqual(self.expense_type.name, "")