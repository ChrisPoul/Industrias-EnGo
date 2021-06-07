from tests import Test
from EnGo.models.expense import Expense, ExpenseType


class ExpenseTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.expense_type = ExpenseType(
            name="Test Expense"
        )
        self.expense_type.add()
        self.expense = Expense(
            concept="Test Expense",
            type_id=self.expense_type.id
        )
        self.expense.add()
