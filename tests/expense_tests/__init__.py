from tests import Test
from EnGo.models.expense import Expense


class ExpenseTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.expense = Expense(
            concept="Test Expense",
            type="Test Type"
        )
        self.expense.add()
