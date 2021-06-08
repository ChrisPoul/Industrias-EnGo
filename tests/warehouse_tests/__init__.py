from tests import Test
from EnGo.models.warehouse import Warehouse
from EnGo.models.expense import Expense


class WarehouseTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.warehouse = Warehouse(
            address="Test Address"
        )
        self.warehouse.add()
        self.expense = Expense(
            concept="Test Expense",
            type_id=1
        )
        self.expense.add()
