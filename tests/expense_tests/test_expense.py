from . import ExpenseTest
from EnGo.models.expense import Expense


class TestAdd(ExpenseTest):

    def test_should_add_expense(self):
        expense = Expense(
            concept="Some Expense",
            type_id=self.expense_type.id
        )
        expense.add()

        self.assertIn(expense, self.db.session)


class TestUpdate(ExpenseTest):

    def test_should_update_expense(self):
        self.expense.concept = "New Name"
        self.expense.update()
        self.db.session.rollback()

        self.assertEqual(self.expense.concept, "New Name")


class TestDelete(ExpenseTest):

    def test_should_delete_expense(self):
        self.expense.delete()

        self.assertNotIn(self.expense, self.db.session)


class TestGet(ExpenseTest):

    def test_should_return_expense_given_valid_id(self):
        expense = Expense.get(self.expense.id)

        self.assertEqual(expense, self.expense)


class TestGetAll(ExpenseTest):

    def test_should_return_all_expenses(self):
        expenses = Expense.get_all()

        self.assertEqual(expenses, [self.expense])


class TestSearchAll(ExpenseTest):

    def test_should_return_expense_given_valid_search_term(self):
        expenses = Expense.search_all(self.expense.concept)

        self.assertEqual(expenses, [self.expense])

